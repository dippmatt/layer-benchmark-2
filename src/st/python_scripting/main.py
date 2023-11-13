import sys
import argparse
from pathlib import Path

shared_scripts_path = Path.cwd() / Path('..', '..', 'shared_scripts').resolve()
sys.path.append(str(shared_scripts_path))

# class to manage pipelined benchmarking flow 
# it executes each of the flollowing mehtods 
# one after another and checks for successful execution
from shared_scripts.benchmark_pipeline import Pipeline

# keep it simple here, one return value: true or false. 
# Cecks if args are valid to use
from validate_args import validate_args

# now all methods to load data

# copy tinyengine framework to workdir, copy custom_tflite.py to framework,
# run custom_tflite.py to generate model source files
from use_framework import use_framework_compile

# TODO: make it agnostic to ML graph framework (tflite / onnx,..).
# load model and test tensors then test the model
from shared_scripts.load_model_and_data import load_model_and_data
# load templates for layer timings, 
# reference timings and empty template for flash / ram estimation
from load_cube_project import load_cube_project
# get mcu info
from shared_scripts.get_mcu_dev import get_mcu_dev

# validate model IO data types, shapes,.. 
# against test tensors, framework settings,...
from validate_data import validate_data

# assemble compilable cube project: 
# copy input files, fill templates, build, compile...
# from copy_build_compile import copy_build_compile

# flash and UART readback methods
from flash_and_readback import flash_and_readback

# process and store data
from process_data import process_data

# save the results
from shared_scripts.save_results import save_results

def _main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-repetitions', dest='repetitions', type=int,
                        help='The number of repetitions each input tensor propagated through the model..', default=1)
    parser.add_argument('-model', dest='model', type=str,
                        help='Path to tflite input model.', default=None)
    parser.add_argument('-cube_programmer', dest='cube_programmer', type=str,
                        help='Path STM 32 Cube Cube Programmer executable. \
                            Usually found at /usr/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI.', 
                            default="/usr/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI")
    parser.add_argument('-cube_mx', dest='cube_mx', type=str,
                        help='Path STM 32 Cube Cube MX executable. \
                            Usually found at /usr/local/STMicroelectronics/STM32Cube/STM32CubeMX/STM32CubeMX', 
                            default="/usr/local/STMicroelectronics/STM32Cube/STM32CubeMX/STM32CubeMX")
    parser.add_argument('-stm32ai', dest='stm32ai', type=str,
                        help='Path STM 32 stm32ai executable. \
                            Usually found at /home/<user>/STM32Cube/Repository/Packs/STMicroelectronics/X-CUBE-AI/<cube ai version>/Utilities/linux/stm32ai', 
                            default="~/STM32Cube/Repository/Packs/STMicroelectronics/X-CUBE-AI/8.1.0/Utilities/linux/stm32ai")
    parser.add_argument('-workdir', dest='workdir', type=str,
                        help='Path where generated temporary files can be stored. \
                            After model generation is done, model C files are stored at <workdir>/build.', default=None)
    parser.add_argument('-input_tensors', dest='input_tensors', type=str,
                        help='Path to one .npz file. \
                            Numpy binary array file represents list of input tensor examples, used for quantising the model. \
                            Minimum of 10 tensors required.', default=None)
    parser.add_argument('-cube_template', dest='cube_template', type=str,
                        help='Path to the STM Cube IDE template project, where the compiled model source files are copied to.', default=None)
    parser.add_argument('-cube_template_validate', dest='cube_template_validate', type=str,
                        help='Path to the STM Cube IDE reference template project, used validate the project and retirieve C model output tensors.', default=None)
    parser.add_argument('-out_dir', dest='out_dir', type=str,
                        help='Path to the results as csv.', default=None)
    args = parser.parse_args()


    
    pipeline = Pipeline(args, validate_args)

####################################################
    # 0. keys added in load_model_and_data step:
    # num_samples: int, number of samples in input_tensors
    # input_tensors: np.array, shape: (num_samples, *input_shape), dtype: input_dtype
    # num_representative_samples: int, number of samples in representative_tensors, None if not quantized
    # representative_tensors: np.array, shape: (num_representative_samples, *input_shape), dtype: input_dtype, None if not quantized
    # model: str, path to model file in workdir
    # input_name: str, first layer name of model
    # input_dtype: np.dtype, dtype of input tensor
    # input_shape: tuple, shape of input tensor
    # output_name: str, last layer name of model
    # output_dtype: np.dtype, dtype of output tensor
    # output_shape: tuple, shape of output tensor
    # reference_output: list, reference output of the tflite interpreter, shape: (num_samples, *output_shape), dtype: output_dtype
    step_requirements = [{'main_arg': 'workdir'},
                         {'main_arg': 'model'},
                         {'main_arg': 'input_tensors'}]
    pipeline.add_step(load_model_and_data, step_requirements)
    

    # 1. keys added in load_cube_project step:
    # cube_template: Path, path to cube template project used for per layer measurements
    # cube_template_all_layers: Path path to project used for error estimation (measures whole model)
    # cube_template_validate: Path, projet with inference framework, used for output tensor validation
    step_requirements = [{'main_arg': 'workdir'},
                         {'main_arg': 'cube_template'},
                         {'main_arg': 'cube_template_validate'},
                         {'step': 0, 'name': 'model'}]
    pipeline.add_step(load_cube_project, step_requirements)


    # 2. keys added in get_mcu_dev step:
    # serial: serial.Serial, serial connection to MCU
    step_requirements = [{'main_arg': 'cube_programmer'}]
    pipeline.add_step(get_mcu_dev, step_requirements)


    # 3. no keys added in validate_data step.
    # verifies that input tensors are valid for model
    step_requirements = [{'step': 0, 'name': 'input_tensors'},
                         {'step': 0, 'name': 'input_dtype'},
                         {'step': 0, 'name': 'input_shape'}]
    pipeline.add_step(validate_data, step_requirements)


    # 4. keys added in use_framework step:
    # tensor_values: list. Model output in either float or int8 format, depending on quantization
    # cube_template: Path to the elf file of the compiled model
    # cube_template_all_layers: Path to the elf file of the compiled model without per-layer timings 
    # flash: int, total flash size in KB of the model + framework runtime
    # flash_rt: int, flash size framework runtime only in KB
    # ram: int, total ram size in KB of the model + framework runtime
    # ram_rt: int, ram size framework runtime only in KB
    step_requirements = [{'main_arg': 'workdir'},
                         {'main_arg': 'cube_mx'},
                         {'main_arg': 'stm32ai'},
                         {'main_arg': 'repetitions'},
                         {'main_arg': 'cube_programmer'},
                         {'step': 0, 'name': 'model'},
                         {'step': 1, 'name': 'cube_template'},
                         {'step': 1, 'name': 'cube_template_validate'}]
    pipeline.add_step(use_framework_compile, step_requirements)    
   

    # 5. keys added in flash_and_readback step:
    # reps: list of list. first dimenion: repetitions, second dimension: layer measurements
    # reps_all_layers: list. Layer measurements of the whole model
    step_requirements = [{'main_arg': 'cube_programmer'},
                         {'main_arg': 'workdir'},
                         {'step': 2, 'name': 'serial'},
                         {'step': 4, 'name': 'cube_template'},
                         {'step': 4, 'name': 'cube_template_all_layers'}]
    pipeline.add_step(flash_and_readback, step_requirements)


    # 6. keys added in process_data step:
    # mcu_tensor_values: np.array, shape: (num_samples, *output_shape), dtype: depends on quantization
    # ref_tensor_values: np.array, shape: (num_samples, *output_shape), dtype: depends on quantization
    # per_layer_timings_mean: np.array, shape: (num_layers), dtype: float,
    #   mean of per layer timings over all repetitions and samples
    # all_layers_timings_mean: np.array, shape: (num_samples), dtype: float,
    #   mean of total inference time over all repetitions and samples for all layers
    step_requirements = [{'main_arg': 'repetitions'},
                         {'step': 0, 'name': 'num_samples'},
                         {'step': 0, 'name': 'output_shape'},
                         {'step': 0, 'name': 'output_dtype'},
                         {'step': 0, 'name': 'reference_output'},
                         {'step': 4, 'name': 'tensor_values'},
                         {'step': 5, 'name': 'reps'},
                         {'step': 5, 'name': 'reps_all_layers'}]
    pipeline.add_step(process_data, step_requirements)


    step_requirements = [{'main_arg': 'out_dir'},
                         {'main_arg': 'workdir'},
                         {'step': 4, 'name': 'layer_list'},
                         {'step': 4, 'name': 'ram'},
                         {'step': 4, 'name': 'flash'},
                         {'step': 6, 'name': 'per_layer_timings_mean'},
                         {'step': 6, 'name': 'per_layer_timings_std_dev'},
                         {'step': 6, 'name': 'all_layers_timings_mean'},
                         {'step': 6, 'name': 'all_layers_timings_std_dev'},
                         {'step': 6, 'name': 'mcu_tensor_values'},
                         {'step': 6, 'name': 'ref_tensor_values'}]
    pipeline.add_step(save_results, step_requirements)

    pipeline.run()

    if pipeline.steps[-1].output["Success"] == True:
        return 0
    else:
        return -1
    
    # Test output
    layer_list = pipeline.steps[4].output["layer_list"]
    ram = pipeline.steps[4].output["ram"]
    flash = pipeline.steps[4].output["flash"]
    per_layer_timings_mean = pipeline.steps[6].output["per_layer_timings_mean"]
    all_layers_timings_mean = pipeline.steps[6].output["all_layers_timings_mean"]
    mcu_tensor_values = pipeline.steps[6].output["mcu_tensor_values"]
    ref_tensor_values = pipeline.steps[6].output["ref_tensor_values"]
    
    print("RUN SUMMARY:")
    print("Used RAM (bytes): ", ram)
    print("Used FLASH (bytes): ", flash)
    print()
    print("layer names:")
    print(layer_list)
    print()
    print("layer_timings:")
    print(per_layer_timings_mean.shape)
    print(per_layer_timings_mean)
    print("sum of layer timings:")
    import numpy as np
    print(np.sum(per_layer_timings_mean))
    print()
    print("all_layers_timings shape:")
    print(all_layers_timings_mean.shape)
    print(all_layers_timings_mean)
    print()
    print("tensor_values shape:")
    print(mcu_tensor_values.shape)
    print()
    print("tensor_values:")
    print(mcu_tensor_values)
    print()
    print("ref_tensor_values shape:")
    print(ref_tensor_values.shape)
    print()
    print("ref_tensor_values:")
    print(ref_tensor_values)

    import sys; sys.exit(0)

    # TODO
    #TODO: read ouput values from network_output/network_val_io.npz to retrive C model output process_data
    #Also implement total runtime by disabling the observer

    pipeline.run()
    print()
    print(pipeline.steps[-1].output)
    for rep in pipeline.steps[-1].output["reps"]:
        print(rep)
    import sys;sys.exit(0)

    # from assemble_project import assemble_project
    # from flash_mcu import flash_mcu
    # from uart_readback import uart_readback
    # from store_data import store_data


if __name__ == '__main__':
    import sys
    sys.exit(_main())
