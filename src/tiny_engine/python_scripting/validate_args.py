from pathlib import Path
import shutil

def validate_args(args):
    # Check file paths
    
    args.workdir = Path(args.workdir).resolve()
    assert args.workdir.is_dir(), f"Working directory path {args.workdir} does not exist!"
    # clean workdir
    shutil.rmtree(args.workdir)
    args.workdir.mkdir()

    args.tiny_engine_submodule = Path(args.tiny_engine_submodule).resolve()
    assert args.tiny_engine_submodule.is_dir(), f"Could not find submodule directory for tinyengine at path: {args.tiny_engine_submodule}"

    args.model = Path(args.model).resolve()
    assert args.model.is_file(), f"Could not find model file at path: {args.model}"

    args.input_tensors = Path(args.input_tensors).resolve()
    assert args.input_tensors.is_file(), f"No .npz array at location {args.input_tensors} not found!"

    args.cube_programmer = Path(args.cube_programmer).resolve()
    assert args.cube_programmer.is_file(), f"STM 32 Cube Cube Programmer executable {args.cube_programmer} not found!."

    args.cube_template = Path(args.cube_template).resolve()
    assert args.cube_template.is_dir(), f"STM Cube IDE template project {args.cube_template} not found!."

    return