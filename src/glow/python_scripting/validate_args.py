from pathlib import Path
import shutil

def validate_args(args):
    # Check file paths
    
    args.workdir = Path(args.workdir).resolve()
    args.workdir.mkdir(exist_ok=True)
    assert args.workdir.is_dir(), f"Working directory path {args.workdir} does not exist!"
    # clean workdir
    shutil.rmtree(args.workdir)
    args.workdir.mkdir()
    
    # check that all args are set
    # for arg, value in vars(args).items():
    #     assert value is not None, f"Required argument {arg} is not set!"

    args.out_dir = Path(args.out_dir).resolve()
    assert args.out_dir.is_dir(), f"Output directory {args.out_dir} not found!."

    args.cube_template = Path(args.cube_template).resolve()
    assert args.cube_template.is_dir(), f"Did not find path to STM Cube IDE template project: {args.cube_template}"
    
    args.cube_template_ref = Path(args.cube_template_ref).resolve()
    assert args.cube_template_ref.is_dir(), f"Did not find path to STM Cube IDE template project: {args.cube_template_ref}"

    args.cube_template_empty = Path(args.cube_template_empty).resolve()
    assert args.cube_template_empty.is_dir(), f"Did not find path to STM Cube IDE template project: {args.cube_template_empty}"

    args.model = Path(args.model).resolve()
    assert args.model.is_file(), f"Could not find model file at path: {args.model}"

    args.glow_compiler = Path(args.glow_compiler).resolve()
    assert args.glow_compiler.is_file(), f"Glow compiler executable {args.glow_compiler} not found!"

    args.cube_programmer = Path(args.cube_programmer).resolve()
    assert args.cube_programmer.is_file(), f"STM 32 Cube Cube Programmer executable {args.cube_programmer} not found!."

    args.input_tensors = Path(args.input_tensors).resolve()
    # find any .bin files in directory
    tensor_files = list(args.input_tensors.glob(f"*{'.bin'}"))
    assert args.input_tensors.suffix == ".npz" or len(tensor_files) > 0, f"No tensors found at location {args.input_tensors} not found!"

    assert args.repetitions >= 1, f"Must specify number of repetitions as integer >= 1."

    if args.quantize:
        args.glow_profiler = Path(args.glow_profiler).resolve()
        assert args.glow_profiler.is_file(), f"Glow model profiler executable {args.glow_profiler} not found!"

        args.representative_tensors = Path(args.representative_tensors).resolve()
        assert args.representative_tensors.is_file(), f"No .npz array at location {args.representative_tensors} not found!"

    # Things omitted here, todo in validata_data:
    # - flag indicating if profile has to be created 
    # - model IO info (shape, dtype)
    return