from typing import Dict
from pathlib import Path
import numpy as np
import shutil
from shared_scripts.color_print import print_in_color, Color

INPUT_SAMPLES = 5
PROFILE_SAMPLES = 1000

def load_model_and_data(workdir: Path, model_path: Path, input_data: Path, representative_data: Path = None, quantize: bool = False):
    """Loads the tflite model and the input data.
    
    Also checks if the input data is quantized and quantizes it if necessary.
    Then tests the model on the input data using the tflite interpreter.
    This test is intended to be checked against the results of the framework.
    If the framework supports quantisation, a representive data set is used for calibration.
    
    Args:
        workdir (Path): path to working directory
        input_data (Path): path to the input data's directory.
            Individual tensors are expected to be in .bin format.
        representative_tensors (Path): path to the representative data set's directory.
        tflite_model_path (Path): path to the tflite model
        quantize (bool): whether to quantize the model or not
    """
    step_output = dict()

    # first exract model details to properly load the input data 
    # (check shape and dtype depency against model)
    load_model(model_path, step_output, workdir)

    # load input data including calibration data if model will be quantized
    input_tensors = load_data(input_data, step_output['input_shape'])

    num_samples = input_tensors.shape[0]
    if num_samples > INPUT_SAMPLES:
        print_in_color(Color.YELLOW, f"Note: Found {num_samples} samples in input_tensors, but limiting sample size to {INPUT_SAMPLES} for simplicity!")
        input_tensors = input_tensors[:INPUT_SAMPLES,...]
        num_samples = INPUT_SAMPLES
    step_output['num_samples'] = num_samples
    # Note: step_output['input_tensors'] is set in quant_data_and_test_tflite depending on quantization of the model

    if quantize:
        representative_tensors = load_data(representative_data, step_output['input_shape'])
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
    
    # next load the model again and test it on the input data
    if model_path.suffix == '.tflite':
        quant_data_and_test_tflite(model_path, input_tensors, step_output)
    elif model_path.suffix == '.onnx':
        raise NotImplementedError("test_onnx functionality is not implemented yet")

    return step_output

def load_model(model: Path, step_output: Dict, workdir: Path):
    """Loads the model using tflite runtime (or onnx).

    Args:
        model (Path): ML model file
        workdir (Path): Path to working directory
    """
    
    # Copy model to workdir & create a generic model name
    copied_model = workdir / Path("model" + model.suffix)
    shutil.copy(model, copied_model)
    step_output['model'] = str(copied_model)

    if model.name.endswith('tflite'):
        load_tflite(step_output, copied_model)
    elif model.name.endswith('onnx'):
        load_onnx(step_output, copied_model)
    return step_output

def load_tflite(step_output: Dict, model: Path):
    """Extracts I/O details from tflite model.

    Keys that are added to step_output from input / output details:
        name, dtype, shape
    """
    import tensorflow as tf
    interpreter = tf.lite.Interpreter(model_path=str(model))
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    step_output['input_name'] = input_details[0]['name']
    step_output['input_dtype'] = input_details[0]['dtype']
    step_output['input_shape'] = input_details[0]['shape']

    step_output['output_name'] = output_details[0]['name']
    step_output['output_dtype'] = output_details[0]['dtype']
    step_output['output_shape'] = output_details[0]['shape']

def load_onnx(step_output: Dict, model: Path):
    raise NotImplementedError("load_onnx functionality is not implemented yet")

def load_data(input_data: Path, data_shape: tuple):
    """Either loads the input data from a directory of binary files,
    or loads a single npz file containing the input data at key "input_tensors".

    Args:
        input_data (Path): path to the input data's directory or npz file.
        data_shape (tuple): shape of the input data (model input shape)
    Returns:
        np.array: numpy array with float32 dtype
    """
    if input_data.suffix == ".npz":
        input_data = np.load(input_data)
        input_tensors = input_data['input_tensors']
        return input_tensors
    elif input_data.is_dir():
        input_tensors = floatBin2np(input_data, data_shape)
        return input_tensors
    else:
        raise ValueError(f"Invalid data type for input data {input_data}: .npz array or directory of binary files required!")

def floatBin2np(bin_files: Path, tensor_shape: tuple):
    """Converts a flaot type binary files in a directory to a numpy array

    Args:
        bin_files (Path): path to binary files' directory

    Returns:
        np.array: numpy array with float32 dtype
    """
    from os import listdir
    binary_files = listdir(bin_files)
    out_data = []

    binary_files.sort()
    for bin_file in binary_files:
        print(bin_file)
        file_name = bin_files / Path(bin_file)
        with open(file_name, 'rb') as file:
            data = np.frombuffer(file.read(), dtype=np.float32)
            data = data.reshape(tensor_shape[1:])
            out_data.append(data)

    out_data = np.array(out_data)
    
    return out_data

def quant_data_and_test_tflite(tflite_model_path: Path, input_data: np.array, step_output: Dict):
    """Runs the model on the input tensors

    Args:
        tflite_model_path (Path): path to tflite model file
        input_tensors (np.array): input tensors
    """
    import tensorflow as tf
    # Load the TFLite model
    interpreter = tf.lite.Interpreter(model_path=str(tflite_model_path))
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    if is_model_quantized(input_details[0]):
        (input_scale, input_zero_point, input_dtype), (output_scale, output_zero_point, output_dtype) = extract_quantization_details(interpreter)
        if is_data_quantized(input_data):
            processed_input_data = input_data
        else:
            processed_input_data = quantize_input_data(input_data, input_scale, input_zero_point, input_dtype)
    else:
        processed_input_data = input_data

    step_output["input_tensors"] = processed_input_data
    reference_output = []

    # Perform inference
    for i, tensor in enumerate(processed_input_data):
        input_tensor_index = input_details[0]['index']
        expanded_tensor = tensor[np.newaxis, :]
        interpreter.set_tensor(input_tensor_index, expanded_tensor)
        
        interpreter.invoke()
        
        output_tensor_index = output_details[0]['index']
        output_data = interpreter.get_tensor(output_tensor_index)
        if is_model_quantized(input_details[0]):
            # ToDo: activate again
            #dequantized_output = dequantize_output(output_data, output_scale, output_zero_point)
            dequantized_output = output_data
        else:
            dequantized_output = output_data

        reference_output.append(dequantized_output)
        # max_index = np.argmax(dequantized_output[0])
        # max_value = dequantized_output[0][max_index]
        # print(f"value is {max_value}, index is {max_index}")
    step_output['reference_output'] = reference_output

def is_model_quantized(details):
    if details["dtype"] == np.float32:
        return False
    else:
        return True
    
def is_data_quantized(tensor):
    if np.issubdtype(tensor.dtype, np.integer):
        if np.issubdtype(tensor.dtype, np.uint8):
            return True
        elif np.issubdtype(tensor.dtype, np.int8):
            return True
        else:
            return "Unknown quantized format"
    elif np.issubdtype(tensor.dtype, np.floating):
        return False
    else:
        raise ValueError("Unknown data type")

def extract_quantization_details(interpreter):

    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]

    input_scale, input_zero_point = input_details['quantization']
    output_scale, output_zero_point = output_details['quantization']
    input_dtype = input_details['dtype']
    output_dtype = output_details['dtype']
    return (input_scale, input_zero_point, input_dtype), (output_scale, output_zero_point, output_dtype)

def quantize_input_data(input_tensor, scale, zero_point, dtype):
    if dtype == np.uint8:
        quantized_tensor = np.round(input_tensor / scale + zero_point)
        quantized_tensor = np.clip(quantized_tensor, 0, 255).astype(np.uint8)
    else:  # int8
        quantized_tensor = np.round(input_tensor / scale + zero_point)
        quantized_tensor = np.clip(quantized_tensor, -128, 127).astype(np.int8)
    return quantized_tensor

def dequantize_output(output_tensor, scale, zero_point):
    return (output_tensor.astype(np.float32) - zero_point) * scale

