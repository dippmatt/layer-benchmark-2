from typing import Dict
from pathlib import Path
import shutil

def load_cube_project(workdir: Path, cube_template: Path):#, cube_template_ref: Path, cube_template_empty: Path):
    step_output = dict()

    dst_cube_template = workdir / cube_template.name
    # dst_cube_template_ref = workdir / cube_template_ref.name
    # dst_cube_template_empty = workdir / cube_template_empty.name

    step_output['cube_template'] = shutil.copytree(cube_template, dst_cube_template)
    # step_output['cube_template_ref'] = shutil.copytree(cube_template_ref, dst_cube_template_ref)
    # step_output['cube_template_empty'] = shutil.copytree(cube_template_empty, dst_cube_template_empty)
    return step_output
    