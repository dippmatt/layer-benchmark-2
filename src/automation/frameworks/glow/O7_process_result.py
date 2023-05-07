import os

def get_layer_inference_time(workdir, uart_result):
    layer_info_file = os.path.abspath(os.path.join(workdir, "..", "instrument-ir.info"))

    with open(layer_info_file, 'r') as file:
        lines = file.readlines()
    
    layer_list = []
    i = 0
    while(1):
        line = lines[i]
        if "ID" in line:
            layer_info, last_layer_line_index = parse_layer(i, lines)
            layer_list.append(layer_info)
            i = last_layer_line_index
        i += 1 
        if i >= len(lines):
            break

    timings = get_uart_timing_list(uart_result)
    
    # combine layer metadata with timing benchmarks on HW
    assert len(timings) == len(layer_list), "Length mismatch between measured layers and layer number found in metadata file."
    for i, timing in enumerate(timings):
        layer_list[i]['time'] = timing
    
    return layer_list
            

def parse_layer(index_with_ID, lines):
    # Glow layer log dump looks like this:
    
    # ID   : 0
    # Kind : 156 (armcmcwqconvolution)
    # Name : model_activation_Relu_model_batch_normalization_FusedBatchNormV3_model_conv2d_BiasAdd_ReadVariableOp_model_conv2d_BiasAdd_model_conv2d_4_Conv2D_model_conv2d_Conv2D1__1
    # Inp[0] Src:       i8[S:0.584702909 O:83][-123.372,25.727]<1 x 49 x 10 x 1>
    # Inp[1] Filter:    i8[S:1.000000000 O:0][-128.000,127.000]<64 x 10 x 4 x 1>
    # Inp[2] Bias:      i32[S:1.000000000 O:0][-2147483648.000,2147483648.000]<64>
    # Out[0] Dest:      i8[S:0.094564661 O:-128][0.000,24.114]<1 x 25 x 5 x 64>
    # Out[1] Scratch:   i8[S:0.000000000 O:0][-0.000,0.000]<160>

    i = index_with_ID
    layer_info = dict()
    io_info = []
    while(1):
        line = lines[i]
        # delimiter line between layers
        if line == "\n":
            layer_info["io_info"] = io_info
            last_layer_line_index = i
            return layer_info, last_layer_line_index
        elif "ID" in line:
            tokens = line.split(":")
            id = int(tokens[1].replace(" ", ""))
            layer_info["id"] = id
        elif "Kind" in line:
            tokens = line.split(":", maxsplit=1)
            kind = tokens[1].replace(" ", "")
            layer_info["kind"] = kind.rstrip("\n")
        elif "Name" in line:
            tokens = line.split(":", maxsplit=1)
            name = tokens[1].replace(" ", "")
            layer_info["name"] = name.rstrip("\n")
        else:
            io_info.append(line)
        i += 1

def get_uart_timing_list(uart_result):
################## Example Response from UART Serial  ###################
# Profiling "MAIN loop timing" sequence: 
# --Event-----------------------|--timestamp--|----delta_t---
# BEGIN                         :        0 µs | +        0 µs
# START                         :        2 µs | +        2 µs
# STOP                          :    14570 µs | +    14568 µs
# START                         :    14571 µs | +        1 µs
# STOP                          :    23141 µs | +     8570 µs
# START                         :    23143 µs | +        2 µs
# STOP                          :    33860 µs | +    10717 µs
# START                         :    33861 µs | +        1 µs
# STOP                          :    42431 µs | +     8570 µs
# START                         :    42433 µs | +        2 µs
# STOP                          :    53150 µs | +    10717 µs
# START                         :    53151 µs | +        1 µs
# STOP                          :    61721 µs | +     8570 µs
# START                         :    61723 µs | +        2 µs
# STOP                          :    72440 µs | +    10717 µs
# START                         :    72441 µs | +        1 µs
# STOP                          :    81011 µs | +     8570 µs
# START                         :    81013 µs | +        2 µs
# STOP                          :    91730 µs | +    10717 µs
# START                         :    91731 µs | +        1 µs
# STOP                          :    92018 µs | +      287 µs
# START                         :    92019 µs | +        1 µs
# STOP                          :    92049 µs | +       30 µs
# START                         :    92049 µs | +        0 µs
# STOP                          :    92060 µs | +       11 µs
# END                           :    92060 µs | +        0 µs

    timings = []
    for line in uart_result:
        if "STOP" in line:
            timing = line.split('+')[1]
            timing = timing.strip(' ')
            timings.append(int(timing.strip('µs')))
    return timings