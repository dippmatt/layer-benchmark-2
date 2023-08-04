import argparse
from pathlib import Path
import multiprocessing
import tensorflow as tf
import numpy as np
import serial
import csv

# class to manage pipelined benchmarking flow 
# it executes each of the flollowing mehtods 
# one after another and checks for successful execution
from benchmark_pipeline import Pipeline

# keep it simple here one return value: true or false. 
# Cecks if args are valid to use
from validate_args import validate_args

# now all methods to load data

# get test tensors from npz file. extract data type and shape. 
# Return info as dict.
from load_test_tensors import load_test_tensors
# make it agnostic to ML graph framework (tflite / onnx,..). 
# Extract IO data of model and return dict with data
from load_model import load_model
# load templates for layer timings, 
# reference timings and empty template for flash / ram estimation
from load_cube_project import load_cube_project
# get mcu info
from get_mcu_dev import get_mcu_dev

# validate model IO data types, shapes,.. 
# against test tensors, framework settings,...
from validate_data import validate_data

# use framework with all parsed settings
from use_framework import use_framework

# assemble compilable cube project: 
# copy files, create files from templates,...
from python_scripting.copy_build_compile import copy_build_compile

# flash and UART readback methods
from flash_mcu import flash_mcu
from uart_readback import uart_readback

# process and store data
from store_data import store_data

MAX_SAMPLES = 10

def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-quantize', dest='quantize', action='store_true',
                        help='Defines wether the model should be quantized.')
    parser.add_argument('-nxp', dest='nxp', action='store_true',
                        help='Defines wether the model compiler is from NXP or the open source one.\
                            NXP\'s model compiler can use the CMSIS library from ARM, which results in improved performance.')
    parser.add_argument('-glow_compiler', dest='glow_compiler', type=str,
                        help='Path to glow compiler executable.', default=None)
    parser.add_argument('-glow_profiler', dest='glow_profiler', type=str,
                        help='Path to glow profiler executable.', default=None)
    parser.add_argument('-repetitions', dest='repetitions', type=int,
                        help='The number of repetitions each input tensor propagated through the model..', default=1)
    parser.add_argument('-model', dest='model', type=str,
                        help='Path to tflite input model.', default=None)
    parser.add_argument('-cube_programmer', dest='cube_programmer', type=str,
                        help='Path STM 32 Cube Cube Programmer executable. \
                            Usually found at /usr/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI.', 
                            default="/usr/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI")
    parser.add_argument('-workdir', dest='workdir', type=str,
                        help='Path where generated temporary files can be stored. \
                            After model generation is done, model C files are stored at <workdir>/build.', default=None)
    parser.add_argument('-input_tensors', dest='input_tensors', type=str,
                        help='Path to one .npz file. \
                            Numpy binary array file represents list of input tensor examples, used for quantising the model. \
                            Minimum of 10 tensors required.', default=None)
    parser.add_argument('-dat_bin_folder', dest='dat_bin_folder', type=str,
                        help='Path to a folder containing binary input tensors for inference. Only .bin files are read.', default=None)
    parser.add_argument('-cube_template', dest='cube_template', type=str,
                        help='Path to the STM Cube IDE template project, where the compiled model source files are copied to.', default=None)
    parser.add_argument('-out_dir', dest='out_dir', type=str,
                        help='Path to the results as csv.', default=None)
    args = parser.parse_args()

    
    
    # Check file paths
    if not os.path.exists(args.workdir):
        eprint(f"Working directory path {args.workdir} does not exist!")
        return -1
    else:
        assert os.path.isdir(args.workdir)
        args.workdir = os.path.abspath(args.workdir)
        # clean workdir
        assert os.system(f"rm -rf {args.workdir}/*") == 0

    assert os.path.isdir(args.out_dir), "Must specify valid directory to write results to."

    if not os.path.exists(args.cube_template):
        eprint(f"Did not find path to STM Cube IDE template project: {args.cube_template}")
        return -1
    else:
        inc_dir = os.path.join(args.cube_template, "Core", "Inc")
        src_dir = os.path.join(args.cube_template, "Core", "Src")
        assert os.path.exists(inc_dir),"Unexpected project structure in STM Cube IDE template project."
        assert os.path.exists(src_dir), "Unexpected project structure in STM Cube IDE template project."

    if not os.path.exists(args.model):
        eprint(f"Working directory path {args.model} does not exist!")
        return -1
    else:
        # Copy model to workdir & create a generic model name
        copied_model = os.path.join(args.workdir, "model.tflite")
        assert os.system(f"cp {args.model} {copied_model}") == 0

        # Load the TFLite model and allocate tensors.
        interpreter = tf.lite.Interpreter(model_path=copied_model)
        interpreter.allocate_tensors()

        # Get input and output tensors.
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # Test model on some input data.
        input_name = input_details[0]['name']
        input_dtype = input_details[0]['dtype']
        input_shape = input_details[0]['shape']

        output_name = output_details[0]['name']
        output_dtype = output_details[0]['dtype']
        output_shape = output_details[0]['shape']

    if not os.path.exists(args.glow_compiler):
        eprint(f"Glow compiler executable {args.glow_compiler} not found!")
        return -1
    
    if not os.path.exists(args.input_tensors):
        eprint(f"No .npz array at location {args.input_tensors} not found!")
        return -1

    # ToDo move to validate data
    if input_dtype in [np.float16, np.float32, np.float64, np.float128] and args.quantize:
        create_profile = True
        if not os.path.exists(args.glow_profiler):
            eprint(f"Glow model profiler executable {args.glow_profiler} not found!")
            return -1
    else:
        create_profile = False

    # ToDo move to use_framework
    # Get list of all input tensors for quantisation    
    if not args.input_tensors.endswith('.npz'):
        eprint(f"Invalid data type for input tensors {args.input_tensors}: .npz array required!")
        return -1
    input_data = np.load(args.input_tensors)
    print(input_data['input_tensors'].shape)

    input_tensors = input_data['input_tensors']
    # Limit tensor size to 10 for now
    num_samples = input_tensors.shape[0]
    if num_samples > MAX_SAMPLES:
        print_yellow(f"Note: Found {num_samples} in input_tensors, but limiting sample size to {MAX_SAMPLES} for simplicity!")
        input_tensors = input_tensors[:MAX_SAMPLES,...]
        num_samples = MAX_SAMPLES

    # Compile model
    if create_profile:
        input_tensors_list = gen_tensor_list_file(input_tensors, args.workdir)

        # Profile model
        model_profile = profile(args.glow_profiler, input_tensors_list, copied_model, input_name, args.workdir)
        bundle_dir = compile(args.glow_compiler, copied_model, create_profile, args.workdir, args.nxp, model_profile=model_profile)
    else:
        bundle_dir = compile(args.glow_compiler, copied_model, create_profile, args.workdir, args.nxp, model_profile=None)

    # generate input test tensors as C header from npz data
    if input_dtype in [np.float16, np.float32, np.float64, np.float128]:
        io_dtype = 'float'
    else:
        io_dtype = 'int8_t'
    test_tensor_header = gen_test_tensors(input_tensors, io_dtype)

    # ToDo move to copy_build_compile
    # Build & Compile C Project

    # Note already moved to validate_args
    assert args.repetitions >= 1, f"Cannot set the number of repetitions each input tensor propagated to {args.repetitions}!"
    elf_file = build_cube_prj(args.cube_template, args.repetitions, test_tensor_header, args.workdir, bundle_dir, build_ref=False)

    # Build reference project without individual layer timings to error estimation of measurements
    elf_reference_timing = build_cube_prj(args.cube_template_ref_timing, 1, test_tensor_header, args.workdir, bundle_dir, build_ref=True)

    # get uart details
    location, speed, _ = get_uart(args.cube_programmer)
    stm_port = location
    baudrate = speed
    parity = serial.PARITY_NONE
    stopbits = serial.STOPBITS_ONE
    bytesize = serial.EIGHTBITS
    ser = serial.Serial(
        port=stm_port,
        baudrate=baudrate,
        parity=parity,
        stopbits=stopbits,
        bytesize=bytesize)
    
    # Use multiprocessing for readback. 
    # Might miss first few uart transmissions when reading back sequentially after flash.

    # All arguments for methods in 'Process' are passed as 'copy by value',
    # therefore we need a list from manager
    manager = multiprocessing.Manager()
    reps = manager.list()
    readback_args = (ser, reps,)
    flash_args = (args.cube_programmer, elf_file, )

    readback_process = multiprocessing.Process(target=readback, args=readback_args)
    flash_process = multiprocessing.Process(target=flash_mcu, args=flash_args)

    readback_process.start()
    flash_process.start()

    flash_process.join()
    readback_process.join()

    assert readback_process.exitcode == 0, "UART Readback of STM32 MCU encountered an error."
    assert flash_process.exitcode == 0, "Flashing STM32 MCU encountered an error."

    # extract layer names from log and associate runtimes
    # we expect <number of test tensors> x <number of inference repetitions> meausrements
    # the cube template will return measurements in the following order:
    #
    # input1
    #   input1 reptetition1
    #     input1 reptetition1 layer1 runtime
    #     input1 reptetition1 layer2 runtime
    #     ...
    #     input1 reptetition1 layerN runtime
    #   input1 reptetition2
    #   ...
    #   input1 reptetitionN
    # input2
    # ...
    # inputN
    layer_runtimes = get_layer_inference_time(args.workdir, reps, num_samples, args.repetitions)

    model_name = os.path.basename(args.model).rstrip(".tflite")
    keys = set().union(*(d.keys() for d in layer_runtimes))
    csv_file = os.path.join(args.out_dir, f'layer_inference_timings_{model_name}.csv')
    with open(csv_file, mode='w', newline='') as csv_file:
        # Create a CSV writer object
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        # Write the header row
        writer.writeheader()
        # Write the data rows
        for row in layer_runtimes:
            writer.writerow(row)
    

    for layer in layer_runtimes:
        print(layer["id"])
        print(layer["name"])
        print(layer["kind"])
        print(layer["time"], "µs")
        print()

    return 0

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def print_yellow(text):
    os.system(f'echo "\\033[93m{text}\\033[0m"')

if __name__ == '__main__':
    import sys
    sys.exit(_main())
