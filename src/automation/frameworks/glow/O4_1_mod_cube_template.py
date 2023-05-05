import os

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