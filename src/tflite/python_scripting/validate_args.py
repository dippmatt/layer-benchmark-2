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

    args.out_dir = Path(args.out_dir).resolve()
    assert args.out_dir.is_dir(), f"Output directory {args.out_dir} not found!."

    args.model = Path(args.model).resolve()
    assert args.model.is_file(), f"Could not find model file at path: {args.model}"

    args.input_tensors = Path(args.input_tensors).resolve()
    assert args.input_tensors.is_file(), f"No .npz array at location {args.input_tensors} not found!"

    args.cube_programmer = Path(args.cube_programmer).resolve()
    assert args.cube_programmer.is_file(), f"STM 32 Cube Programmer executable {args.cube_programmer} not found!."

    args.cube_mx = Path(args.cube_mx).resolve()
    assert args.cube_mx.is_file(), f"STM 32 Cube MX executable {args.cube_mx} not found!."

    args.cube_ide = Path(args.cube_ide).resolve()
    assert args.cube_ide.is_file(), f"STM 32 Cube IDE executable {args.cube_ide} not found!."

    args.cube_ide_workspace = Path(args.cube_ide_workspace).expanduser().resolve()
    assert args.cube_ide_workspace.is_dir(), f"STM 32 Cube IDE workspace {args.cube_ide_workspace} not found!."

    args.stm32tflm = Path(args.stm32tflm).expanduser().resolve()
    assert args.stm32tflm.is_file(), f"STM 32 Cube IDE executable {args.stm32tflm} not found!."

    args.stm32ai = Path(args.stm32ai).resolve()
    assert args.stm32ai.is_file(), f"STM 32 Cube AI executable {args.stm32ai} not found!."

    args.cube_template = Path(args.cube_template).resolve()
    assert args.cube_template.is_dir(), f"STM Cube IDE template project {args.cube_template} not found!."

    args.cube_template_validate = Path(args.cube_template_validate).resolve()
    assert args.cube_template_validate.is_dir(), f"STM Cube IDE template project {args.cube_template_validate} not found!."

    # Cube AI does not perform quantization, so we don't hardcode the following options
    args.quantize = False
    args.representative_tensors = None

    # args.cube_template_empty = Path(args.cube_template_empty).resolve()
    # assert args.cube_template_empty.is_dir(), f"STM Cube IDE template project {args.cube_template_empty} not found!."

    return