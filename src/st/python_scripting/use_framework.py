from os import chdir
import shutil
import subprocess
from pathlib import Path

def use_framework(workdir: Path, cube_mx: Path, cube_project: Path, model: Path):
    """Uses MX cube application to benchmark the model on the MCU.
    """
    step_output = dict()

    # Create the directpry where cube MX will generate the project
    project_name = cube_project.stem
    generate_directory = workdir / Path("gen")
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
    subprocess.run(compile_cmd, shell=True)
    # print("mx_generate_script", mx_generate_script)
    # print("generate_command", generate_command)
    # print("compile_cmd", compile_cmd)
    import sys;sys.exit(0)

    chdir(cwd)
    step_output["codegen"] = tinyengine_dir / Path("codegen")
    return step_output
    
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
