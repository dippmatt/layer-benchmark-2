from color_print import print_in_color, Color

def process_data(tensor_values: list, reps: list, reps_no_ir: list):
    """Processes benchmark data from the STM32 MCU and saves it to a file.
    """
    step_output = dict()
    
    print_in_color(Color.GREEN, "Testing data processing for tensor values")
    for tensor_value in tensor_values:
        # remove trailing whitespace
        tensor_value = tensor_value.rstrip(' ')
        tensor_value = tensor_value.split(' ')
        assert len(tensor_value) == 640, "Tensor value has wrong format."
        print(tensor_value)
    
    print()

    print_in_color(Color.GREEN, "Testing data processing for reps")
    for rep in reps:
        print(len(rep))

    print()

    print_in_color(Color.GREEN, "Testing data processing for reps_no_ir")
    for rep in reps_no_ir:
        print(rep)
    
    step_output["return_code"] = 0
    return step_output


    



