from typing import Dict
from enum import Enum
from os import chdir
import shutil
import subprocess
from pathlib import Path
import re
from shared_scripts.color_print import print_in_color, Color
from flash_and_readback import flash_mcu

def use_framework_compile(workdir: Path, cube_mx: Path, stm32ai: Path, repetitions: int, cube_programmer: Path, model: Path, cube_project: Path, cube_project_validate: Path):
    """Uses MX cube application to benchmark the model on the MCU.
    """
    step_output = dict()

    # Create the directpry where cube MX will validate the project
    validate_directory = workdir / Path("validate")
    validate_directory.mkdir()

    # Create the directories where cube MX will generate the projects
    generate_main_prj_dir = workdir / Path("gen", "main")
    generate_main_prj_dir.mkdir(parents=True, exist_ok=True)
    generate_valitate_prj_dir = workdir / Path("gen", "validate")
    generate_valitate_prj_dir.mkdir(parents=True, exist_ok=True)
    generate_reference_prj_dir = workdir / Path("gen", "reference")
    generate_reference_prj_dir.mkdir(parents=True, exist_ok=True)

    # Create the directory where the network report will be saved
    network_output_directory = workdir / Path("network_output")
    network_output_directory.mkdir(parents=True, exist_ok=True)
    # "network_output" is the directory where the network report will be saved,
    # as well as the output tensors of the network. We already know the path.
    step_output["tensor_values"] = network_output_directory / Path("network_val_io.npz")

    # Modify and copy the input script for MX to generate the project
    mx_generate_script = workdir / Path("..", "misc", "gen_mx_prj.txt")
    
    # compile main project, all layer project and validation project
    compile_project(workdir, 
                    cube_mx, 
                    cube_programmer,
                    stm32ai,
                    model,
                    step_output, 
                    repetitions, 
                    cube_project_validate, 
                    mx_generate_script, 
                    generate_valitate_prj_dir, 
                    compile_mode=CompileMode.VALIDATE, 
                    postfix="_validate",
                    validate_directory=validate_directory,
                    network_output_directory=network_output_directory)
    
    compile_project(workdir, 
                    cube_mx,
                    cube_programmer,
                    stm32ai,
                    model,
                    step_output, 
                    repetitions, 
                    cube_project, 
                    mx_generate_script, 
                    generate_reference_prj_dir, 
                    compile_mode=CompileMode.REFERENCE, 
                    postfix="_all_layers")
    
    compile_project(workdir, 
                    cube_mx,
                    cube_programmer,
                    stm32ai,
                    model,
                    step_output, 
                    repetitions, 
                    cube_project, 
                    mx_generate_script, 
                    generate_main_prj_dir, 
                    compile_mode=CompileMode.BENCHMARK, 
                    postfix="")
    
    return step_output


def compile_project(workdir: Path, 
                    cube_mx: Path, 
                    cube_programmer: Path,
                    stm32ai: Path,
                    model: Path,
                    step_output: Dict, 
                    repetitions: int, 
                    cube_project: Path, 
                    mx_generate_script: Path, 
                    generate_prj_dir: Path, 
                    compile_mode: Enum, 
                    postfix: str, 
                    validate_directory: Path = None,
                    network_output_directory: Path = None):
    
    # get the .ioc file by matching the .ioc file type
    ioc_files = cube_project.glob("*.ioc")
    first_ioc_file = next(ioc_files, None)

    #project_name = cube_project.stem
    project_name = Path(first_ioc_file).stem
    print_in_color(Color.BLUE, "project_name: " + project_name)
    
    # set the mx generate script from the template path to the workdir path
    mx_generate_script = set_generate_path(workdir, mx_generate_script, first_ioc_file, generate_prj_dir)
    
    # Generate the C project
    generate_command = f"{cube_mx} -q {mx_generate_script}"
    
    # Compile the C project
    make_dir = generate_prj_dir / Path(project_name)
    compile_cmd = f"make -C {make_dir}"

    if compile_mode == CompileMode.BENCHMARK:
        generate_log = workdir / Path("generate_out.txt")
        with open(generate_log, "w") as outfile:
            result = subprocess.run(generate_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            # Print the output to the terminal
            print(result.stdout, end='')
            outfile.write(result.stdout)

        extract_network_analyze_report_info(workdir, generate_log, step_output)
    else:
        subprocess.run(generate_command, shell=True)  

    if compile_mode in [CompileMode.BENCHMARK, CompileMode.REFERENCE]:
        # Set number of iterations per perf test to the reps variable, 
        # the default value is 16, we overwrite it here. 
        # Maybe there is a way to configure that in the MX IDE, that setting wasn't found.
        aiSystemPerformance_c = generate_prj_dir / Path(project_name, "X-CUBE-AI", "App", "aiSystemPerformance.c")
        main_c = generate_prj_dir / Path(project_name, "Core", "Src", "main.c")
        if compile_mode == CompileMode.BENCHMARK:
            set_repetitions_and_observer_end(aiSystemPerformance_c, repetitions, observer=True)
        else:
            set_repetitions_and_observer_end(aiSystemPerformance_c, repetitions, observer=False)
        set_end_of_benchmark(main_c)

    subprocess.run(compile_cmd, shell=True)

    elf_file = make_dir / Path("build", project_name + ".elf")
    print(elf_file)
    assert elf_file.exists()
    step_output["cube_template" + postfix] = elf_file

    # validate the model
    if compile_mode == CompileMode.VALIDATE:
        flash_mcu(cube_programmer, elf_file)
        
        # # analyze model
        # analyze_command = f"{stm32ai} analyze \
        #         --name network -m {model} \
        #         --type tflite \
        #         --compression none \
        #         --verbosity 1 \
        #         --output {network_output_directory} \
        #         --allocate-inputs \
        #         --series stm_series \
        #         --allocate-outputs"
        # subprocess.run(analyze_command, shell=True)
        
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
                --desc /dev/ttyACM0:115200"
        
        subprocess.run(validate_command, shell=True)
        
        # Check if the validation was successful and we got the output tensors
        assert step_output["tensor_values"].exists()
   
    return


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
    

class CompileMode(Enum):
    BENCHMARK = 1
    REFERENCE = 2
    VALIDATE = 3


if __name__ == "__main__":
    from pathlib import Path
    
    # Prepare directory structure
    workdir = Path.cwd() / Path("..", "workdir")
    submodule_dir = Path.cwd() / Path("..", "..", "..", "third_party", "tinyengine")
    
    model = Path("/home/matthias/Documents/BA/results/models_and_data/anomaly_detection/trained_models/ad01_int8.tflite")
    prep_tinyengine_framework(workdir, submodule_dir, model)
