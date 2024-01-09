import json
from pathlib import Path
import codecs
import subprocess
from shared_scripts.color_print import print_in_color, Color

def get_json(json_path: Path):    
    json_dict = json.load(codecs.open(json_path, 'r', 'utf-8-sig'))
    return json_dict

def create_run_commands(permutations: list):
    commands = []
    final_permutations = []
    broken_keys = ["glow_noquant_ad_normal_float_", 
                   "glow_noquant_ad_anomaly_float_", 
                   "glow_quant_ad_normal_float_", 
                   "glow_quant_ad_anomaly_float_", 
                   "glow_quant_vww_float_", 
                   "tiny_engine_kws_int_nosoftmax_", 
                   "glow_quant_vww_float_nosoftmax_", 
                   "glow_noquant_vww_int_",
                   "glow_noquant_vww_int_nosoftmax_",
                   "glow_noquant_vww_float_",
                   "glow_noquant_vww_float_nosoftmax_"]
    skip_counter = 0
    for permutation in permutations:
        venv_dir = (Path(permutation["-workdir"]) / Path("..", "venv", "bin")).resolve()
        python_exec = venv_dir / Path("python3")
        python_main = Path(permutation["-workdir"]) / Path("..", "python_scripting", "main.py")
        python_main = python_main.resolve()

        assert python_exec.exists(), f"Python executable {python_exec} does not exist"
        assert python_main.exists(), f"Python main {python_main} does not exist"

        command = ""
        command += str(python_exec) + " " + str(python_main) + " "
        #print(python_exec, python_main, end=" ")
    
        for key, value in permutation.items():
            if key[0] == "-":
                if key == "-out_dir":
                    # create unique out_dir
                    out_dir = Path(value) / Path(permutation["unique_key"])
                    out_dir = out_dir.resolve()
  
                    # create out_dir if it does not exist
                    if not out_dir.exists():
                        out_dir.mkdir(parents=True, exist_ok=True)

                    # if "tflite" in str(out_dir):
                    #     print(type(out_dir))
                    #     print(out_dir)
                    #     import sys;sys.exit()
                    
                    # check if output is already present
                    contents = list(out_dir.glob('*'))
                    if not contents:
                        results_present = False
                    else:
                        results_present = True

                    value = str(out_dir)
                if type(value) == bool and value == True:
                    #print(key, end=" ")
                    command += key + " "
                elif type(value) == bool and value == False:
                    pass
                else:
                    #print(key, value, end=" ")
                    command += key + " " + str(value) + " "
        
        if permutation["unique_key"] in broken_keys:
            omit_command = True
        else:
            omit_command = False
        
        if not results_present and not omit_command:
            commands.append(command)
            final_permutations.append(permutation)
        else:
            print_in_color(Color.YELLOW, f"Skipping {permutation['unique_key']}, results already present")
            skip_counter += 1
            continue
    print_in_color(Color.YELLOW, f"Skipping {skip_counter} permutations")
    return commands, final_permutations
        
def run_commands(commands: list, permutations: list, command_run_dir: Path, log_dir: Path):
    
    num_permutations = len(permutations)
    for i, command in enumerate(commands):
        unique_key = permutations[i]["unique_key"]
        print(command)
        print()
        print("Running permutation: ", f"{i+1}/{num_permutations}")
        print("Running configuration: ", unique_key)
        result = subprocess.run(command, shell=True, cwd=command_run_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Check the return code
        if result.returncode == 0:
            print_in_color(Color.GREEN, f"SUCCESS {unique_key}")
        else:
            print_in_color(Color.RED, f"FAILED {unique_key}")
        print()

        stdout_output = result.stdout.decode('utf-8')
        stderr_output = result.stderr.decode('utf-8')

        with open(Path(log_dir, unique_key + ".stdout"), "w") as file:
            file.write(stdout_output)
        with open(Path(log_dir, unique_key + ".stderr"), "w") as file:
            file.write(stderr_output)
    return

def create_permutations(config):
    framework_permutations = []
    frameworks = config["frameworks"].keys()

    # create unique keys, to identify permutations
    permutation_string = ""
    for framework in frameworks:
        # create framework permutations
        permutation = {}
        permutation["unique_key"] = framework + "_"
        fixed = []
        variables = []
        for key in config["frameworks"][framework].keys():            
            if isinstance(config["frameworks"][framework][key], list):
                variables.append(key)
            else:
                fixed.append(key)
            
        # add fixed values to permutation
        for key in fixed:
            permutation["-" + key] = config["frameworks"][framework][key]
            
        # add variable values to permutation
        if len(variables) == 0:
            framework_permutations.append(permutation.copy())
        else:
            for variable in variables:
                for value in config["frameworks"][framework][variable]:
                    sub_permutation = permutation.copy()
                    sub_permutation["-" + variable] = value
                    
                    # append identifier to permutation string
                    if variable == "quantize":
                        if value == True:
                            sub_permutation["unique_key"] += "quant_"
                        else:
                            sub_permutation["unique_key"] += "noquant_"
                    elif variable == "cube_template" and framework == "st":
                        if "time" in value:
                            sub_permutation["unique_key"] += "time_"
                        elif "ram" in value:
                            sub_permutation["unique_key"] += "ram_"
                        elif "balanced" in value:
                            sub_permutation["unique_key"] += "balanced_"
                        else:
                            raise ValueError("Invalid cube template")
                    
                    framework_permutations.append(sub_permutation.copy())
                    

    # create use case permutations
    final_permutations = []
    for use_case in config["use_case"].keys():
        input_permutations = framework_permutations.copy()
        output_permutations = []

        for permutation in input_permutations:
            perm_copy = permutation.copy()
            perm_copy["unique_key"] += use_case + "_"
            output_permutations.append(perm_copy)
        
        input_permutations = output_permutations
        output_permutations = []  

        # insert test data
        for permutation in input_permutations:
            if use_case == "ad":
                perm_copy1 = permutation.copy()
                perm_copy2 = permutation.copy()
                perm_copy1["-input_tensors"] = config["use_case"][use_case]["test_data_fp"][0]
                perm_copy2["-input_tensors"] = config["use_case"][use_case]["test_data_fp"][1]
                perm_copy1["unique_key"] += "normal_"
                perm_copy2["unique_key"] += "anomaly_"
                output_permutations.append(perm_copy1)
                output_permutations.append(perm_copy2)
            else:
                perm_copy = permutation.copy()
                perm_copy["-input_tensors"] = config["use_case"][use_case]["test_data_fp"][0]
                output_permutations.append(perm_copy)

        input_permutations = output_permutations
        output_permutations = []      
        # insert model into permutation
        for permutation in input_permutations:

            if "tiny_engine" in permutation["unique_key"]:
                # glow can only use quantized models
                for model_int in config["use_case"][use_case]["model_int"]:
                    perm_copy = permutation.copy()
                    if use_case == "ad":
                        perm_copy["-model"] = model_int
                        perm_copy["unique_key"] += "int_"
                    elif "no_softmax" in model_int:
                        perm_copy["-model"] = model_int
                        perm_copy["unique_key"] += "int_nosoftmax_"
                    else:
                        continue
                
                    output_permutations.append(perm_copy)

            elif "glow" in permutation["unique_key"]:
                # cannot quantize quantized models
                if permutation["-quantize"] == False:
                    for model_int in config["use_case"][use_case]["model_int"]:
                        perm_copy = permutation.copy()
                        if "no_softmax" in model_int:
                            perm_copy["unique_key"] += "int_nosoftmax_"
                        else:
                            perm_copy["unique_key"] += "int_"
                        perm_copy["-model"] = model_int
                        output_permutations.append(perm_copy)
                for model_fp in config["use_case"][use_case]["model_fp"]:
                    perm_copy = permutation.copy()
                    perm_copy["-model"] = model_fp
                    if "no_softmax" in model_fp:
                        perm_copy["unique_key"] += "float_nosoftmax_"
                    else:
                        perm_copy["unique_key"] += "float_"
                    perm_copy["-representative_tensors"] = config["use_case"][use_case]["representative_data_fp"]
                    output_permutations.append(perm_copy)

            elif "st" in permutation["unique_key"]:
                for model_fp in config["use_case"][use_case]["model_fp"]:
                    perm_copy = permutation.copy()
                    if "no_softmax" in model_fp:
                        perm_copy["unique_key"] += "float_nosoftmax_"
                    else:
                        perm_copy["unique_key"] += "float_"
                    perm_copy["-model"] = model_fp
                    output_permutations.append(perm_copy)
                
                for model_int in config["use_case"][use_case]["model_int"]:
                    perm_copy = permutation.copy()
                    if "no_softmax" in model_int:
                        perm_copy["unique_key"] += "int_nosoftmax_"
                    else:
                        perm_copy["unique_key"] += "int_"
                    perm_copy["-model"] = model_int
                    output_permutations.append(perm_copy)

            elif "tflite" in permutation["unique_key"]:
                # for model_fp in config["use_case"][use_case]["model_fp"]:
                #     perm_copy = permutation.copy()
                #     if "no_softmax" in model_fp:
                #         perm_copy["unique_key"] += "float_nosoftmax_"
                #     else:
                #         perm_copy["unique_key"] += "float_"
                #     perm_copy["-model"] = model_fp
                #     output_permutations.append(perm_copy)
                for model_int in config["use_case"][use_case]["model_int"]:
                    perm_copy = permutation.copy()
                    if "no_softmax" in model_int:
                        continue
                    else:
                        perm_copy["unique_key"] += "int_"
                    perm_copy["-model"] = model_int
                    output_permutations.append(perm_copy)

        final_permutations.extend(output_permutations)
    
    return final_permutations
    
    # Dead code to verify permutations and unique keys
    unique_keys = []
    for permutation in final_permutations:
        permutation_string = json.dumps(permutation, indent=2)
        unique_keys.append(permutation["unique_key"])
        print(permutation_string)
    print(len(final_permutations))
    print(len(set(unique_keys)))
    import sys;sys.exit()

    print(config["frameworks"][framework].keys())

    return final_permutations
    

if __name__ == "__main__":
    config_path = Path(Path.cwd(), "benchmark_automation" , "config.json")
    config = get_json(config_path)

    # insert root_dir placeholder
    root_dir = config["root_dir"]
    config_string = json.dumps(config, indent=2)
    config_string = config_string.replace("<root_dir>", str(root_dir))
    config = json.loads(config_string)

    permutations = create_permutations(config)
    print()
    for permutation in permutations:
        print(permutation["unique_key"])
    print()
    print(len(permutations))
    # import sys; sys.exit(0)

    commands, final_permutations = create_run_commands(permutations)
    command_run_dir = Path(root_dir, "src")
    log_dir = Path(root_dir, "logs")

    run_commands(commands, final_permutations, command_run_dir, log_dir)

    import sys; sys.exit(0)
    
    config_string = json.dumps(config, indent=2)
    print(config_string)
    
