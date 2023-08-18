import numpy as np

def validate_data(input_tensors, model_input_dtype, model_input_shape):

    data_input_shape = (1, * input_tensors.shape[1:])
    model_input_shape = tuple(model_input_shape)

    assert data_input_shape == model_input_shape, f"Model input shape {model_input_shape} does not match data shape {data_input_shape}."
    assert input_tensors.dtype == model_input_dtype, f"Model input dtype {model_input_dtype} does not match data dtype {input_tensors.dtype}."
    return dict()