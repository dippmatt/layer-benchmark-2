import json
from pathlib import Path
import codecs

def get_json(json_path: Path):    
    json_dict = json.load(codecs.open(json_path, 'r', 'utf-8-sig'))
    return json_dict

def create_permutations(config, schema, root_dir):
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
    finaly_permutations = []
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
                for model_int in config["use_case"][use_case]["model_int"]:
                    perm_copy = permutation.copy()
                    if use_case == "ad":
                        perm_copy["-model"] = model_int
                        perm_copy["unique_key"] += "int_"
                    elif "no_softmax" in model_int:
                        perm_copy["-model"] = model_int
                        perm_copy["unique_key"] += "int_nosoftmax_"
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

        finaly_permutations.extend(output_permutations)
        
    unique_keys = []
    for permutation in finaly_permutations:
        permutation_string = json.dumps(permutation, indent=2)
        unique_keys.append(permutation["unique_key"])
        print(permutation_string)
    print(len(finaly_permutations))
    print(len(set(unique_keys)))
    import sys;sys.exit()

    print(config["frameworks"][framework].keys())

    

if __name__ == "__main__":
    config_path = Path.cwd() / "config.json"
    schema_path = Path.cwd() / "schema.json"

    
    config = get_json(config_path)
    schema = get_json(schema_path)

    # insert root_dir placeholder
    root_dir = config["root_dir"]
    config_string = json.dumps(config, indent=2)
    #config_string = config_string.replace("<root_dir>", str(root_dir))
    config = json.loads(config_string)

    create_permutations(config, schema, root_dir)
    
    config_string = json.dumps(config, indent=2)
    schema_string = json.dumps(schema, indent=2)
    print(config_string)
    print(schema_string)
    