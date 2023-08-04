from typing import Dict
from pathlib import Path
import numpy as np
import shutil

def load_model(model: Path, workdir: Path):
    """Loads the model using tflite runtime (or onnx).

    Args:
        model (Path): ML model file
        workdir (Path): Path to working directory
    """
    step_output = dict()
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
    import tensorflow as tf
    interpreter = tf.lite.Interpreter(model_path=str(model))
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Test model on some input data.
    step_output['input_name'] = input_details[0]['name']
    step_output['input_dtype'] = input_details[0]['dtype']
    step_output['input_shape'] = input_details[0]['shape']

    step_output['output_name'] = output_details[0]['name']
    step_output['output_dtype'] = output_details[0]['dtype']
    step_output['output_shape'] = output_details[0]['shape']

def load_onnx(step_output: Dict, model: Path):
    raise NotImplementedError("load_onnx functionality is not implemented yet")