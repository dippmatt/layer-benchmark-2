import os
import json
import numpy as np
import pandas as pd

def get_layer_inference_time(workdir, uart_result, num_samples, num_reps):
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
    
    
    timings_reps = get_uart_timing_list(uart_result)

    # convert measurements into array of shape:
    # (num_samples, num_reps, num_layers)
    # num_samples: number of unique input tensors, used for inference
    # num_reps: number of inferences (repetitions) for each input tensor
    # num_layers: number of layers in the model, each layer has it's inference time measurement
    
    # create array-like list of lists for all measurements
    timing_array = []
    for i in range(num_samples):
        sample_array = []
        for j in range(num_reps):
            # append dummy value
            sample_array.append(0)
        timing_array.append(sample_array)

    # fill array
    for i, timings in enumerate(timings_reps):
        sample_index = i // num_reps
        rep_index = i % num_reps
        timing_array[sample_index][rep_index] = timings
    timing_array = np.array(timing_array)

    # combine layer metadata with timing benchmarks on HW
    assert timing_array.shape[-1] == len(layer_list), "Length mismatch between measured layers and layer number found in metadata file."
    test_pd(timing_array, layer_list, workdir)

    import sys; sys.exit()
    ############################################ OLD
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

def get_uart_timing_list(uart_result_reps):
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
    
    timings_reps = []
    for uart_result in uart_result_reps:
        timings = []
        for line in uart_result:
            if "STOP" in line:
                timing = line.split('+')[1]
                timing = timing.strip(' ')
                # convert to int and then to ms from µs
                timings.append(int(timing.strip('µs')) / 1000)
        timings_reps.append(timings)
    return timings_reps

def test_pd(result_tensor, layer_metadata, workdir):
    num_samples, num_reps, num_layers = result_tensor.shape
    data_dict = dict()
    data_dict['num_samples'] = num_samples
    data_dict['num_reps'] = num_reps
    data_dict['num_layers'] = num_layers

    data_dict['metadata'] = dict()
    for i, layer_data in enumerate(layer_metadata):
        data_dict['metadata'][i] = layer_data

    # for i, input in enumerate(result_tensor):
    #     input_dict = dict()
    #     for k, rep in enumerate(input):
    #         rep_dict = dict()
    #         for l, timing in enumerate(rep):
    #             timing_dict = dict()
    #             timing_dict['time'] = timing
    #             rep_dict[l] = timing_dict
    #         # if k == 0:
    #         #     rep_dict['result'] = result
    #         input_dict[k] = rep_dict
    #     data_dict[i] = input_dict

    arr = result_tensor.reshape(num_samples * num_reps, num_layers)
    tensor_indices = np.repeat(np.arange(num_samples), num_reps)
    repetition_indices = np.tile(np.arange(num_reps), num_samples)
    headers = [f'Tensor_{t}_Rep_{r}' for t, r in zip(tensor_indices, repetition_indices)]
    for header in headers:
        print(type(header))
    print(len(headers))
    print(type(headers))
    df = pd.DataFrame(arr.T, columns=headers)
    
    df.to_csv(os.path.join(workdir, "data.csv"), index=False)
    return
    data_save_path = os.path.join(workdir, "data.json")
    with open(data_save_path, "w") as file:
        json.dump(data_dict, file)

    