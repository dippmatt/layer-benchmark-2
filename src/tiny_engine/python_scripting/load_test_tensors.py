from pathlib import Path
import numpy as np

from color_print import print_in_color, Color

INPUT_SAMPLES = 10
PROFILE_SAMPLES = 1000

def load_test_tensors(input_tensors: Path, representative_tensors: Path, quantize: bool):
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

    # only load 
    if quantize:
        assert representative_tensors.suffix == ".npz", f"Invalid data type for representative tensors {representative_tensors}: .npz array required!"

        input_data = np.load(representative_tensors)
        representative_tensors = input_data['input_tensors']
        num_representative_samples = representative_tensors.shape[0]

        if num_representative_samples > PROFILE_SAMPLES:
            print_in_color(Color.YELLOW, f"Note: Found {num_representative_samples} samples in representative_tensors, but limiting sample size to {PROFILE_SAMPLES} for simplicity!")
            representative_tensors = representative_tensors[:PROFILE_SAMPLES,...]
            num_representative_samples = PROFILE_SAMPLES

        assert input_tensors.shape[1:] == representative_tensors.shape[1:], f"Input tensors and representative tensors must have the same shape! \
            (except for dimention 0, the sample size) Input tensors: {input_tensors.shape}, representative tensors: {representative_tensors.shape}"
        step_output['num_representative_samples'] = num_representative_samples
        step_output['representative_tensors'] = representative_tensors
    else:
        step_output['num_representative_samples'] = None
        step_output['representative_tensors'] = None


    return step_output