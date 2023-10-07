from typing import Dict
from pathlib import Path
import subprocess
import shutil
import os

def load_cube_project(workdir: Path, cube_template: Path, cube_template_ref: Path, cube_template_empty: Path, model: Path,):#, cube_template_ref: Path, cube_template_empty: Path):
    step_output = dict()

    dst_cube_template = workdir / cube_template.name
    # dst_cube_template_all_layers = workdir / Path(cube_template.name + '_all_layers')
    # dst_cube_template_ref = workdir / cube_template_ref.name
    # dst_cube_template_empty = workdir / cube_template_empty.name

    step_output['cube_template'] = shutil.copytree(cube_template, dst_cube_template)
    set_model_and_workdir_path(workdir, model, step_output['cube_template'])
    # step_output['cube_template_all_layers'] = shutil.copytree(cube_template, dst_cube_template_all_layers)
    # step_output['cube_template_ref'] = shutil.copytree(cube_template_ref, dst_cube_template_ref)
    # step_output['cube_template_empty'] = shutil.copytree(cube_template_empty, dst_cube_template_empty)
    return step_output
    
def set_model_and_workdir_path_bad(workdir, model, cube_template):

    # get the .ioc file by matching the .ioc file type
    ioc_files = cube_template.glob("*.ioc")
    first_ioc_file = next(ioc_files, None)

    with open(first_ioc_file, 'r') as file:
        file_content = file.readlines()

    for i, line in enumerate(file_content):
        if "/home/matthias/Documents/BA/layer-benchmark-2/src/st/workdir/model.tflite" in line:
            line = line.replace("/home/matthias/Documents/BA/layer-benchmark-2/src/st/workdir/model.tflite", str(model))
            file_content[i] = line

    # Save the modified content to a temporary file
    temp_file_path = workdir / Path("temp.txt")
    temp_file_path.resolve()
    temp_file_path.touch()

    with open(temp_file_path, 'w') as temp_file:
        temp_file.writelines(file_content)
    assert temp_file_path.is_file()

    # Copy the metadata (including timestamps) from the original file to the temporary file
    shutil.copystat(first_ioc_file, temp_file_path)

    # Replace the original file with the temporary file
    os.remove(first_ioc_file)
    os.rename(temp_file_path, first_ioc_file)

    # Optionally, you can delete the temporary file
    os.remove(temp_file_path)
    return 

def set_model_and_workdir_path(workdir, model, cube_template):
    ###################################################
    # TODO: remove this test
    # model = Path(model).parent / Path("..", "model.tfllite")
    # model = model.resolve()
    # print("model", model)

    # Right now, the alterning the model path in the .ioc does not get applied
    # the change gets overwritten immediatly when launching cube mx in the automation script
    # I could not find a way to find the cached model path  or change this behaviour
    # Workaround to change the model path: open the cube template in cube mx and change the path manually,
    # then save the project and close cube mx.
    ###################################################

    # get the .ioc file by matching the .ioc file type
    ioc_files = cube_template.glob("*.ioc")
    first_ioc_file = next(ioc_files, None)
    
    # Step 1: Extract the current modification timestamp
    original_timestamp = os.path.getmtime(str(first_ioc_file))
    
    subprocess.run(["sed", "-i", f"s#/home/matthias/Documents/BA/layer-benchmark-2/src/st/workdir/model.tflite#{str(model)}#g", str(first_ioc_file)])

    # Step 3: Set the modified timestamp using the touch command
    new_timestamp = original_timestamp  # You can set this to your desired timestamp
    formatted_new_timestamp = "@{}".format(int(new_timestamp))

    # Use subprocess to run the touch command with the new timestamp
    try:
        subprocess.run(["touch", "-d", formatted_new_timestamp, str(first_ioc_file)], check=True)
        print("Timestamp successfully set to", formatted_new_timestamp)
    except subprocess.CalledProcessError as e:
        print("Error setting timestamp:", e)
    
    # with open(first_ioc_file, "r") as f:
    #     lines = f.readlines()
    # for i, line in enumerate(lines):
    #     if "<MODEL_PATH>" in line:
    #         line = line.replace("<MODEL_PATH>", str(model))
    #         lines[i] = line
    #     elif "<WORKDIR_PATH>" in line:
    #         line = line.replace("<WORKDIR_PATH>", str(workdir))
    #         lines[i] = line
    # with open(first_ioc_file, "w") as f:
    #     f.writelines(lines)
    return
