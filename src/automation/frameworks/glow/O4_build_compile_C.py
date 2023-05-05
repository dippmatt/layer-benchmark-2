import os

def build_cube_prj(glow_cubeIDE_template, workdir, bundle_dir):

    # copy STMCubeIDE project template to workdir
    cube_prj = os.path.join(workdir, os.path.basename(os.path.dirname(glow_cubeIDE_template)))
    os.system(f"cp -r {glow_cubeIDE_template} {cube_prj}")

    # copy model source files into project
    src_dir = os.path.join(cube_prj, "Core", "Src")
    inc_dir = os.path.join(cube_prj, "Core", "Inc")

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
    set_io_names(main_c, input_name, output_name)
    # compile project
    cwd = os.getcwd()
    build_dir = os.path.join(cube_prj, "Debug")
    os.chdir(build_dir)
    logfile = os.path.join(build_dir, "compile.log")
    assert os.system("make all > compile.log") == 0, f"Compiling model project encountered an error. See {logfile} for details."
    elf_file = os.path.abspath(os.path.basename(os.path.dirname(glow_cubeIDE_template)) + ".elf")
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