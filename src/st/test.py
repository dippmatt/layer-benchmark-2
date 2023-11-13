import sys
from pathlib import Path
import numpy as np

data_fp = Path("workdir", "data.npz")
data_int = Path("workdir", "data_validate.npz")

input_data = np.load(data_fp)
input_tensors = input_data['input_tensors']
print(data_fp)
print(input_tensors.dtype)
print(input_tensors.shape)
print()

input_data = np.load(data_int)
input_tensors = input_data['input_tensors']
print(data_int)
print(input_tensors.dtype)
print(input_tensors.shape)
print()
