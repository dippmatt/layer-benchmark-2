import os 
import sys
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('codegen', type=str, help='Path to the codegen folder, that was generated with tinyengine')
    args = parser.parse_args()

    genModel = os.path.join(args.codegen, "Source", "genModel.c")
    assert os.path.exists(genModel)

    with open(genModel) as f:
        input_lines = f.readlines()

    # save original file
    new_file_name = os.path.join(args.codegen, "Source", "genModel_backup.c")
    os.rename(genModel, new_file_name)

    invoke_trigger = False

    layer_number = 0
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
                input_lines[i] = f"PROFILING_EVENT(\"Timestamp before {layer_name} {layer_number}\");\n"
                layer_number += 1
            
        
    with open(genModel, "w") as f:
        f.writelines(input_lines)


if __name__ == '__main__':
    main()