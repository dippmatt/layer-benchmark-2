import numpy as np

def validate_data(input_tensors, model_input_dtype, model_input_shape, quantize: bool):

    data_input_shape = (1, * input_tensors.shape[1:])
    model_input_shape = tuple(model_input_shape)

    if quantize:
        assert input_tensors.dtype in [np.float16, np.float32, np.float64, np.float128], 'Cannot quantize & profile with glow when input data is already quantized.'
    assert data_input_shape == model_input_shape, f"Model input shape {model_input_shape} does not match data shape {data_input_shape}."
    assert input_tensors.dtype == model_input_dtype, f"Model input dtype {model_input_dtype} does not match data dtype {input_tensors.dtype}."
    return dict()