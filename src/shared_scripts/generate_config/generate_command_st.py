import sys
import json
import subprocess

def generate_command(config):
    command_parts = ["python3", "st/python_scripting/main.py"]
    
    for arg, value in config["arguments"].items():
        command_parts.append(f"{arg}")
        command_parts.append(value)
    
    command_parts.extend(config["parameters"])

    command = ""
    for command_part in command_parts:
    	command += command_part + " "
    
    return command



if __name__ == "__main__":
    with open(sys.argv[1], "r") as config_file:
        config = json.load(config_file)

    command = generate_command(config)
    print(command)
