import os
import numpy as np
import argparse


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-name', dest='name', type=str,
                        help='Name of the output file. Default: "<dtype>.npz"', default="")
    parser.add_argument('-dtype', dest='dtype', type=str,
                        help='Data type of the input. Currently supported: int8, uint8, float32 \
                            Extend to your need in lines 24 - ', default=None)
    parser.add_argument('-out_dir', dest='out_dir', type=str,
                        help='Path to store the npz file.', default=None)
    parser.add_argument('-bin_dir', dest='bin_dir', type=str,
                        help='Path to folder with binary model input files.', default=None)
    parser.add_argument('-bin_files',  dest='bin_files', nargs='+', 
                        help='List of binary model input files', default=None)
    args = parser.parse_args()

    assert args.dtype is not None
    assert args.bin_dir is not None or args.bin_files is not None, "\
        Must specify either folder of input files, \
        or provide list of input files."
    assert args.out_dir is not None and os.path.isdir(args.out_dir)
    
    dtype = None
    if args.dtype == 'int8':
        dtype = np.int8
    elif args.dtype == 'uint8':
        dtype = np.uint8
    elif args.dtype == 'float32':
        dtype = np.float32
    else:
        raise ValueError(f"Unsupproted numpy input data type {args.dtype}. \
                         Extend data type parsing on your own here, if you want more data types.")

    if args.name == "":
        out_file = os.path.join(args.out_dir, f"{args.dtype}.npz")
    else:
        out_file = os.path.join(args.out_dir, f"{args.name}")

    input_files = []
    input_tensors = []


    # Iterate through all the .bin files in the input directory
    if args.bin_dir is not None and os.path.isdir(args.bin_dir):
        for filename in os.listdir(args.bin_dir):
            if filename.endswith('.bin'):
                file = os.path.join(args.bin_dir, filename)
                input_files.append(file)
    else:
        for filename in args.bin_files:
            if filename.endswith('.bin'):
                input_files.append(file)

    input_files = sorted(input_files, key=lambda x: os.path.basename(x))
    for filename in input_files:
            if filename.endswith('.bin'):
                # Load the binary file and append it to the input_tensors list
                print("Appending file: ", filename)
                input_tensor = np.fromfile(filename, dtype=dtype)
                input_tensors.append(input_tensor)
    # Convert the input_tensors list to a numpy array
    input_tensors = np.array(input_tensors)

    # Save the input_tensors numpy array to a .npz file
    np.savez(out_file, input_tensors=input_tensors)
    print(f"Wrote npz file to {out_file}.")

if __name__ == '__main__':
    import sys
    sys.exit(_main())