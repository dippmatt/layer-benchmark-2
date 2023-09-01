from shared_scripts.color_print import print_in_color, Color
from typing import Tuple
import numpy as np
import pandas as pd

def process_data(reference_output: list, output_shape: Tuple, output_dtype,  tensor_values: list, reps: list, reps_no_ir: list):
    """Processes benchmark data from the STM32 MCU and saves it to a file.
    """
    step_output = dict()

    ########## CONVERT TENSOR VALUES TO NUMPY ARRAYS ##########
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
        
    mcu_tensor_values_df = out_tensors_to_df(tensor_values)    
    step_output["mcu_tensor_values_df"] = mcu_tensor_values_df
    print_in_color(Color.GREEN, "Testing MCU data processing for tensor values")
    print(mcu_tensor_values_df)

    print()
    element = mcu_tensor_values_df.at[1, "output_3"]
    print(element)
    print()
    
    ref_tensor_values_df = out_tensors_to_df(reference_output)
    step_output["ref_tensor_values_df"] = ref_tensor_values_df
    print_in_color(Color.GREEN, "Testing reference data processing for tensor values")
    print(ref_tensor_values_df)


    print_in_color(Color.GREEN, "Testing data processing for reps")
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


    



######################## TESTS ########################

def out_tensors_to_df(tensor_values):
    """Converts a list of output tensors to a pandas DataFrame.
    """
    # Create a list of column names
    column_names = [f"output_{i+1}" for i in range(len(tensor_values))]

    # Create a list of dictionaries where each dictionary corresponds to an output tensor
    data = [{column_names[i]: value for i, value in enumerate(tensor)} for tensor in tensor_values]

    # Create a pandas DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame
    return df

def dequantize_output(output_tensor, scale, zero_point, dtype):
    if dtype == np.uint8:
        dequantized_tensor = (output_tensor.astype(np.float32) - zero_point) * scale
    else:  # int8
        dequantized_tensor = (output_tensor.astype(np.float32) - zero_point) * scale
    return dequantized_tensor