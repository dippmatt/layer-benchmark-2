import os

def gen_tensor_list_file(np_array, workdir):
    out_file_name = 'inputtensors.txt'

    tensor_bin_file_dir = os.path.join(workdir, 'bin_files')
    os.system(f"mkdir -p {tensor_bin_file_dir}")

    filenames = []
    for i in range(np_array.shape[0]):
        output_file = os.path.join(tensor_bin_file_dir, f'{i}.bin')
        filenames.append(output_file)
        np_array[i].tofile(output_file)

    with open(os.path.join(workdir, out_file_name), 'w') as outfile:
        for filename in filenames:
            outfile.write(filename + '\n')

    print()
    print(f"List of all files written to ", os.path.join(workdir, out_file_name))
    return os.path.join(workdir, out_file_name)
