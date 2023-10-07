from os import chdir
import shutil
import subprocess
from pathlib import Path
import re
from shared_scripts.color_print import print_in_color, Color

def use_framework_compile(workdir: Path, cube_mx: Path, stm32ai: Path, cube_project: Path, repetitions: int, model: Path):
    """Uses MX cube application to benchmark the model on the MCU.
    """
    step_output = dict()

    project_name = cube_project.stem

    # Create the directpry where cube MX will validate the project
    validate_directory = workdir / Path("validate")
    validate_directory.mkdir()

    # Create the directpry where cube MX will generate the project
    generate_directory = workdir / Path("gen")
    generate_directory.mkdir()

    # Create the directory where the network report will be saved
    network_output_directory = workdir / Path("network_output")
    network_output_directory.mkdir()

    # Modify and copy the input script for MX to generate the project
    mx_generate_script = workdir / Path("..", "misc", "gen_mx_prj.txt")
    # get the .ioc file by matching the .ioc file type
    ioc_files = cube_project.glob("*.ioc")
    first_ioc_file = next(ioc_files, None)
    # set the mx generate script from the template path to the workdir path
    mx_generate_script = set_generate_path(workdir, mx_generate_script, first_ioc_file, generate_directory)

    # Validate the input data
    input_data_path = workdir / Path("data.npz")
    validate_command = f"{stm32ai} validate \
            --name network -m {model} \
            --type tflite \
            --compression none \
            --verbosity 1 \
            --workspace {validate_directory} \
            --output {network_output_directory} \
            --allocate-inputs \
            --allocate-outputs \
            --mode stm32 \
            --valinput {input_data_path} \
            --desc 115200"
    
    # Generate the C project
    generate_command = f"{cube_mx} -q {mx_generate_script}"
    
    # Compile the C project
    make_dir = generate_directory / Path(project_name)
    compile_cmd = f"make -C {make_dir}"

    subprocess.run(validate_command, shell=True)

    generate_log = workdir / Path("generate_out.txt")
    with open(generate_log, "w") as outfile:
        result = subprocess.run(generate_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        # Print the output to the terminal
        print(result.stdout, end='')
        outfile.write(result.stdout)

    extract_network_analyze_report_info(workdir, generate_log, step_output)

    # Set number of iterations per perf test to the reps variable, 
    # the default value is 16, we overwrite it here. 
    # Maybe there is a way to configure that in the MX IDE, that setting wasn't found.
    aiSystemPerformance_c = generate_directory / Path(project_name, "X-CUBE-AI", "App", "aiSystemPerformance.c")
    main_c = generate_directory / Path(project_name, "Core", "Src", "main.c")
    set_repetitions_and_observer_end(aiSystemPerformance_c, repetitions, observer=True)
    set_end_of_benchmark(main_c)

    subprocess.run(compile_cmd, shell=True)

    elf_file = make_dir / Path("build", project_name + ".elf")
    print(elf_file)
    assert elf_file.exists()
    step_output["cube_template"] = elf_file

    return step_output


def extract_network_analyze_report_info(workdir: Path, generate_log: Path, step_output: dict):
    """Extracts the network analyze report from the generate log.

    Info found in the network analyze report:
    Flash usage, RAM usage: network only and network + framework (toolchain, runtime)
    """
    with open(generate_log, "r") as f:
        lines = f.readlines()
    # flag to indicate that the network analyze report is being read
    extraction_start = False
    report = []
    for i, line in enumerate(lines):
        if "Exec/report summary (analyze)" in line:
            extraction_start = True
        if extraction_start:
            report.append(line)
            if "Creating txt report file" in line:
                report_file = line.split("Creating txt report file ")[1].strip()
                print_in_color(Color.GREEN, f"Found network analyze report at {report_file}")
                break
    report_file = workdir / Path(report_file).stem
    with open(report_file, "w") as f:
        f.writelines(report)
    
    # extract flash and ram usage
    start_summery_flag = False
    for line in report:
        if "Summary per memory device type" in line:
            start_summery_flag = True
        if start_summery_flag:
            # RT total is the calculated ram and flash ONLY of the runtime using 
            # text, rodata, data and bss sections of the elf file
            if "RT total" in line:
                line = line.split("RT total")[1]
                result = re.split(r'\s+', line.strip())
                flash_usage_rt = result[0].replace(",", "")
                ram_usage_rt = result[2].replace(",", "")
            # TOTAL is the calculated ram and flash of the runtime AND the network (weights, activations, io buffers)
            if "TOTAL" in line:
                line = line.split("TOTAL")[1]
                result = re.split(r'\s+', line.strip())
                flash_usage = result[0].replace(",", "")
                ram_usage = result[1].replace(",", "")
                break
    
    # save the results in KB (not KiB!)
    step_output["flash"] = int(flash_usage) / 1000
    step_output["ram"] = int(ram_usage) / 1000
    step_output["flash_rt"] = int(flash_usage_rt) / 1000
    step_output["ram_rt"] = int(ram_usage_rt) / 1000
    print("RAM / RAM_RT: ", step_output["ram"], step_output["ram_rt"])
    print("FLASH / FLASH_RT: ", step_output["flash"], step_output["flash_rt"])
    return
 

def set_repetitions_and_observer_end(aiSystemPerformance_c: Path, repetitions: int, observer: bool = True):
    """Sets the number of repetitions for a given performance test 
    and if per-layer measurements should be used.
    
    Args:
        aiSystemPerformance_c (Path): Path to the C file to modify
        num_reps (int): number of repetitions to set
    """
    pattern = r"#define _APP_ITER_[ \t]+\d+"
    with open(aiSystemPerformance_c, "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        # set number of repetitions
        if re.match(pattern, line):
            lines[i] = f"#define _APP_ITER_ {repetitions}\n"
        # set termination condition of benchmark
        if "idx = (idx+1) % AI_MNETWORK_NUMBER;" in line:
            lines[i+1] = "    r=CONS_EVT_QUIT;\n"
        # set observer
        if not observer:
            if "#define USE_OBSERVER" in line:
                lines[i] = "#define USE_OBSERVER 0\n"
    with open(aiSystemPerformance_c, "w") as f:
        f.writelines(lines)
    return


def set_end_of_benchmark(main_c: Path):
    """Sets the termination condition for the benchmark in the main() functions's while loop.
    """
    found_line_flag = False
    with open(main_c, "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if "MX_X_CUBE_AI_Process();" in line:
            found_line_flag = True
        elif found_line_flag:
            insertion = '  uint8_t end_message[] = "Finished timing measurements!\\r\\n";\n  HAL_UART_Transmit (&hlpuart1, end_message, sizeof (end_message), HAL_MAX_DELAY);\n  return 0;\n'
            lines[i] = insertion
            break
    with open(main_c, "w") as f:
        f.writelines(lines)
    return


def set_generate_path(workdir: Path, mx_generate_script: Path, ioc_file: Path, cube_prj_gen: Path):
    """Reads the MX generate script and sets the path to the generated project.
    Then saves the script to workdir.
    """
    with open(mx_generate_script, "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if "<CUBE_PRJ_IOC>" in line:
            line = line.replace("<CUBE_PRJ_IOC>", str(ioc_file))
            lines[i] = line
        elif "<CUBE_PRJ_GEN>" in line:
            line = line.replace("<CUBE_PRJ_GEN>", str(cube_prj_gen))
            lines[i] = line
    save_path = workdir / Path("gen_mx_prj.txt")
    with open(save_path, "w") as f:
        f.writelines(lines)
    return save_path
    

if __name__ == "__main__":
    from pathlib import Path
    
    # Prepare directory structure
    workdir = Path.cwd() / Path("..", "workdir")
    submodule_dir = Path.cwd() / Path("..", "..", "..", "third_party", "tinyengine")
    
    model = Path("/home/matthias/Documents/BA/results/models_and_data/anomaly_detection/trained_models/ad01_int8.tflite")
    prep_tinyengine_framework(workdir, submodule_dir, model)
