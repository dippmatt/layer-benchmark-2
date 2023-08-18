import sys
import argparse
from pathlib import Path

shared_scripts_path = Path.cwd() / Path('..', '..', 'shared_scripts').resolve()
sys.path.append(str(shared_scripts_path))

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
# copy input files, fill templates, build, compile...
from copy_build_compile import copy_build_compile

# flash and UART readback methods
from flash_and_readback import flash_and_readback

# process and store data
from process_data import process_data

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
    parser.add_argument('-representative_tensors', dest='representative_tensors', type=str,
                        help='Path to one .npz file. \
                            Numpy binary array file represents list of input tensor examples, used to calibrate quantization if needed. \
                            Minimum of 10 tensors required.', default=None)
    parser.add_argument('-dat_bin_folder', dest='dat_bin_folder', type=str,
                        help='Path to a folder containing binary input tensors for inference. Only .bin files are read.', default=None)
    parser.add_argument('-cube_template', dest='cube_template', type=str,
                        help='Path to the STM Cube IDE template project, where the compiled model source files are copied to.', default=None)
    parser.add_argument('-cube_template_ref', dest='cube_template_ref', type=str,
                        help='Path to the STM Cube IDE reference template project, used as error estimation of layer measurements.', default=None)
    parser.add_argument('-cube_template_empty', dest='cube_template_empty', type=str,
                        help='Path to the empty STM Cube IDE template project, used to extract RAM & FLASH usage.', default=None)
    parser.add_argument('-out_dir', dest='out_dir', type=str,
                        help='Path to the results as csv.', default=None)
    args = parser.parse_args()


    
    pipeline = Pipeline(args, validate_args)

    # 0. keys added in load_test_tensors step:
    # num_samples: int, number of samples in input_tensors
    # input_tensors, np.array, shape: (num_samples, *input_shape), dtype: input_dtype
    # num_representative_samples: int, number of samples in representative_tensors, None if not quantized
    # representative_tensors, np.array, shape: (num_representative_samples, *input_shape), dtype: input_dtype, None if not quantized
    step_requirements = [{'main_arg': 'input_tensors'},
                         {'main_arg': 'representative_tensors'},
                         {'main_arg': 'quantize'}]
    pipeline.add_step(load_test_tensors, step_requirements)
    

    # 1. keys added in load_model step:
    # model: str, path to model file in workdir
    # input_name: str, first layer name of model
    # input_dtype: np.dtype, dtype of input tensor
    # input_shape: tuple, shape of input tensor
    # output_name: str, last layer name of model
    # output_dtype: np.dtype, dtype of output tensor
    # output_shape: tuple, shape of output tensor
    step_requirements = [{'main_arg': 'model'},
                         {'main_arg': 'workdir'}]
    pipeline.add_step(load_model, step_requirements)


    # 2. keys added in load_cube_project step:
    # cube_template: Path, path to cube template project used for per layer measurements
    # cube_template_no_ir: Path path to project used for error estimation (measures whole model)
    # cube_template_ref: Path, projet with inference framework, used for flash and ram estimation
    # cube_template_empty: Path, empty project, used for flash and ram estimation
    step_requirements = [{'main_arg': 'workdir'},
                         {'main_arg': 'cube_template'},
                         {'main_arg': 'cube_template_ref'},
                         {'main_arg': 'cube_template_empty'}]
    pipeline.add_step(load_cube_project, step_requirements)


    # 3. keys added in get_mcu_dev step:
    # serial: serial.Serial, serial connection to MCU
    step_requirements = [{'main_arg': 'cube_programmer'}]
    pipeline.add_step(get_mcu_dev, step_requirements)


    # 4. no keys added in validate_data step.
    # verifies that input tensors are valid for model
    step_requirements = [{'step': 0, 'name': 'input_tensors'},
                         {'step': 1, 'name': 'input_dtype'},
                         {'step': 1, 'name': 'input_shape'},
                         {'main_arg': 'quantize'}]
    pipeline.add_step(validate_data, step_requirements)


    # 5. keys added in use_framework step:
    # bundle_dir: Path, path to compiled model with IR
    # bundle_dir_no_ir: Path, path to compiled model without IR
    step_requirements = [{'main_arg': 'quantize'},
                         {'main_arg': 'workdir'},
                         {'main_arg': 'glow_compiler'},
                         {'main_arg': 'glow_profiler'},
                         {'main_arg': 'nxp'},
                         {'step': 1, 'name': 'input_name'},
                         {'step': 0, 'name': 'representative_tensors'},
                         {'step': 1, 'name': 'model'}]
    pipeline.add_step(use_framework, step_requirements)


    # 6. keys added in copy_build_compile step:
    # cube_templates (all): Path, path to elf file for respective template
    # ram: int, estimated ram usage of model
    # flash: int, estimated flash usage of model
    step_requirements = [{'main_arg': 'workdir'},
                         {'main_arg': 'repetitions'},
                         {'step': 0, 'name': 'input_tensors'},
                         {'step': 1, 'name': 'input_dtype'},
                         {'step': 2, 'name': 'cube_template'},
                         {'step': 2, 'name': 'cube_template_no_ir'},
                         {'step': 2, 'name': 'cube_template_ref'},
                         {'step': 2, 'name': 'cube_template_empty'},
                         {'step': 5, 'name': 'bundle_dir'},
                         {'step': 5, 'name': 'bundle_dir_no_ir'}]
    pipeline.add_step(copy_build_compile, step_requirements)


    # 7. keys added in flash_and_readback step:
    # tensor_values: list. Model output in either float or int8 format, depending on quantization
    # reps: list of list. first dimenion: repetitions, second dimension: layer measurements
    # reps_no_ir: list. Layer measurements of model without IR
    step_requirements = [{'main_arg': 'cube_programmer'},
                         {'step': 3, 'name': 'serial'},
                         {'step': 6, 'name': 'cube_template'},
                         {'step': 6, 'name': 'cube_template_no_ir'}]
    pipeline.add_step(flash_and_readback, step_requirements)


    # 8. keys added in process_data step:

    step_requirements = [{'step': 7, 'name': 'tensor_values'},
                         {'step': 7, 'name': 'reps'},
                         {'step': 7, 'name': 'reps_no_ir'}]
    pipeline.add_step(process_data, step_requirements)

    pipeline.run()
    print()
    print(pipeline.steps[-1].output)

    # from assemble_project import assemble_project
    # from flash_mcu import flash_mcu
    # from uart_readback import uart_readback
    # from store_data import store_data


if __name__ == '__main__':
    import sys
    sys.exit(_main())
