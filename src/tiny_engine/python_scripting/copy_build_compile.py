from pathlib import Path
import numpy as np
import shutil
import subprocess
from os import chdir
import re

# Idea: use cube_prj to run 2 inference loops: one with layer-by-layer measurements,
# and one with whole model measurements. Then, use the layer-by-layer measurements
# to estimate the overhead of the measurement process.

def copy_build_compile(workdir: Path, repetitions: int, input_tensors, input_dtype, output_shape: tuple, cube_template: Path, cube_template_all_layers: Path, cube_template_ref: Path, cube_template_empty: Path, codegen_src: Path):
    """Copy all data into the cube project, build and compile it
    Repeat for the inference tempalate, the reference template and the empty template.
    Inference Template: The template to run measurements.
    Reference Template: The template to measure the overhead of layer-by-layer measurements.
    Empty Template: The template to measure the RAM and FLASH usage of the model.
    Args:
        workdir: The working directory.
        repetitions: The number of repetitions to run the inference per input tensor.
        input_tensors: The input tensors.
        input_dtype: The data type of the input tensors.
        cube_template: The path to the STM Cube IDE Inference Template project.
        codegen_src: The path to the generated model C code.
    """
    step_output = dict()
    
    # generate input test tensors as C header from npz data
    if input_dtype in [np.float16, np.float32, np.float64, np.float128]:
        io_dtype = 'float'
    elif input_dtype in [np.uint8, np.uint16, np.uint32, np.uint64]:
        io_dtype = 'uint8_t'
    else:
        io_dtype = 'int8_t'
    test_tensor_header = gen_test_tensors(input_tensors, io_dtype)
    
    # copy test tensors into project only, not into reference project,
    # because the tensors are not part of the model
    data_header = cube_template / Path("Core", "Inc", "ml_data.h")
    with open(data_header, 'w') as f:
        f.writelines(test_tensor_header)
    data_header = cube_template_all_layers / Path("Core", "Inc", "ml_data.h")
    with open(data_header, 'w') as f:
        f.writelines(test_tensor_header)

    # copy framework bundle into project and reference project, 
    # not into empty project because we want to measure the RAM and FLASH usage of the model
    codegen = cube_template / Path("Core", "Src", "TinyEngine", "codegen")
    codegen_all_layers = cube_template_all_layers / Path("Core", "Src", "TinyEngine", "codegen")
    codegen_ref = cube_template_ref / Path("Core", "Src", "TinyEngine", "codegen")
    shutil.copytree(codegen_src, codegen)
    shutil.copytree(codegen_src, codegen_all_layers)
    shutil.copytree(codegen_src, codegen_ref)

    genModel_profiled = codegen / Path("Source", "genModel.c")
    assert genModel_profiled.exists(), f"{genModel_profiled} does not exist or is not a file"
    # insert profiling events into genModel.c
    insert_layer_measurements(genModel_profiled)

    main_c = cube_template / Path("Core", "Src", "main.c")
    main_c_all_layers = cube_template_all_layers / Path("Core", "Src", "main.c")
    main_c_ref = cube_template_ref / Path("Core", "Src", "main.c")

    # set the number of repetitions for each input tensor propagated through the model.
    # can be used for averaging the inference time over multiple runs.
    set_reps(main_c, repetitions)
    set_reps(main_c_all_layers, repetitions)
    set_reps(main_c_ref, repetitions)
    # explicitly define memory buffer allocation input / output tensors
    set_io_byte_consts(main_c, io_dtype, output_shape)
    set_io_byte_consts(main_c_all_layers, io_dtype, output_shape)
    set_io_byte_consts(main_c_ref, io_dtype, output_shape)        

    # compile projects
    templates = [cube_template, cube_template_all_layers, cube_template_ref, cube_template_empty]
    template_names = ["cube_template", "cube_template_all_layers", "cube_template_ref", "cube_template_empty"]
    for i, template in enumerate(templates):
        build_dir = template / Path("Debug")
        chdir(build_dir)
        logfile = build_dir / Path("compile.log")
        assert subprocess.call("make all > compile.log", shell=True) == 0, f"Compiling model project encountered an error. See {logfile} for details."
        ioc_files = template.glob("*.ioc")
        first_ioc_file = next(ioc_files, None)
        prj_name = str(first_ioc_file.stem)
        elf_file = build_dir / Path(f"{prj_name}.elf")
        assert elf_file.exists(), f"Compiling model project encountered an error. See {logfile} for details."
        step_output[template_names[i]] = elf_file

    ram, flash = calc_flash_ram(step_output["cube_template_ref"], step_output["cube_template_empty"])
    step_output["flash"] = flash
    step_output["ram"] = ram

    return step_output

    
def insert_layer_measurements(genModel: Path):
    with open(genModel) as f:
        input_lines = f.readlines()

    invoke_trigger = False

    layer_number = 0
    # insert START events for each layer
    for i, line in enumerate(input_lines):
        # find out if we are in function that executes the model
        if "void invoke" in line:
            invoke_trigger = True
            layer_number = 0
            continue
        # if the functoin ends, we want to know
        if invoke_trigger == True:
            if "}" in line:
                invoke_trigger = False
            # comment indicating a new layer
            if "/*" in line and "*/" in line:
                layer_name = line.rstrip("\n")
                layer_name = layer_name.replace("/* ", "")
                layer_name = layer_name.replace(" */", "") 
                input_lines[i] = f"PROFILING_EVENT(\"START Timestamp before {layer_name} {layer_number}\");\n"
                layer_number += 1
    
    # insert STOP events for each layer
    new_line = 'PROFILING_EVENT("STOP");\n'
    index = 0
    while index < len(input_lines):
        # Check if the current line is a line of interest
        if "START Timestamp" in input_lines[index]:
            # Insert the new line two lines after the detected line
            input_lines.insert(index + 2, new_line)
            # Move the index to the line after the inserted line
            index += 3  # Adjust for the newly inserted line and continue checking
        else:
            index += 1

    with open(genModel, "w") as f:
        f.writelines(input_lines)

def gen_test_tensors(input_tensors, input_dtype):
    """Create test tensors as C arrays

    Creates a C header file with the test tensors as C arrays.
    The header file is saved in the STM Cube project's Inc folder.
    Args:
        input_tensors: A np array with the test tensors.
        input_dtype: The data type of the input tensors.
    
    Returns: A list of lines, content of the header file.
    """
    flat_tensor_len = 1
    num_samples = input_tensors.shape[0]
    for shape in input_tensors.shape[1:]:
        flat_tensor_len *= shape
    
    lines_o = []
    lines_o.append("#ifndef ML_DATA_H\n")
    lines_o.append("#define ML_DATA_H\n")
    lines_o.append("\n")
    lines_o.append("#include <stdint.h>\n")
    lines_o.append(f"#define ROWS {num_samples}\n")
    lines_o.append(f"#define COLS {flat_tensor_len}\n")
    lines_o.append("\n")
    lines_o.append("#endif /* ML_DATA_H */\n")
    lines_o.append("\n")

    lines_o.append(f"{input_dtype} array[ROWS][COLS] = {{\n")
    for i, tensor in enumerate(input_tensors):
        values = ""
        elem = tensor.flatten()
        for number in elem:
            if input_dtype == 'int8_t':
                values += f'{number}, '
            else:
                values += f'{number: .16e}, '
        values = values.rstrip(', ')
        lines_o.append(f"    {{ {values} }},\n")
    lines_o[-1] = lines_o[-1].rstrip(',\n') + '\n'
    lines_o.append('};\n')
    return lines_o

def get_io_names(model_h: str):
    assert model_h.exists(), f"{model_h} does not exist or is not a file"
    
    with open(model_h, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if "// Placeholder address offsets within mutable buffer (bytes)." in line:
                input_layer = lines[i+1] 
                output_layer = lines[i+2]
                break

        # Example for input / output layer constant offset defines,
        # we want the name of the preprocessor constant
        #define MODEL_serving_default_input_1_0  0
        #define MODEL_StatefulPartitionedCall_0  1984
        input_layer = input_layer.split()
        input_name = input_layer[1] 
        output_layer = output_layer.split()
        output_name = output_layer[1] 
    return input_name, output_name

def set_reps(main_c: Path, repetitions: int):
    assert main_c.exists(), f"{main_c} does not exist or is not a file"

    with open(main_c, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if "<REPETITIONS_PER_INPUT_TENSOR>" in line:
                lines[i] = line.replace("<REPETITIONS_PER_INPUT_TENSOR>", str(repetitions))
                
    with open(main_c, 'w') as file:
        file.writelines(lines)
    return

def set_io_byte_consts(main_c: Path, c_out_dtype: str, output_shape: tuple):
    assert main_c.exists(), f"{main_c} does not exist or is not a file"
        
    # multiply all dimensions to get the total number of elements in the output tensor
    output_elements = 1
    for dimension in output_shape:
        output_elements *= dimension    

    if c_out_dtype == 'float':
        c_out_specifier = 'f'
    elif c_out_dtype == 'int8_t':
        c_out_specifier = 'd'
    else:
        c_out_specifier = 'u'

    with open(main_c, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            # set flattened output tensor size
            if "<ELEMENTS>" in line:
                line = line.replace("<ELEMENTS>", str(output_elements))
            if "<o_type>" in line:
                line = line.replace("<o_type>", c_out_dtype)
            if "<int_type>" in line:
                # special case when using float model:
                # we don't need this funciton so just use uint8_t by default
                # if we were to use float we would have a function redefinition error
                if c_out_dtype == 'uint8_t':
                    line = line.replace("<int_type>", c_out_dtype)
                else:
                    line = line.replace("<int_type>", 'int8_t')
            if "<o_format_specifier>" in line:
                line = line.replace("<o_format_specifier>", c_out_specifier)
            lines[i] = line
                
    with open(main_c, 'w') as file:
        file.writelines(lines)
    return

def calc_flash_ram(elf_file_ref: Path, elf_file_empty: Path):
    """Calculate the flash and RAM usage of the project.

    Returns: A tuple with the flash and RAM usage.
    """
    # Define the regular expression patterns for the sections and sizes
    pattern_text = r"\.text\s+(\d+)"
    pattern_data = r"\.data\s+(\d+)"
    pattern_bss = r"\.bss\s+(\d+)"

    ref_size = subprocess.check_output(f'arm-none-eabi-size -A {elf_file_ref}', shell=True, text=True)
    empty_size = subprocess.check_output(f'arm-none-eabi-size -A {elf_file_empty}', shell=True, text=True)
    
    text_sizes_ref = re.findall(pattern_text, ref_size)
    data_sizes_ref = re.findall(pattern_data, ref_size)
    bss_sizes_ref = re.findall(pattern_bss, ref_size)

    text_sizes_empty = re.findall(pattern_text, empty_size)
    data_sizes_empty = re.findall(pattern_data, empty_size)
    bss_sizes_empty = re.findall(pattern_bss, empty_size)

    flash_usage_ref = int(data_sizes_ref[0]) + int(text_sizes_ref[0])
    ram_usage_ref = int(bss_sizes_ref[0]) + int(data_sizes_ref[0])

    flash_usage_empty = int(data_sizes_empty[0]) + int(text_sizes_empty[0])
    ram_usage_empty = int(bss_sizes_empty[0]) + int(data_sizes_empty[0])

    ram_diff = ram_usage_ref - ram_usage_empty
    flash_diff = flash_usage_ref - flash_usage_empty

    print(f"Flash usage reference: {flash_usage_ref} bytes")
    print(f"RAM usage reference: {ram_usage_ref} bytes")
    print(f"Flash usage empty: {flash_usage_empty} bytes")
    print(f"RAM usage empty: {ram_usage_empty} bytes")
    print(f"Flash usage: {flash_diff} bytes")
    print(f"RAM usage: {ram_diff} bytes")
    print()
    return (ram_diff, flash_diff)