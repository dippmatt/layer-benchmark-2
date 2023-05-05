import argparse
import os
import tensorflow as tf
import numpy as np
import serial

from O1_gen_bin_file_path_list import gen_tensor_list_file
from O2_profile_model import profile
from O3_compile_model import compile
from O4_build_compile_C import build_cube_prj
from O5_flash_mcu import flash_mcu
from O6_readback import get_uart, readback
from O7_process_result import get_layer_inference_time

def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-quantize', dest='quantize', action='store_true',
                        help='Defines wether the model should be quantized.')
    parser.add_argument('-glow_compiler', dest='glow_compiler', type=str,
                        help='Path to glow compiler executable.', default=None)
    parser.add_argument('-glow_profiler', dest='glow_profiler', type=str,
                        help='Path to glow profiler executable.', default=None)
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

    if not os.path.exists(args.glow_profiler):
        eprint(f"Glow model profiler executable {args.glow_profiler} not found!")
        return -1

    if not os.path.exists(args.glow_compiler):
        eprint(f"Glow compiler executable {args.glow_compiler} not found!")
        return -1
    
    if not os.path.exists(args.input_tensors):
        eprint(f"No .npz array at location {args.input_tensors} not found!")
        return -1

    if input_dtype in [np.float16, np.float32, np.float64, np.float128] and args.quantize:
        create_profile = True
    else:
        create_profile = False

    # Compile model
    if create_profile:
        # Get list of all input tensors for quantisation    
        if not args.input_tensors.endswith('.npz'):
            eprint(f"Invalid data type for input tensors {args.input_tensors}: .npz array required!")
            return -1
        input_data = np.load(args.input_tensors)
        input_tensors = input_data['input_tensors']

        input_tensors_list = gen_tensor_list_file(input_tensors, args.workdir)

        # Profile model
        model_profile = profile(args.glow_profiler, input_tensors_list, copied_model, input_name, args.workdir)
        bundle_dir = compile(args.glow_compiler, copied_model, create_profile, args.workdir, model_profile=model_profile)
    else:
        bundle_dir = compile(args.glow_compiler, copied_model, create_profile, args.workdir, model_profile=None)

    # Build & Compile C Project
    elf_file = build_cube_prj(args.cube_template, args.workdir, bundle_dir)
    print(elf_file)

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
    
    # Flash MCU
    assert flash_mcu(args.cube_programmer, elf_file) == 0, "Flashing STM32 MCU encountered an error."

    # Read back uart output
    lines = readback(ser)

    # extract layer names from log and associate runtimes
    layer_runtimes = get_layer_inference_time(args.workdir, lines)
    for layer in layer_runtimes:
        print(layer["id"], layer["name"], layer["time"])
    return

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if __name__ == '__main__':
    import sys
    sys.exit(_main())
