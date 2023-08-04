from pathlib import Path
import shutil

def validate_args(args):
    # Check file paths
    
    args.workdir = Path(args.workdir).resolve()
    assert args.workdir.is_dir(), f"Working directory path {args.workdir} does not exist!"
    # clean workdir
    shutil.rmtree(args.workdir)
    args.workdir.mkdir()

    args.submodule_dir = Path(args.submodule_dir).resolve()
    assert args.submodule_dir.is_dir(), f"Could not find submodule directory for tinyengine at path: {args.submodule_dir}"

    args.model = Path(args.model).resolve()
    assert args.model.is_file(), f"Could not find model file at path: {args.model}"

    return