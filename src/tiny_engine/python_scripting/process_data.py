from shared_scripts.color_print import print_in_color, Color
from typing import Tuple
import numpy as np
import pandas as pd

def process_data(repetitions: int, num_samples: int, output_shape: Tuple, output_dtype, reference_output: list, tensor_values: list, reps: list, reps_no_ir: list):
    """Processes benchmark data from the STM32 MCU and saves it to a file.
    """
    step_output = dict()

    mcu_tensor_values = process_mcu_output_tensors(output_shape, output_dtype, tensor_values)
    step_output["mcu_tensor_values"] = mcu_tensor_values
    
    # ref_tensor_values_df = out_tensors_to_df(reference_output)
    #step_output["ref_tensor_values_df"] = ref_tensor_values_df
    ref_tensor_values = np.array(reference_output)
    step_output["ref_tensor_values"] = ref_tensor_values

    # process per layer timings
    per_layer_timings_mean , per_layer_timings_std_dev = process_layer_timings(reps, num_samples, num_reps=repetitions)
    
    # process reference total inference time
    all_layers_timings_mean, all_layers_timings_std_dev = process_layer_timings_ref(reps_no_ir, num_samples, num_reps=repetitions)

    step_output["per_layer_timings_mean"] = per_layer_timings_mean
    step_output["per_layer_timings_std_dev"] = per_layer_timings_std_dev
    step_output["all_layers_timings_mean"] = all_layers_timings_mean
    step_output["all_layers_timings_std_dev"] = all_layers_timings_std_dev

    return step_output

    # reps shape should be (num_reps, num_outputs)
    print(reps.shape)
    for rep in reps:
        print(len(rep))
    ref_tensor_values_df = out_tensors_to_df(reference_output)
    step_output["ref_tensor_values_df"] = ref_tensor_values_df
    print_in_color(Color.GREEN, "Testing reference data processing for tensor values")
    print(ref_tensor_values_df)

    ################################    
    
    return step_output
    ################################

    print_in_color(Color.GREEN, "Testing data processing for reps_no_ir")
    for rep in reps_no_ir:
        print(rep)
    
    step_output["return_code"] = 0
    return step_output

def process_layer_timings_ref(reps, num_samples, num_reps):

    timings_reps = []
    for line in reps:
        timing = line.split('+')[1]
        timing = timing.strip(' ')
        # convert to int and then to ms from µs
        timings_reps.append(int(timing.strip('µs')) / 1000)

    timings_reps = np.array(timings_reps)
    mean = np.mean(timings_reps, axis=(0))
    std_dev = np.std(timings_reps, axis=(0))
    return mean, std_dev

def process_layer_timings(reps, num_samples, num_reps):
    timings_reps = get_uart_timing_list_in_ms(reps)

    # convert measurements into array of shape:
    # (num_samples, num_reps, num_layers)
    # num_samples: number of unique input tensors, used for inference
    # num_reps: number of inferences (repetitions) for each input tensor
    # num_layers: number of layers in the model, each layer has it's inference time measurement
    # 
    # Then calculates the average over all repetitions and all samples, 
    # so that only a vector of length num_layers is left.
    
    # create array-like list of lists for all measurements
    timing_array = []
    for i in range(num_samples):
        sample_array = []
        for j in range(num_reps):
            # append dummy value
            sample_array.append(0)
        timing_array.append(sample_array)

    # fill array
    for i, timings in enumerate(timings_reps):
        sample_index = i // num_reps
        rep_index = i % num_reps
        timing_array[sample_index][rep_index] = timings
    timing_array = np.array(timing_array)

    # now that we have an np array with shape (num_samples, num_reps, num_layers),
    # we want to average over all samples and repetitions, to generate an array of shape (num_layers)
    mean = np.mean(timing_array, axis=(0, 1))
    std_dev = np.std(timing_array, axis=(0, 1))
    return mean, std_dev

def get_uart_timing_list_in_ms(uart_result_reps):
    ################## Example Response from UART Serial  ###################

    # Profiling "MAIN loop timing" sequence: 
    # --Event-----------------------|--timestamp--|----delta_t---
    # BEGIN                         :        0 µs | +        0 µs
    # START                         :        2 µs | +        2 µs
    # STOP                          :    14570 µs | +    14568 µs
    # START                         :    14571 µs | +        1 µs
    # STOP                          :    23141 µs | +     8570 µs
    # START                         :    23143 µs | +        2 µs
    # STOP                          :    33860 µs | +    10717 µs
    # START                         :    33861 µs | +        1 µs
    # STOP                          :    42431 µs | +     8570 µs
    # START                         :    42433 µs | +        2 µs
    # STOP                          :    53150 µs | +    10717 µs
    # START                         :    53151 µs | +        1 µs
    # STOP                          :    61721 µs | +     8570 µs
    # START                         :    61723 µs | +        2 µs
    # STOP                          :    72440 µs | +    10717 µs
    # START                         :    72441 µs | +        1 µs
    # STOP                          :    81011 µs | +     8570 µs
    # START                         :    81013 µs | +        2 µs
    # STOP                          :    91730 µs | +    10717 µs
    # START                         :    91731 µs | +        1 µs
    # STOP                          :    92018 µs | +      287 µs
    # START                         :    92019 µs | +        1 µs
    # STOP                          :    92049 µs | +       30 µs
    # START                         :    92049 µs | +        0 µs
    # STOP                          :    92060 µs | +       11 µs
    # END                           :    92060 µs | +        0 µs
    
    timings_reps = []
    for uart_result in uart_result_reps:
        timings = []
        for line in uart_result:
            if "STOP" in line:
                timing = line.split('+')[1]
                timing = timing.strip(' ')
                # convert to int and then to ms from µs
                timings.append(int(timing.strip('µs')) / 1000)
        timings_reps.append(timings)
    return timings_reps

def process_mcu_output_tensors(output_shape: Tuple, output_dtype, tensor_values: list):
    """Converts a list of output tensors (raw UART string data) to a pandas np array.
    """
    for i, tensor_value in enumerate(tensor_values):
        # remove trailing whitespace
        tensor_value = tensor_value.rstrip(' ')
        tensor_value = tensor_value.split(' ')
        if "int" in str(output_dtype):
            tensor_value = [int(x) for x in tensor_value]
        elif "float" in str(output_dtype):
            tensor_value = [float(x) for x in tensor_value]
        else:
            print("Tensor value has wrong data type. Can only convert to int or float.")
        tensor_value = np.array(tensor_value).reshape(output_shape)
        tensor_values[i] = tensor_value

    tensor_values = np.array(tensor_values)
    return tensor_values




def out_tensors_to_df(tensor_values):
    """Converts a list of output tensors to a pandas DataFrame.
    """
    # Create a list of column names
    column_names = [f"output_{i+1}" for i in range(len(tensor_values))]

    # Create a list of dictionaries where each dictionary corresponds to an output tensor
    data = [{column_names[i]: value} for i, value in enumerate(tensor_values)]
    print(data)

    # Create a pandas DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame
    print(df.columns)
    print()
    print(df)
    import sys; sys.exit()
    return df

######################## TESTS ########################

def dequantize_output(output_tensor, scale, zero_point, dtype):
    if dtype == np.uint8:
        dequantized_tensor = (output_tensor.astype(np.float32) - zero_point) * scale
    else:  # int8
        dequantized_tensor = (output_tensor.astype(np.float32) - zero_point) * scale
    return dequantized_tensor