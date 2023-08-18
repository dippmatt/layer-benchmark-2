from pathlib import Path
import numpy as np

from color_print import print_in_color, Color

INPUT_SAMPLES = 10
PROFILE_SAMPLES = 1000

def load_test_tensors(input_tensors: Path):
    """Imports test tensors to run

    Args:
        input_tensors (Path): npz file with test tensors.
            after np.load, it is expected that 
            the array of tensors can be accessed using array['input_tensors']
        representative_tensors (Path): npz file with representative tensors.
            They are used for calibration during quantization when using the glow model profiler.
        quantize (bool): whether to quantize the model or not

    Returns:
        Dict: step_output
    """    
    step_output = dict()

    assert input_tensors.suffix == ".npz", f"Invalid data type for input tensors {input_tensors}: .npz array required!"
    
    input_data = np.load(input_tensors)
    input_tensors = input_data['input_tensors']
    num_samples = input_tensors.shape[0]

    if num_samples > INPUT_SAMPLES:
        print_in_color(Color.YELLOW, f"Note: Found {num_samples} samples in input_tensors, but limiting sample size to {INPUT_SAMPLES} for simplicity!")
        input_tensors = input_tensors[:INPUT_SAMPLES,...]
        num_samples = INPUT_SAMPLES

    step_output['num_samples'] = num_samples
    step_output['input_tensors'] = input_tensors

    return step_output