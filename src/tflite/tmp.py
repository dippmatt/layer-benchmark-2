import numpy as np

tensor_values = "workdir/data.npz"
input_data = np.load(tensor_values)
tensor_values_quant = "workdir/data_quant.npz"
input_data_quant = np.load(tensor_values_quant)

# set first dimension of output shape to number of samples

tensor_values = input_data.keys()

for key in tensor_values:
	print(key)
	
np_arr = input_data["input_tensors"]
np_arr_quant = input_data_quant["input_tensors"]
print("data.npz")
print(np_arr.shape)
print(np_arr.dtype)
print("data_quant.npz")
print(np_arr_quant.shape)
print(np_arr_quant.dtype)
