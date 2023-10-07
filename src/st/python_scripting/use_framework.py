from os import chdir
import shutil
import subprocess
from pathlib import Path
import re

def use_framework_compile(workdir: Path, cube_mx: Path, cube_project: Path, repetitions: int, model: Path):
    """Uses MX cube application to benchmark the model on the MCU.
    """
    step_output = dict()

    # Create the directpry where cube MX will generate the project
    project_name = cube_project.stem
    generate_directory = workdir / Path("gen")
    generate_directory.mkdir()

    # Create the directory where the network report will be saved
    project_name = cube_project.stem
    generate_directory = workdir / Path("network_output")
    generate_directory.mkdir()

    # Modify and copy the input script for MX to generate the project
    mx_generate_script = workdir / Path("..", "misc", "gen_mx_prj.txt")
    # get the .ioc file by matching the .ioc file type
    ioc_files = cube_project.glob("*.ioc")
    first_ioc_file = next(ioc_files, None)
    # set the mx generate script from the template path to the workdir path
    mx_generate_script = set_generate_path(workdir, mx_generate_script, first_ioc_file, generate_directory)

    generate_command = f"{cube_mx} -q {mx_generate_script}"
    make_dir = generate_directory / Path(project_name)
    compile_cmd = f"make -C {make_dir}"

    # print("generate_command", generate_command)
    # print("compile_cmd", compile_cmd)
    # import sys;sys.exit(0)
    
    #TODO: Cube MX immmediately notices if I fuck with the IOC file,
    # e.g. replace the model path with a placeholder for the workdir
    # I need something like a hex editor to modify the placeholder without them noticing the modifications

    subprocess.run(generate_command, shell=True)

    # Set number of iterations per perf test to the reps variable, 
    # the default value is 16, we overwrite it here. 
    # Maybe there is a way to configure that in the MX IDE, that setting wasn't found.
    aiSystemPerformance_c = generate_directory / Path(project_name, "X-CUBE-AI", "App", "aiSystemPerformance.c")
    main_c = generate_directory / Path(project_name, "Core", "Src", "main.c")
    set_repetitions_and_observer_end(aiSystemPerformance_c, repetitions, observer=True)
    set_end_of_benchmark(main_c)
    # TODO: correct readback method to log all lines sent

    subprocess.run(compile_cmd, shell=True)
    # print("mx_generate_script", mx_generate_script)
    # print("generate_command", generate_command)
    # print("compile_cmd", compile_cmd)

    elf_file = make_dir / Path("build", project_name + ".elf")
    print(elf_file)
    assert elf_file.exists()
    step_output["cube_template"] = elf_file

    return step_output


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
