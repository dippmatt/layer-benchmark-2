import os

def gen_test_tensors(test_tensors, io_type):
    # creates a header file in the STM Cube project's 'Inc' directory,
    # that contains all test tensors as an array of arrays of all tensors.

    # get number of elements to store in a flat tensor
    flat_tensor_len = 1
    num_samples = test_tensors.shape[0]
    for shape in test_tensors.shape[1:]:
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

    lines_o.append(f"{io_type} array[ROWS][COLS] = {{\n")
    for i, tensor in enumerate(test_tensors):
        values = ""
        elem = tensor.flatten()
        for number in elem:
            #values += f'{number: .6e}, '
            values += f'{number: e}, '
        values = values.rstrip(', ')
        lines_o.append(f"    {{ {values} }},\n")
    lines_o[-1] = lines_o[-1].rstrip(',\n') + '\n'
    lines_o.append('};\n')
    return lines_o

def build_cube_prj(glow_cubeIDE_template, repetitions, test_tensor_header, workdir, bundle_dir, build_ref):
    # copy STMCubeIDE project template to workdir    
    if str(glow_cubeIDE_template).endswith("/"):
        prj_name = os.path.basename(os.path.dirname(glow_cubeIDE_template))
    else:
        prj_name = os.path.basename(glow_cubeIDE_template)

    cube_prj = os.path.join(workdir, prj_name)

    os.system(f"cp -r {glow_cubeIDE_template} {cube_prj}")

    # copy model source files into project
    src_dir = os.path.join(cube_prj, "Core", "Src")
    inc_dir = os.path.join(cube_prj, "Core", "Inc")

    # copy test tensors
    data_header = os.path.join(inc_dir, "ml_data.h")
    with open(data_header, 'w') as f:
        f.writelines(test_tensor_header)

    src_files = ["model.o"]
    inc_files = ["model.h", "model.weights.txt"]

    for inc_file in inc_files:
        file = os.path.join(bundle_dir, inc_file)
        if inc_file == "model.h":
            input_name, output_name = get_io_names(file)
        os.system(f"cp -f {file} {inc_dir}")
    for src_file in src_files:
        file = os.path.join(bundle_dir, src_file)
        os.system(f"cp -f {file} {src_dir}")

    # insert correct model input and output layer names into main.c template
    main_c = os.path.join(src_dir, "main.c")
    model_h = os.path.join(inc_dir, "model.h")
    set_io_names(main_c, input_name, output_name)
    
    # set the number of repetitions each input tensor propagated through the model.
    # can be used for averaging
    set_reps(main_c, repetitions)
    # explicitly define memory buffer allocation input / output tensors
    set_io_byte_consts(main_c, model_h)
    # compile project
    cwd = os.getcwd()
    build_dir = os.path.join(cube_prj, "Debug")
    os.chdir(build_dir)
    logfile = os.path.join(build_dir, "compile.log")
    assert os.system("make all > compile.log") == 0, f"Compiling model project encountered an error. See {logfile} for details."
    elf_file = os.path.join(cube_prj, "Debug", f"{prj_name}.elf")
    assert os.path.isfile(elf_file)
    
    os.chdir(cwd)
    
    return elf_file

def get_io_names(model_h: str):
    assert os.path.isfile(model_h), f"{model_h} does not exist or is not a file"
    
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

def set_io_names(main_c: str, input_name: str, output_name: str):
    assert os.path.isfile(main_c), f"{main_c} does not exist or is not a file"
    
    with open(main_c, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if "<input_name>" in line:
                lines[i] = line.replace("<input_name>", input_name)
            if "<output_name>" in line:
                lines[i] = line.replace("<output_name>", output_name)

    with open(main_c, 'w') as file:
        file.writelines(lines)
    return

def set_reps(main_c: str, repetitions: int):
    assert os.path.isfile(main_c), f"{main_c} does not exist or is not a file"

    with open(main_c, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if "<REPETITIONS_PER_INPUT_TENSOR>" in line:
                lines[i] = line.replace("<REPETITIONS_PER_INPUT_TENSOR>", str(repetitions))
                
    with open(main_c, 'w') as file:
        file.writelines(lines)
    return

def set_io_byte_consts(main_c: str, model_h: str):
    assert os.path.isfile(main_c), f"{main_c} does not exist or is not a file"
    assert os.path.isfile(model_h), f"{model_h} does not exist or is not a file"

    with open(model_h, 'r') as file:
        found_io_placeholders = False
        input_found = False
        
        input_tensor_bytes = 0
        output_tensor_bytes = 0

        lines = file.readlines()
        for i, line in enumerate(lines):
            if "// Placeholders:" in line:
                found_io_placeholders = True
                continue
            if "Name: " in line and found_io_placeholders and not input_found:
                input_found = True
                n_bytes = lines[i+3].split('Size: ')[1]
                input_tensor_bytes = int(n_bytes.split()[0])
                continue
            if "Name: " in line and input_found:
                n_bytes = lines[i+3].split('Size: ')[1]
                output_tensor_bytes = int(n_bytes.split()[0])
                break

    with open(main_c, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if "<NUM_INPUT_BYTES>" in line:
                lines[i] = line.replace("<NUM_INPUT_BYTES>", str(input_tensor_bytes))
            if "<NUM_OUTPUT_BYTES>" in line:
                lines[i] = line.replace("<NUM_OUTPUT_BYTES>", str(output_tensor_bytes))
                
    with open(main_c, 'w') as file:
        file.writelines(lines)
    return

