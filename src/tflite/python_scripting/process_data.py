from shared_scripts.color_print import print_in_color, Color
from typing import Tuple
import numpy as np
import pandas as pd
from pathlib import Path

def process_data(repetitions: int, num_samples: int, output_shape: Tuple, output_dtype, reference_output: list, tensor_values: list, reps: list, reps_all_layers: list):
    """Processes benchmark data from the STM32 MCU and saves it to a file.
    """
    step_output = dict()

    mcu_tensor_values = process_mcu_output_tensors(output_shape, output_dtype, tensor_values, num_samples)
    step_output["mcu_tensor_values"] = mcu_tensor_values
    
    ref_tensor_values = np.array(reference_output)
    step_output["ref_tensor_values"] = ref_tensor_values
    
    # process per layer timings
    per_layer_timings_mean, layer_names = process_layer_timings(reps)
    step_output["layer_list"] = layer_names

    # process reference total inference time
    all_layers_timings_mean = process_layer_timings_ref(reps_all_layers)  
    
    ########################################
    # dummy value for per_layer_timings_std_dev
    step_output["per_layer_timings_std_dev"] = None
    step_output["all_layers_timings_std_dev"] = None
    print(per_layer_timings_mean)
    print(all_layers_timings_mean)
    ########################################
    
    step_output["per_layer_timings_mean"] = per_layer_timings_mean
    step_output["all_layers_timings_mean"] = all_layers_timings_mean
    
    return step_output


def process_layer_timings_ref(reps_all_layers):
    """Converts the string of averaged timings into a float in ms.
    """
    # Example string to process:
    # duration     : 7.597 ms (average)
    
    assert len(reps_all_layers) == 1, "Found more than one line in reps_all_layers"
    timing = reps_all_layers[0].split(':')[1]
    timing = timing.split('ms')[0]
    
    timing = timing.split(' ')
    # remove empty strings
    timing = list(filter(None, timing))
    
    timing[0] = float(timing[0])
    
    return np.array(timing)


def process_layer_timings(reps):
    """Converts a list of layer timings to a numpy array with one timing in ms per layer.
    """
    # create array-like list of lists for all measurements
    timing_array = []
    layer_names = []

    for rep in reps:
        sample_array = []
        for layer in rep:
            # Example for one layer:
            # 0     FULLY_CONNECTED                2.213  27.33 %
            timing = layer.split(' ')
            # remove empty strings
            timing = list(filter(None, timing))
            layer_names.append(timing[-4])
            timing = timing[-3]
            timing = float(timing)
            sample_array.append(timing)
        timing_array.append(np.array(sample_array))

    timing_array = np.array(timing_array)
    timing_array = timing_array.reshape((len(reps), -1))
    
    return timing_array, layer_names

def process_mcu_output_tensors(output_shape: Tuple, output_dtype, tensor_values: Path, num_samples: int):
    """Converts a list of output tensors (raw UART string data) to a pandas DataFrame.
    """
    assert tensor_values.exists(), f"Path to tensor_values file does not exist: {tensor_values}"
    input_data = np.load(tensor_values)

    # set first dimension of output shape to number of samples
    final_output_shape = (num_samples, *output_shape)
    tensor_values = input_data["c_outputs_1"].reshape(final_output_shape)
    # convert to the finaly data type
    tensor_values = tensor_values.astype(output_dtype)

    return tensor_values


######################## TESTS ########################

def dequantize_output(output_tensor, scale, zero_point, dtype):
    if dtype == np.uint8:
        dequantized_tensor = (output_tensor.astype(np.float32) - zero_point) * scale
    else:  # int8
        dequantized_tensor = (output_tensor.astype(np.float32) - zero_point) * scale
    return dequantized_tensor