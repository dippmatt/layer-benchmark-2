from pathlib import Path
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import re
import copy
import subprocess
from paretoset import paretoset

def get_data_frame(data_source_dir: Path) -> pd.DataFrame:
    data_source_dir = data_source_dir.resolve()
    
    df = pd.DataFrame(columns=['model', 'framework', 'dtype', 'flash', 'ram', 'avg_timing', 'config_name', 'layer_names', 'rmse', 'nrmse', 'mae', 'l2r', 'std_dev', 'std_dev_per_layer', 'per_layer_timings', 'sum_timing', 'layer_assignments', 'ref_config_name', 'mcu_tensor_values', 'ref_tensor_values'])
    
    # Sanity check: verify the naming scheme of the benchmark folders
    framework_counter = 0
    model_counter = 0
    quant_counter = 0

    #########################################################################
    ######     Loop over all benchmarks and fill pandas data frame     ######
    #########################################################################
    
    for benchmark in data_source_dir.iterdir():
        # filter empty directories
        if not any(benchmark.iterdir()):
            continue
        
        # empty row template for df
        new_row_data = {'config_name': benchmark.stem}
        
        ##############################################
        ###### Fill model, framework, data type ######
        ##############################################

        # frameworks
        if 'tiny_engine' in benchmark.stem:
            framework_counter += 1
            new_row_data['framework'] = 'tiny_engine'
        if 'st_' in benchmark.stem:
            framework_counter += 1
            new_row_data['framework'] = 'st'
        if 'glow_' in benchmark.stem:
            framework_counter += 1
            new_row_data['framework'] = 'glow'
        if 'tflite_' in benchmark.stem:
            framework_counter += 1
            new_row_data['framework'] = 'tflite'
        # models
        if 'ad_' in benchmark.stem:
            model_counter += 1
            new_row_data['model'] = 'ad'
        if 'kws' in benchmark.stem:
            model_counter += 1
            new_row_data['model'] = 'kws'
        if 'vww' in benchmark.stem:
            model_counter += 1
            new_row_data['model'] = 'vww'
        if 'ic' in benchmark.stem:
            model_counter += 1
            new_row_data['model'] = 'ic'
        # data type schemes (int or float)
        if 'int' in benchmark.stem:
            quant_counter += 1
            new_row_data['dtype'] = 'int'
        if 'float' in benchmark.stem:
            quant_counter += 1
            if '_quant' in benchmark.stem:
                new_row_data['dtype'] = 'int'
            else:
                new_row_data['dtype'] = 'float'
        
        ###################################################
        ############### Insert layer names ################
        ###################################################

        layer_names_file = Path(benchmark, 'layer_list.txt')
        new_row_data['layer_names'] = read_layer_names(layer_names_file)

        ###################################################
        ###### Insert average timings for all layers ######
        ###################################################
        
        mean_timings = Path(benchmark, 'all_layers_timings_mean.npz')
        assert mean_timings.exists(), f'No mean timings found for {benchmark}.'
        input_data = np.load(mean_timings)

        avg_timing =input_data['arr_0']

        if avg_timing.shape == (1,):
            avg_timing = avg_timing[0]
        else:
            avg_timing = avg_timing
        new_row_data['avg_timing'] = avg_timing

        ###################################################
        #############  Insert sum of layers ###############
        ###################################################
        
        per_layer_timings = Path(benchmark, 'per_layer_timings_mean.npz')
        assert per_layer_timings.exists(), f'No mean timings found for {benchmark}.'
        input_data = np.load(per_layer_timings)

        per_layer_timings = input_data['arr_0']
        
        # the per layer timings have shape (reps, layers)
        # now create the mean and standard deviation over the first axis (reps)
        std_dev_timing = np.std(per_layer_timings, axis=0)
        mean_timing = np.mean(per_layer_timings, axis=0)

        sum = 0.0
        for layer_timing in mean_timing:
            sum += layer_timing
        new_row_data['sum_timing'] = sum
        new_row_data['per_layer_timings'] = per_layer_timings

        ###################################################
        ###### STD DEVIATION  ######
        ###################################################
        
        std_dev_file = Path(benchmark, 'all_layers_timings_std_dev.npz')
        if not std_dev_file.exists():
            std_dev = np.array([0])
        else:
            input_data = np.load(std_dev_file)
            std_dev =input_data['arr_0']
     
        if std_dev.shape == (1,):
            std_dev = std_dev[0]
        else:
            std_dev = std_dev

        new_row_data['std_dev'] = float(std_dev)

        ###################################################
        ###### STD DEVIATION PER LAYER ######
        ###################################################

        std_dev_file_per_layer = Path(benchmark, 'per_layer_timings_std_dev.npz')
        
        # In this case, the layer timings are derived from random samples for reach repetition
        # Create the standard deviation over the number repetitions (axis=0)
        if not std_dev_file_per_layer.exists():
            std_dev_per_layer = np.std(new_row_data['per_layer_timings'], axis=0)
        # In this case, the layer timings are derived from tensors of the data set
        # Each tensor was processed number of repetitions times
        # The std_dev_file_per_layer contains the standard deviation over the data set tensors
        # Now create the weighted average of the standard deviations,
        # to combine the two sources (repetitions and data set tensors)
        else:
            input_data = np.load(std_dev_file_per_layer)
            std_dev_per_layer =input_data['arr_0']
            divisor = std_dev_per_layer.shape[0]
            squared_sum = np.sum(np.square(std_dev_per_layer), axis=-0)
            std_dev_per_layer = np.sqrt(squared_sum / divisor)

        if std_dev_per_layer.shape == (1,):
            std_dev_per_layer = std_dev_per_layer[0]
        else:
            std_dev_per_layer = std_dev_per_layer

        assert len(std_dev_per_layer.shape) == 1 and std_dev_per_layer.shape[-1] == new_row_data['per_layer_timings'].shape[-1], 'Invalid shape for std_dev_per_layer.'
        new_row_data['std_dev_per_layer'] = std_dev_per_layer
        
        ##################################################
        ####           Insert Ram & Flash             ####
        ##################################################

        mean_timings = Path(benchmark, 'ram_flash.txt')
        assert mean_timings.exists(), 'No ram, flash found.'
        
        with open(mean_timings, 'r') as f:
            lines = f.readlines()
        
        ram = lines[0].strip().split(' ')[-1]
        flash = lines[1].strip().split(' ')[-1]
        new_row_data['ram'] = int(ram)
        new_row_data['flash'] = int(flash)

        ##################################################
        #### Ram & Flash specifics .data .rodata .bss ####
        ##################################################

        # We dont have the individual sizes for the tflite models, 
        # ram and flash are extracted from simple network analyze report
        if 'tflite' in benchmark.stem:
            new_row_data['elf_size'] = None
        # ST offers a more detailed generate_report.txt log file
        elif 'st' in benchmark.stem:
            generate_report_file = Path(benchmark, 'workdir', 'generate_report.txt')
            assert generate_report_file.exists(), 'No generate_report.txt found.'
            elf_size_dict = get_bss_data_rodata_text_st(generate_report_file)
            new_row_data['elf_size'] = elf_size_dict
        # for glow and tiny_engine we can use the elf file to extract the sizes manually
        elif 'glow' in benchmark.stem or 'tiny_engine' in benchmark.stem:
            if 'glow' in benchmark.stem:
                elf_ref_file = Path(benchmark, 'workdir', 'Glow_Template_ref', 'Debug', 'Glow_Template_ref.elf')
                elf_empty_file = Path(benchmark, 'workdir', 'Glow_Template_empty', 'Debug', 'Glow_Template_empty.elf')
                assert elf_ref_file.exists(), 'No ref elf file found.'
                assert elf_empty_file.exists(), 'No empty elf file found.'
            elif 'tiny_engine' in benchmark.stem:
                elf_ref_file = Path(benchmark, 'workdir', 'TinyEngineTemplateCleanR5Zi_ref', 'Debug', 'TinyEngineTemplateCleanR5Zi.elf')
                elf_empty_file = Path(benchmark, 'workdir', 'TinyEngineTemplateCleanR5Zi_ref_empty', 'Debug', 'TinyEngineTemplateCleanR5Zi.elf')
                assert elf_ref_file.exists(), 'No ref elf file found.'
                assert elf_empty_file.exists(), 'No empty elf file found.'
            
            # execute 'arm-none-eabi-size -A <elf>' using subprocess
            eabi_size_ref = subprocess.run(['arm-none-eabi-size', '-A', elf_ref_file], stdout=subprocess.PIPE).stdout.decode('utf-8')
            eabi_size_empty = subprocess.run(['arm-none-eabi-size', '-A', elf_empty_file], stdout=subprocess.PIPE).stdout.decode('utf-8')
            elf_size_dict = get_bss_data_rodata_text(eabi_size_ref, eabi_size_empty)
            new_row_data['elf_size'] = elf_size_dict
        if not 'tflite' in benchmark.stem:
            print(new_row_data['elf_size'])

        
        #################################################
        ####            Calulate Errors              ####
        #################################################

        # load reference data
        ref_data = Path(benchmark, 'ref_tensor_values.npz')
        assert ref_data.exists(), 'No reference data found.'
        ref_data = np.load(ref_data)
        ref_tensor_values = ref_data['arr_0']
        # load mcu data
        mcu_data = Path(benchmark, 'mcu_tensor_values.npz')
        assert mcu_data.exists(), 'No mcu data found.'
        mcu_data = np.load(mcu_data)
        mcu_tensor_values = mcu_data['arr_0']
        # calculate metrics
        metrics = data_metrics(mcu_tensor_values, ref_tensor_values)
        new_row_data['mcu_tensor_values'] = mcu_tensor_values
        new_row_data['ref_tensor_values'] = ref_tensor_values
        new_row_data['rmse'] = metrics['rmse']
        new_row_data['mae'] = metrics['mae']
        new_row_data['l2r'] = metrics['l2r']
        new_row_data['nrmse'] = metrics['nrmse']

        # add the new row to the df
        df.loc[len(df)] = new_row_data
    

    ############# Process per layer data:
    # Optimisation techniques split or fuse layers
    # in this step correspond the layers to the original (tflite) model layers
    # e.g., if the original model has 10 layers, but the optimised model has 20 layers,
    # probably 1 layer was split into 2 layers, so the first 2 layers of the optimised model
    # correspond to the first layer of the original model.
    # This analysis is done manually


    # Original AD model has 10 layers
    layer_assignment_ad_10 = [{0: (0), 1: (1), 2: (2), 3: (3), 4: (4), 5: (5), 6: (6), 7: (7), 8: (8), 9: (9)}]
    layer_assignment_ad_19 = [{0: (0,1), 1: (2,3), 2: (4,5), 3: (6,7), 4: (8,9), 5: (10,11), 6: (12,13), 7: (14,15), 8: (16,17), 9: (18)}]

    # Original KWS model has 13 layers
    layer_assignment_kws_11 = [{0: (0), 1: (1), 2: (2), 3: (3), 4: (4), 5: (5), 6: (6), 7: (7), 8: (8), 9: (8), 10: (9), 11: (9), 12: (10)}]
    layer_assignment_kws_12 = [{0: (0), 1: (1), 2: (2), 3: (3), 4: (4), 5: (5), 6: (6), 7: (7), 8: (8), 9: (9), 10: (10), 11: (10), 12: (11)}]
    layer_assignment_kws_13 = [{0: (0), 1: (1), 2: (2), 3: (3), 4: (4), 5: (5), 6: (6), 7: (7), 8: (8), 9: (9), 10: (10), 11: (11), 12: (12)}]
    layer_assignment_kws_16 = [{0: (0,1), 1: (2), 2: (3,4), 3: (5), 4: (6,7), 5: (8), 6: (9,10), 7: (11), 8: (12), 9: (13), 10: (14), 11: (14), 12: (15)}]
    layer_assignment_kws_21 = [{0: (0,1), 1: (2,3), 2: (4,5), 3: (6,7), 4: (8,9), 5: (10,11), 6: (12,13), 7: (14,15), 8: (16,17), 9: (18), 10: (19), 11: (19), 12: (20)}]
    layer_assignment_kws_24 = [{0: (0,1,2), 1: (3,4), 2: (5,6), 3: (7,8), 4: (9,10), 5: (11,12), 6: (13,14), 7: (15,16), 8: (17,18), 9: (19,20), 10: (21), 11: (21), 12: (22,23)}]

    # Original IC model has 16 layers
    layer_assignment_ic_15 = [{0: (0), 1: (1), 2: (2), 3: (3), 4: (4), 5: (5), 6: (6), 7: (7), 8: (8), 9: (9), 10: (10), 11: (11), 12: (12), 13: (13), 14: (13), 15: (14)}]
    layer_assignment_ic_16 = [{0: (0), 1: (1), 2: (2), 3: (3), 4: (4), 5: (5), 6: (6), 7: (7), 8: (8), 9: (9), 10: (10), 11: (11), 12: (12), 13: (13), 14: (14), 15: (15)}]
    layer_assignment_ic_17 = [{0: (0), 1: (1), 2: (2), 3: (3), 4: (5), 5: (6, 7), 6: (4), 7: (8), 8: (10), 9: (11, 12), 10: (9), 11: (13), 12: (14), 13: (15), 14: (15), 15: (16)}]
    layer_assignment_ic_18 = [{0: (0), 1: (1), 2: (2), 3: (3,4), 4: (6), 5: (7), 6: (5), 7: (8,9), 8: (11), 9: (12), 10: (10), 11: (13,14), 12: (15), 13: (16), 14: (16), 15: (17)}]
    layer_assignment_ic_21 = [{0: (0), 1: (1,2), 2: (3,4), 3: (5), 4: (6,7), 5: (8,9), 6: (10), 7: (11), 8: (12,13), 9: (14,15), 10: (16), 11: (17), 12: (18), 13: (19), 14: (19), 15: (20)}]
    layer_assignment_ic_22 = [{0: (0,1), 1: (2,3), 2: (4), 3: (5,6), 4: (8,9), 5: (10), 6: (7), 7: (11,12), 8: (14,15), 9: (16), 10: (13), 11: (17,18), 12: (19), 13: (20), 14: (20), 15: (21)}]
    layer_assignemnt_ic_25 = [{0: (0,1,2), 1: (3,4), 2: (5), 3: (6,7), 4: (9,10), 5: (11), 6: (8), 7: (12,13), 8: (15,16), 9: (17), 10: (14), 11: (18,19), 12: (20,21), 13: (22), 14: (22), 15: (23,24)}]

    # Original VWW model has 31 layers
    layer_assignment_vww_29 = [{0: (0), 1: (1), 2: (2), 3: (3), 4: (4), 5: (5), 6: (6), 7: (7), 8: (8), 9: (9), 10: (10), 11: (11), 12: (12), 13: (13), 14: (14), 15: (15), 16: (16), 17: (17), 18: (18), 19: (19), 20: (20), 21: (21), 22: (22), 23: (23), 24: (24), 25: (25), 26: (26), 27: (27), 28: (28), 29: (28), 30: (28)}]
    layer_assignment_vww_30 = [{0: (0), 1: (1), 2: (2), 3: (3), 4: (4), 5: (5), 6: (6), 7: (7), 8: (8), 9: (9), 10: (10), 11: (11), 12: (12), 13: (13), 14: (14), 15: (15), 16: (16), 17: (17), 18: (18), 19: (19), 20: (20), 21: (21), 22: (22), 23: (23), 24: (24), 25: (25), 26: (26), 27: (27), 28: (28), 29: (28), 30: (29)}]
    layer_assignment_vww_31 = [{0: (0), 1: (1), 2: (2), 3: (3), 4: (4), 5: (5), 6: (6), 7: (7), 8: (8), 9: (9), 10: (10), 11: (11), 12: (12), 13: (13), 14: (14), 15: (15), 16: (16), 17: (17), 18: (18), 19: (19), 20: (20), 21: (21), 22: (22), 23: (23), 24: (24), 25: (25), 26: (26), 27: (27), 28: (28), 29: (29), 30: (30)}]
    layer_assignment_vww_43 = [{0: (0), 1: (1,2), 2: (3), 3: (4,5), 4: (6), 5: (7,8), 6: (9), 7: (10,11), 8: (12), 9: (13,14), 10: (15), 11: (16,17), 12: (18), 13: (19,20), 14: (21), 15: (22,23), 16: (24), 17: (25,26), 18: (27), 19: (28,29), 20: (30), 21: (31,32), 22: (33), 23: (34,35), 24: (36), 25: (37,38), 26: (39), 27: (40), 28: (41), 29: (41), 30: (42)}]
    layer_assignment_vww_57 = [{0: (0,1), 1: (2,3), 2: (4,5), 3: (6,7), 4: (8,9), 5: (10,11), 6: (12,13), 7: (14,15), 8: (16,17), 9: (18,19), 10: (20,21), 11: (22,23), 12: (24,25), 13: (26,27), 14: (28,29), 15: (30,31), 16: (32,33), 17: (34,35), 18: (36,37), 19: (38,39), 20: (40,41), 21: (42,43), 22: (44,45), 23: (46,47), 24: (48,49), 25: (50,51), 26: (52,53), 27: (54), 28: (55), 29: (55), 30: (56)}]


    for index, row in df.iterrows():
        config_name = row["config_name"]
        layer_number = row["per_layer_timings"].shape
    
        if row['model'] == 'ad':
            if layer_number[-1] == 10:
                df.at[index, 'layer_assignments'] = layer_assignment_ad_10
            elif layer_number[-1] == 19:
                df.at[index, 'layer_assignments'] = layer_assignment_ad_19
            df.at[index, 'ref_config_name'] = 'tflite_ad_normal_int_'

        if row['model'] == 'kws':
            if 'nosoftmax' in config_name:
                # ignore all models without softmax
                continue
            else:
                if layer_number[-1] == 11:
                    df.at[index, 'layer_assignments'] = layer_assignment_kws_11
                elif layer_number[-1] == 12:
                    df.at[index, 'layer_assignments'] = layer_assignment_kws_12
                elif layer_number[-1] == 13:
                    df.at[index, 'layer_assignments'] = layer_assignment_kws_13
                elif layer_number[-1] == 16:
                    df.at[index, 'layer_assignments'] = layer_assignment_kws_16
                elif layer_number[-1] == 21:
                    df.at[index, 'layer_assignments'] = layer_assignment_kws_21
                elif layer_number[-1] == 24:
                    df.at[index, 'layer_assignments'] = layer_assignment_kws_24
                df.at[index, 'ref_config_name'] = 'tflite_kws_int_'

        if row['model'] == 'ic':
            if 'nosoftmax' in config_name:
                # ignore all models without softmax
                continue
            else:
                if layer_number[-1] == 15:
                    df.at[index, 'layer_assignments'] = layer_assignment_ic_15
                elif layer_number[-1] == 16:
                    df.at[index, 'layer_assignments'] = layer_assignment_ic_16
                elif layer_number[-1] == 17:
                    df.at[index, 'layer_assignments'] = layer_assignment_ic_17
                elif layer_number[-1] == 18:
                    df.at[index, 'layer_assignments'] = [layer_assignment_ic_18]
                elif layer_number[-1] == 21:
                    df.at[index, 'layer_assignments'] = layer_assignment_ic_21
                elif layer_number[-1] == 22:
                    df.at[index, 'layer_assignments'] = layer_assignment_ic_22
                elif layer_number[-1] == 25:
                    df.at[index, 'layer_assignments'] = layer_assignemnt_ic_25
                df.at[index, 'ref_config_name'] = 'tflite_ic_int_'
                

        if row['model'] == 'vww':
            if 'nosoftmax' in config_name:
                # ignore all models without softmax except vww tiny engine, 
                # because we are interested in the speedup of the depthwise convolutions
                if 'tiny_engine' in config_name and layer_number[-1] == 29:
                    df.at[index, 'layer_assignments'] = layer_assignment_vww_29
                    df.at[index, 'ref_config_name'] = 'tflite_vww_int_'
                else:
                    continue
            else:
                if layer_number[-1] == 30:
                    df.at[index, 'layer_assignments'] = layer_assignment_vww_30
                elif layer_number[-1] == 31:
                    df.at[index, 'layer_assignments'] = layer_assignment_vww_31
                elif layer_number[-1] == 43:
                    df.at[index, 'layer_assignments'] = layer_assignment_vww_43
                elif layer_number[-1] == 57:
                    df.at[index, 'layer_assignments'] = layer_assignment_vww_57
                df.at[index, 'ref_config_name'] = 'tflite_vww_int_'
    
    return df

def get_bss_data_rodata_text_st(generate_report_file: Path) -> dict:
    with open(generate_report_file, 'r') as f:
        lines = f.readlines()
    
    elf_size_dict = {}
    line_minus_2 = ''
    line_minus_1 = ''
    for line in lines:
        if 'TOTAL' in line and '*io*' in line_minus_2:
            line_split = line.split()
            elf_size_dict['text'] = line_split[-4]
            elf_size_dict['rodata'] = line_split[-3]
            elf_size_dict['data'] = line_split[-2]
            elf_size_dict['bss'] = line_split[-1]
            return elf_size_dict
        line_minus_2 = line_minus_1
        line_minus_1 = line

    # Failure to find flash and ram if we rech this point
    return None


def get_bss_data_rodata_text(elf_size_ref: str, elf_size_empty: str) -> dict:
    """Extracts the .bss, .data and .rodata size from the output of 'arm-none-eabi-size -A' command.

    Args:
        elf_size_ref (str): The output of 'arm-none-eabi-size' command for the reference elf file (project compiled including ML model).
        elf_size_empty (str): The output of 'arm-none-eabi-size' command for the empty elf file (project compiled without ML model).

    Returns:
        dict: A dictionary containing the .bss, .data and .rodata size.
    """
    # Define the regular expression patterns for the sections and sizes
    pattern_text = r"\.text\s+(\d+)"
    pattern_data = r"\.data\s+(\d+)"
    pattern_rodata = r"\.rodata\s+(\d+)"
    pattern_bss = r"\.bss\s+(\d+)"

    # rodata, read only data
    # text is code
    # data is read write data
    # bss is uninitialized data / zero initialized data

    text_size_ref = re.findall(pattern_text, elf_size_ref)
    text_size_empty = re.findall(pattern_text, elf_size_empty)
    text_size = int(text_size_ref[0]) - int(text_size_empty[0])

    rodata_size_ref = re.findall(pattern_rodata, elf_size_ref)
    rodata_size_empty = re.findall(pattern_rodata, elf_size_empty)
    rodata_size = int(rodata_size_ref[0]) - int(rodata_size_empty[0])

    data_size_ref = re.findall(pattern_data, elf_size_ref)
    data_size_empty = re.findall(pattern_data, elf_size_empty)
    data_size = int(data_size_ref[0]) - int(data_size_empty[0])

    bss_size_ref = re.findall(pattern_bss, elf_size_ref)
    bss_size_empty = re.findall(pattern_bss, elf_size_empty)
    bss_size = int(bss_size_ref[0]) - int(bss_size_empty[0])

    return {'text': text_size, 'rodata': rodata_size, 'data': data_size, 'bss': bss_size}


def export_latex_table(df, usecase='ad', dtype='int'):
    """Exports a pandas dataframe to a latex table.

    Args:
        df (pd.DataFrame): The dataframe to be exported.
        usecase (str, optional): The usecase to be exported. 
            Valid values: 'ad', 'kws', 'vww', 'ic'. Defaults to 'ad'.
        dtype (str, optional): The data type to be exported. 
            Valid values: 'int' or 'float'. Defaults to 'int'.
    """
    assert dtype in ['int', 'float'], f'Invalid dtype {dtype}.'
    assert usecase in ['ad', 'kws', 'vww', 'ic'], f'Invalid usecase {usecase}.'
    df = df[df['model'] == usecase]
    df = df[df['dtype'] == dtype]

    # only keep the relevant columns: model, config_name, framework, avg_timing
    df = df[['model', 'framework', 'avg_timing', 'config_name']]
    # round the avg_timing to 2 decimal places
    for index, row in df.iterrows():
        df.at[index, 'avg_timing'] = round(float(row['avg_timing']), 3)
    # if dtype is float and config_name contains 'nosoftmax', delete the row
    if dtype == 'float':
        df = df[~df['config_name'].str.contains('nosoftmax')]
    # if config_name contains 'anomaly', delete the row
    df = df[~df['config_name'].str.contains('anomaly')]
    # if config_name contains 'normal', remove the 'normal' part
    df['config_name'] = df['config_name'].str.replace('_normal_', '_')
    # replace all underscores with a - and remove last underscore from config_name
    df['config_name'] = df['config_name'].str.replace('_', '-').str[:-1]
    df['framework'] = df['framework'].str.replace('_', '-')
    # sort by avg_timing
    df = df.sort_values(by='avg_timing', ascending=True)
    # replace _ in header names
    df.columns = ['Model', 'Framework', 'Avg. Timing [ms]', 'Config Name']

    print(df.to_latex(index=False, float_format='%.3f'))
    print()
    return
    


def layer_perf_by_type(df):
    """Analyses the performance of layer types per framwork.

    The hypothesis is that some frameworks have perticular strengths in optimizing certain layer types.
    By comparing the performance of layer types across different frameworks, over all use cases,
    we can identify these well-optimized layers.

    """


    # get possible layer types in all models
    # filter only int dtype, we cannot compare float to a int reference
    df = df[df['dtype'] == 'int']

    layer_types = set()
    for index, row in df.iterrows():
        if "noquant" in row['config_name'] and "float" in row['config_name']:
            continue
        if "_quant" not in row['config_name'] and "float" in row['config_name']:
            continue
        # filter 'nan' values
        if type(row['ref_config_name']) == float:
            continue
        ref_row = (df[df['config_name'] == row['ref_config_name']]).iloc[0]
        ref_timings = np.mean(ref_row['per_layer_timings'], axis=0)
        layer_names_ref = ref_row['layer_names']
        for i in range(len(ref_timings)):
            layer_types.add(layer_names_ref[i])

    # create a dictionary for each framework, saving the relative performance of each layer type
    layer_dict = {}
    for layer in layer_types:
        layer_dict[layer] = {'total': 0, 'count': 0, 'relative': 0.0}
    glow_dict = copy.deepcopy(layer_dict)
    st_dict = copy.deepcopy(layer_dict)
    tiny_engine_dict = copy.deepcopy(layer_dict)
    
    continue_flag = False
    for index, row in df.iterrows():
        continue_flag = False
        if "noquant" in row['config_name'] and "float" in row['config_name']:
            continue
        if "_quant" not in row['config_name'] and "float" in row['config_name']:
            continue
        if "tflite" in row['config_name']:
            continue
        # filter 'nan' values
        if type(row['ref_config_name']) == float:
            continue
        else:
            ref_row = (df[df['config_name'] == row['ref_config_name']]).iloc[0]
            
            layer_assignment = row['layer_assignments']

            timings = np.mean(row['per_layer_timings'], axis=0)
            ref_timings = np.mean(ref_row['per_layer_timings'], axis=0)

            total_runtime = sum(timings)
            total_runtime_ref = sum(ref_timings)

            # extract the corresponding timings for each layer type
            layer_names_ref = ref_row['layer_names']

            layer_type_set = set(layer_names_ref)
            type_timing_dict = {}
            for layer_type in layer_type_set:
                type_timing_dict[layer_type] = {'ref': 0.0, 'target': 0.0}

            for i, name in enumerate(layer_names_ref):
                if i >= len(ref_timings):
                    break
                ref_timing = ref_timings[i]
                if (type(layer_assignment) == float):
                    print(row["config_name"], "SKIPPING DUE TO MISSING LAYER ASSIGNMENT {}".format(row['config_name']))
                    continue_flag = True
                    break
                corresponding_layers = layer_assignment[0][i]
                corresponding_sum = 0.0
                if type(corresponding_layers) == int:
                    corresponding_sum = timings[corresponding_layers]
                else:
                    for timing in corresponding_layers:
                        corresponding_sum += timings[timing]
                type_timing_dict[name]['ref'] += ref_timing
                type_timing_dict[name]['target'] += corresponding_sum
            if continue_flag:
                continue
            
            #print("type_timing_dict: ", type_timing_dict)

            for layer_type in type_timing_dict:
                if row['framework'] == 'glow':
                    glow_dict[layer_type]['total'] += type_timing_dict[layer_type]['target'] / type_timing_dict[layer_type]['ref']
                    glow_dict[layer_type]['count'] += 1
                if row['framework'] == 'st':
                    st_dict[layer_type]['total'] += type_timing_dict[layer_type]['target'] / type_timing_dict[layer_type]['ref']
                    st_dict[layer_type]['count'] += 1
                if row['framework'] == 'tiny_engine':
                    tiny_engine_dict[layer_type]['total'] += type_timing_dict[layer_type]['target'] / type_timing_dict[layer_type]['ref']
                    tiny_engine_dict[layer_type]['count'] += 1

    dicts_to_plot = [glow_dict, st_dict, tiny_engine_dict]
    titles = ['Glow', 'ST', 'Tiny Engine']
    # save the relative performance of each layer type
    for dict_ in dicts_to_plot:
        for layer_type in dict_:
            if dict_[layer_type]['count'] == 0:
                continue
            metric = dict_[layer_type]['total'] / dict_[layer_type]['count']
            dict_[layer_type]['relative'] = metric

    # now plot the relative performance of each layer type
    i = 0
    for dict_ in dicts_to_plot:
        # Define colors based on values
        colors = []
        relative_runtimes = []
        ref_names = []
        for key in dict_.keys():
            # check if count is 0
            if dict_[key]['count'] == 0:
                continue
            ref_names.append(key)
            relative_runtimes.append(dict_[key]['relative'])
            if dict_[key]['relative'] > 1:
                colors.append('red')
            else:
                colors.append('green')

        # convert to percentage
        relative_runtimes = [((1 - value) * 100) * -1 if value < 1 else (value - 1) * 100 for value in relative_runtimes]

        # Create a bar chart
        fig = px.bar(
            x=ref_names, 
            y=relative_runtimes, 
            color=colors,
            color_discrete_map={color: color for name, color in zip(ref_names, colors)},
            text_auto='.1f', 
            title="Relative Speedup per Layer",
            category_orders={"x": ref_names}
            )
        
        fig.update_layout(
            title=f"Relative Speedup of {titles[i]} Layer Types compared to TFLite Layer Types",
            xaxis_title="Reference Layer Name",
            yaxis_title="Relative Speedup Factor",
            bargap=0.1,
        )
        fig.show()
        i+=1

         
            

def read_layer_names(layer_names_txt):
    with open(layer_names_txt, 'r') as f:
        lines = f.readlines()
    layer_names = []
    for line in lines:
        layer_names.append(line.strip())
    return layer_names


def data_metrics(tensor_values, tensor_values_ref):
    tensor_values = tensor_values.astype(np.float64)
    tensor_values_ref = tensor_values_ref.astype(np.float64)

    return_metrics = {}
    return_metrics['rmse'] = rmse(tensor_values_ref, tensor_values)
    return_metrics['mae'] = mae(tensor_values_ref, tensor_values)
    return_metrics['l2r'] = l2r(tensor_values_ref, tensor_values)
    return_metrics['nrmse'] = nrmse(tensor_values_ref, tensor_values)

    return return_metrics


def plot_sankey(title: str, source_data: pd.Series, target_data: pd.Series):
    assert type(target_data['layer_assignments']) == list, 'Layer assignment must exist.'
    layer_assignment = target_data['layer_assignments']

    ref_title = source_data['config_name']
    target_title = target_data['config_name']

    reference_timings = source_data['per_layer_timings']
    reference_timings = np.mean(reference_timings, axis=0)
    target_timings = target_data['per_layer_timings']
    target_timings = np.mean(target_timings, axis=0)

    ref_names = source_data['layer_names'][:len(reference_timings)]
    target_names = target_data['layer_names']

    ref_avg_runtime = np.mean(source_data['avg_timing']).round(3)
    target_avg_runtime = np.mean(target_data['avg_timing']).round(3)

    # preprocessing: apply character limit to layer names
    CHAR_LIMIT = 50
    if 'glow' in ref_title:
        ref_names = process_glow_layer_names(ref_names)
    else:
        ref_names = [name[:CHAR_LIMIT] for name in ref_names]
    if 'glow' in target_title:
        target_names = process_glow_layer_names(target_names)
    else:
        target_names = [name[:CHAR_LIMIT] for name in target_names]
    
    # Extract source and target nodes from the data structure
    ref_len = len(ref_names)
    target_len = len(target_names)

            #[ref_title + '  ' + str(ref_avg_runtime) + ' ms'] + \
    labels = [str(ref_avg_runtime) + ' ms'] + \
        ref_names + \
        target_names + \
        [target_title, str(target_avg_runtime) + ' ms']
       #[target_title, target_title + '  ' + str(target_avg_runtime) + ' ms']

    # get the total runtime for all layers
    ref_total_runtime = reference_timings.sum()
    target_total_runtime = target_timings.sum()

    # source nodes are displayed to the left of a link in a sankey diagram
    source_nodes = []
    # target nodes are displayed to the right of a link in a sankey diagram
    target_nodes = []

    # here we create a sankey diagram with 4 layers of nodes and 3 layers of links in between
    values = []
    max_timings = []

    for mapping in layer_assignment :
        for source, targets in mapping.items():
            # extract the timing value of the tflite reference layer
            source_value = reference_timings[source]

            # add reference link weights
            values.append(source_value)

            # add source link in first step
            source_nodes.append(-1)
            target_nodes.append(source)

            # now process the one to many relation to target layers
            if type(targets) != tuple:
                targets = (targets,)

            # Extract the larger runtime (either ref or target) to scale the buffer space
            target_sum = 0
            
            for target in targets:
                # add target link weights
                target_value = target_timings[target]
                target_sum += target_value

                # add middle link in second step
                source_nodes.append(source)
                target_nodes.append(target + ref_len)
                values.append(target_value)
                # add target link in third step
                source_nodes.append(target + ref_len)
                target_nodes.append(ref_len + target_len + 1)
                values.append(target_value)

            max_timings.append(max(source_value, target_sum))

            continue

    #values = [ref_total_runtime] + values + [target_total_runtime]
    source_nodes = [node + 1 for node in source_nodes]
    target_nodes = [node + 1 for node in target_nodes]

    x_vals = []
    y_vals1 = []
    y_vals2 = []

    max_runtime = max(ref_total_runtime, target_total_runtime)

    buffer_space_ref = max_runtime / (len(ref_names) - 1)
    buffer_space_target = max_runtime / (len(target_names) - 1)

    # y coordinates for ref nodes
    y_sum = 0.
    for timing in max_timings:
        y_vals1.append(y_sum + (timing / 1.5))
        y_sum += timing + buffer_space_ref
    x_vals = x_vals + [0.4] * len(reference_timings)
    y_vals1 = np.array(y_vals1)

    # y coordinates for target nodes
    y_sum = 0.
    for timing in target_timings:
        y_vals2.append(y_sum + timing / 2.)
        y_sum += timing + buffer_space_target
    x_vals = x_vals + [0.6] * len(target_timings)
    y_vals2 = np.array(y_vals2)

    # normalize y coordinates [0.0, 1.0]
    y_vals1 = y_vals1 / np.max(y_vals1)
    y_vals2 = y_vals2 / np.max(y_vals2)

    y_vals = np.concatenate(([0.5], y_vals1, y_vals2, [0.5]))
    y_sum = y_vals.sum()
    y_vals = y_vals.tolist()

    # add the reference and target total runtime nodes to x coordinates
    x_vals = [0.2] + x_vals + [0.8]

    # Create a Plotly Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=labels,
            x=x_vals,
            y=y_vals
        ),
        link=dict(
            source=source_nodes,
            target=target_nodes,
            value=values
        )
    )])
    fig.update_layout(title_text=title, font_size=10)
    fig.show()
    return


# Preprocess layer names for glow framework,
# so that they are visible in diagrams
def process_glow_layer_names(layer_names):
    new_names = []
    for layer_name in layer_names:
        layer_name_segments = layer_name.split('_')
        # Glow copies the unclear tflite layer naming scheme and appends its own layer name
        # So just take the last two segments of the layer name, generated by glow
        if len(layer_name_segments) > 2:
            new_name = layer_name_segments[-3] + '_' + layer_name_segments[-2] + '_' + layer_name_segments[-1]
            new_names.append(new_name)
        else:
            new_names.append(layer_name)
    return new_names


#def plot_speedup(title: str, ref_title: str, target_title: str, layer_assignment: list, ref_names: list, reference_timings: np.array, target_names: list ,target_timings: np.array):
def plot_speedup(title: str, source_data: pd.Series, target_data: pd.Series):                
    assert type(target_data['layer_assignments']) == list, 'Layer assignment must exist.'
    layer_assignment = target_data['layer_assignments']

    ref_title = source_data['config_name']
    target_title = target_data['config_name']

    reference_timings = source_data['per_layer_timings']
    reference_timings = np.mean(reference_timings, axis=0)
    target_timings = target_data['per_layer_timings']
    target_timings = np.mean(target_timings, axis=0)

    ref_names = source_data['layer_names'][:len(reference_timings)]
    target_names = target_data['layer_names']
    
    # preprocessing: apply character limit to layer names
    CHAR_LIMIT = 50
    if 'glow' in ref_title:
        ref_names = process_glow_layer_names(ref_names)
    else:
        ref_names = [name[:CHAR_LIMIT] for name in ref_names]
    if 'glow' in target_title:
        target_names = process_glow_layer_names(target_names)
    else:
        target_names = [name[:CHAR_LIMIT] for name in target_names]
    
    # source nodes are displayed to the left of a link in a sankey diagram
    relative_runtimes = []
    absolute_runtimes = []

    for mapping in layer_assignment :
        for source, targets in mapping.items():
            # extract the timing value of the tflite reference layer
            source_value = reference_timings[source]

            # now process the one to many relation to target layers
            if type(targets) != tuple:
                targets = (targets,)

            # Extract the larger runtime (either ref or target) to scale the buffer space
            target_sum = 0
            
            for target in targets:
                # add target link weights
                target_value = target_timings[target]
                target_sum += target_value

            # process relative speedup
            if source_value / target_sum > 1:
                relative_change_percent = -((source_value / target_sum) - 1 )
            else:
                relative_change_percent = ((target_sum / source_value) - 1 )

            relative_runtimes.append(relative_change_percent)
            absolute_runtimes.append( - (source_value - target_sum))
    
    # Define colors based on values
    colors = ['red' if val > 0 else 'green' for val in relative_runtimes]
    
    
    new_ref_names = []
    for i, name in enumerate(ref_names):
        new_ref_names.append(f'{i+1}: ' + name)
    ref_names = new_ref_names

    # Create a relative speedup bar chart
    # RELATIVE SPEEDUP IS NOT REPRESENTATIVE
    fig = px.bar(
        x=ref_names, 
        y=relative_runtimes, 
        color=colors,
        color_discrete_map={color: color for name, color in zip(ref_names, colors)},
        text_auto='.1f', 
        title="Relative Speedup per Layer",
        category_orders={"x": ref_names},
        )
    
    fig.update_layout(
        title=f"Relative Speedup of {target_title} per Layer compared to reference {ref_title}",
        xaxis_title="Reference Layer Name",
        yaxis_title="Relative Speedup Factor",
        bargap=0.1,
    )
    fig.show()

    # Define colors based on values
    colors = ['red' if val > 0 else 'green' for val in absolute_runtimes]

    # Create a absolute speedup bar chart
    fig = px.bar(
        x=ref_names, 
        y=absolute_runtimes, 
        color=colors,
        color_discrete_map={color: color for name, color in zip(ref_names, colors)},
        text_auto='.2f', 
        title="Absolute Speedup per Layer",
        category_orders={"x": ref_names}
        )
    
    fig.update_layout(
        title=f"Absolote Speedup of {target_title} per Layer compared to reference {ref_title}",
        xaxis_title="Reference Layer Name",
        yaxis_title="Runtime Speedup (green) or Slowdown (red) [ms]",
        bargap=0.1,
    )
    fig.show()
    return


def plot_pareto3d(title: str, df: pd.DataFrame):
    data = {
        'ram': [],
        'flash': [],
        'timing': [],
        'framework': [],
        'shape': [],
        'color': [],
        'label': []
    }

    for index, row in df.iterrows():
        # if row['framework'] == 'tiny_engine':
        #     continue
        # if 'nosoftmax' in row['config_name']:
        #     continue

        data['ram'].append(row['ram'])
        data['flash'].append(row['flash'])
        data['timing'].append(float(row['avg_timing']))
        data['framework'].append(row['framework'])
        data['label'].append(row['config_name'])

    # assign a shape to each data point for the plotly 3d scatter plot
    for i, framework in enumerate(data['framework']):
        if framework == 'tiny_engine':
            data['shape'].append('tiny_engine')
        elif framework == 'st':
            data['shape'].append('st')
        elif framework == 'glow':
            data['shape'].append('glow')
        elif framework == 'tflite':
            data['shape'].append('tflite')
        data['color'].append('#FF0000')

    pareto_dims = pd.DataFrame({'ram': data['ram'], 'flash': data['flash'], 'timing': data['timing']})
    mask = paretoset(pareto_dims, sense=["min", "min", "min"])

    data['color'] = np.array(data['color'])
    data['color'][mask] = '#006400'
    data['color'] = list(data['color'])

    df2plot = pd.DataFrame(data)

    fig = px.scatter_3d(df2plot, x='ram', y='flash', z='timing', symbol='shape', color='color', color_discrete_map='identity', opacity=0.6, text='label')#, size='size', )

    # Set the axis range to start from 0
    fig.update_layout(scene=dict(xaxis=dict(range=[0, df2plot['ram'].max()]),
                                xaxis_title='RAM [Byte]',
                                yaxis=dict(range=[0, df2plot['flash'].max()]),
                                yaxis_title='Flash [Byte]',
                                zaxis=dict(range=[0, df2plot['timing'].max()]),
                                zaxis_title='Runtime [ms]'))
    fig.show()
    return


def plot_ram_flash(title: str, df: pd.DataFrame):
    data = {
        'ram': [],
        'flash': [],
        'framework': [],
        'shape': [],
        'color': [],
        'label': [],
        'dtype': []
    }
    for index, row in df.iterrows():
        if 'nosoftmax' in row['config_name'] and not 'tiny_engine' in row['config_name']:
            continue
        data['ram'].append(row['ram'])
        data['flash'].append(row['flash'])
        data['framework'].append(row['framework'])
        data['label'].append(row['config_name'])
        data['dtype'].append(row['dtype'])


    # assign a shape to each data point for the plotly 3d scatter plot
    for i, framework in enumerate(data['framework']):
        if framework == 'tiny_engine':
            data['shape'].append('tiny_engine')
        elif framework == 'st':
            data['shape'].append('st')
        elif framework == 'glow':
            data['shape'].append('glow')
        elif framework == 'tflite':
            data['shape'].append('tflite')
        data['color'].append('#FF0000')

    color_map = {'tiny_engine': 'red', 'st': 'blue', 'glow': 'green', 'tflite': 'black'}

    df2plot = pd.DataFrame(data)
    fig = px.scatter(df2plot, x='ram', y='flash', symbol='shape', color='framework', color_discrete_map=color_map, hover_data=["label", "dtype"])#, text='label')#, size='size', )
    fig.update_layout(
        title=title,
        xaxis=dict(range=[0, df2plot['ram'].max() * 1.1]),
        xaxis_title="RAM [Byte]",
        yaxis=dict(range=[0, df2plot['flash'].max() * 1.1]),
        yaxis_title="Flash [Byte]",
        bargap=0.1,
    )
    fig.show()

def plot_measurement_impact(df: pd.DataFrame):
    """
    Plots the relative impact of per layer runtime measurements.

    Args:
        df (pd.DataFrame): The DataFrame containing the runtime measurements.

    Returns:
        None
    """
    errors = []
    for index, row in df.iterrows():
        layer_sum_timing = row['sum_timing']
        total_ref_timing = row['avg_timing']
        relative_error = (layer_sum_timing / total_ref_timing) - 1
        if abs(relative_error) > 0.005:
            print(row['config_name'], " ", relative_error) 
        errors.append(relative_error)

    # Create a histogram diagram using px
    fig = px.histogram(df, x=errors, title="Relative Impact of per Layer Runtime Measurements")
    fig.update_layout(
        xaxis_title="Relative Impact of per Layer Runtime Measurements",
        yaxis_title="Count",
        bargap=0.1,
    )

    fig.show()


def plot_deviation(df: pd.DataFrame):
    dev_sums = []
    for index, row in df.iterrows():
        if row['framework'] != 'tiny_engine':
            dev_summand = np.sum(row['std_dev_per_layer'])
            dev_sums.append(dev_summand)
        else:
            dev_sums.append(0)
    dev_sums = np.array(dev_sums)

    #get the index of the maximum deviation
    max_dev_idx = np.argmax(dev_sums)
    # get the row in dataframe with the maximum deviation
    max_dev_row = df.iloc[max_dev_idx]
    per_layer_mean = np.mean(max_dev_row['per_layer_timings'], axis=0)
    
    # Create a data frame of the layer names, mean timings and standard deviation
    layer_names = max_dev_row['layer_names']
    config_name = max_dev_row['config_name']
    CHAR_LIMIT = 50
    if 'glow' in config_name:
        layer_names = process_glow_layer_names(layer_names)
    else:
        layer_names = [name[:CHAR_LIMIT] for name in layer_names]
    
    new_names = []
    for i, layer_name in enumerate(layer_names):
        new_names.append(f'{i+1}: ' + f'{layer_name}')
    layer_names = new_names

    layer_df = pd.DataFrame({'layer_names': layer_names, 'mean': per_layer_mean, 'std_dev': max_dev_row['std_dev_per_layer']})
    fig = px.bar(layer_df, 
                 x="layer_names", 
                 y="mean", 
                 error_y="std_dev",
                )
    fig.update_layout(
        title=f"Per layer runtime and Error for {config_name}",
        xaxis_title="Layer Name",
        yaxis_title="Absolute Runtime [ms]",
        bargap=0.1,
    )

    fig.show()
    return


def runtime_over_error(df: pd.DataFrame, use_case: str):
    # create a scatter diagram using px.scatter
    # where the total runtime is on the y-axis and the precision is on the x-axis
    #df['size'] = .2
    # remove any timing over 2000 ms from df (exclude tiny_engine from the plot)

    error_metric = 'nrmse'
    
    out_file = Path.home() / Path('Desktop', 'runtime_over_error_' + use_case + '.txt')
    with open(out_file, 'w') as f:
        for index, row in df.iterrows():
            f.write(row['config_name'] + ' ' + str(row[error_metric]) + ' ' + str(row['sum_timing']) + '\n')
            f.write(str(row['mcu_tensor_values']) + '\n')
            f.write(str(row['ref_tensor_values']) + '\n\n')

    # filter int data type
    #df = df[df['dtype'] == 'int']
    
    # filter all data points where error is > 2
    # bad_df = df[df[error_metric] > 2]
    # print(f"Bad data points for {use_case}: ")
    # for index, row in bad_df.iterrows():
    #     print(row['config_name'], f" {error_metric} error: ", row[error_metric])
    # print()
    # df = df[df[error_metric] < 2]
    

    # create color map for the frameworks
    color_map = {'tiny_engine': 'red', 'st': 'blue', 'glow': 'green', 'tflite': 'black'}
    color_discrete_sequence=["red", "blue", "green", "black"]

    fig = px.scatter(df, x=error_metric, y='sum_timing',color='framework', color_discrete_map=color_map, hover_data=['config_name', 'dtype'])#, size='size')
    fig.update_layout(
        title="Runtime over Error for " + use_case,
        xaxis_title="Root Mean Square Error",
        # xaxis_title="Mean Absolute Error",
        # xaxis_title="L2 Relative Error",
        yaxis_title="Average Runtime [ms]",
        bargap=0.1
    )
    fig.show()
    return

def model_timing_float_st(dp0=2, dp1=3):

    # Define data points
    sources = ['ad', 'kws', 'ic', 'vww']
    timings = [21.2, 307.2, 1006.996, 827.15]
    operations = [
        # smul | op
        [265864, 1032],  # Data point 1: 2 operations of type A, 3 of type B
        [2657356, 79860],  # Data point 2: 1 operation of type A, 4 of type B
        [12501978, 106646],  # Data point 3 (not used for calculating X and Y)
        [7492402, 233886],  # Data point 4 (not used for calculating X and Y)
    ]

    # Select two data points for calculation
    t1 = timings[dp0]
    t2 = timings[dp1]
    opA1, opB1 = operations[dp0]
    opA2, opB2 = operations[dp1]

    tB = (opA1 * t2 - opA2 * t1) / (opA1 * opB2 - opA2 * opB1)
    tA = (t1 - opB1 * tB) / opA1

    print("model ", sources[dp0], sources[dp1])
    print("tA: ", tA)
    print("tB: ", tB)
    print()
    return tA, tB


def model_timing_float_tflite(dp0=0, dp1=1):
    
    # Define data points
    sources = ['ad', 'vww', 'ic']
    timings = [28.2, 18226, 12030]
    operations = [
        # smul | op
        [265864, 1032],  
        [12501978, 106646],
        [7492402, 233886]
       
    ]

    # Select two data points for calculation
    t1 = timings[dp0]
    t2 = timings[dp1]
    opA1, opB1 = operations[dp0]
    opA2, opB2 = operations[dp1]

    tB = (opA1 * t2 - opA2 * t1) / (opA1 * opB2 - opA2 * opB1)
    tA = (t1 - opB1 * tB) / opA1

    print("model ", sources[dp0], sources[dp1])
    print("tA: ", tA)
    print("tB: ", tB)
    print()
    return tA, tB

    


def rmse(ref, pred):
  """Return Root Mean Squared Error (RMSE)."""
  return np.sqrt(((ref - pred).astype(np.float64) ** 2).mean())


def nrmse(ref, pred):
  """Return Root Mean Squared Error (RMSE)."""
  range = np.max(ref) - np.min(ref)
  rmse = np.sqrt(((ref - pred).astype(np.float64) ** 2).mean())
  return rmse / range


def mae(ref, pred):
  """Return Mean Absolute Error (MAE)."""
  return (np.abs(ref - pred).astype(np.float64)).mean()


def l2r(ref, pred):
  """Compute L2 relative error"""
  def magnitude(v):
    return np.sqrt(np.sum(np.square(v).flatten()))
  mag = magnitude(ref) + np.finfo(np.float32).eps
  return magnitude(ref - pred) / mag


def main():
    """Add generated data into one pandas data frame.

    The data is generated by the benchmarking script (main.py) and saved in the data_gen folder.
    The data frame include the following columns:
    - model (ad, kws, vww, ic)
    - framework (tiny_engine, st, glow)
    - dtype (int, float)
    - flash (bytes)
    - ram   (bytes)
    - timings (mean value)
    """
    #################################################################
    ######     Parse generated data into Pandas data frams     ######
    #################################################################

    timings_dir = Path(__file__).parent / Path('..', '..', 'data_gen')

    df = get_data_frame(timings_dir)

    # filtered_df = df[(df['framework'] == 'tiny_engine') & (df['model'] == 'vww')]
    # print(filtered_df)

    ############################################################
    ######     Postprocess data & Perform experiments     ######
    ############################################################
    
    # config = df[df['config_name'] == 'glow_noquant_ic_int_'].iloc[0]
    # config = df[df['config_name'] == 'tiny_engine_vww_int_nosoftmax_'].iloc[0]
    # config = df[df['config_name'] == 'st_ram_ad_anomaly_int_'].iloc[0]
    # ref_row = (df[df['config_name'] == config['ref_config_name']]).iloc[0]
    # print(config['config_name'])
    # print(config['ram'])
    # print(config['flash'])
    # print()
    # print(ref_row['config_name'])
    # print(ref_row['ram'])
    # print(ref_row['flash'])
    # import sys; sys.exit(0)
    #plot_sankey("Per-Layer Runtime Flow", ref_row, config)
    # plot_speedup("Per-Layer Speedup", ref_row, config)
    # export_latex_table(df, 'ic', 'int')

    # indices = []
    # # generate all pairs of combinations for indices [0, 3]
    # for i in range(4):
    #     for j in range(4):
    #         if i < j:
    #             indices.append((i, j))

    # resultsA = []
    # resultsB = []
    # for pair in indices:
    #     A, B = model_timing_float_st(pair[0], pair[1])
    #     resultsA.append(A)
    #     resultsB.append(B)
    # # plot the result in a 1D scatter plot for A, B respectively
    # fig = px.scatter(x=resultsA, y=resultsB)
    # fig.show()



    # indices = []
    # # generate all pairs of combinations for indices [0, 3]
    # for i in range(3):
    #     for j in range(3):
    #         if i < j:
    #             indices.append((i, j))

    # resultsA = []
    # resultsB = []
    # for pair in indices:
    #     A, B = model_timing_float_tflite(pair[0], pair[1])
    #     resultsA.append(A)
    #     resultsB.append(B)
    # # plot the result in a 1D scatter plot for A, B respectively
    # fig = px.scatter(x=resultsA, y=resultsB)
    # fig.show()

    # import sys; sys.exit(0)
    

    # config = df[df['config_name'] == 'st_time_ic_float_'].iloc[0]
    # config = df[df['config_name'] == 'tflite_ic_float_'].iloc[0]

    # reference_timings = config['per_layer_timings']
    # reference_timings = np.mean(reference_timings, axis=0)

    # for i, layer in enumerate(config['layer_names']):
    #     print(reference_timings[i].round(3), "\t", layer )
    # print()
    
    # import sys; sys.exit(0)


    # plot_measurement_impact(df)
    # plot_sankey("Per-Layer Runtime Flow", ref_row, config)

    # config = df[df['config_name'] == 'glow_noquant_kws_int_'].iloc[0]
    # print(config['mcu_tensor_values'])
    # print(config['ref_tensor_values'])

    # import sys;sys.exit(0)
    
    # runtime_over_error(df[df['model'] == 'ad'], "Anomaly Detection")
    # runtime_over_error(df[df['model'] == 'ic'], "Image Classification")
    # runtime_over_error(df[df['model'] == 'kws'], "Keyword Spotting")
    # runtime_over_error(df[df['model'] == 'vww'], "Wake Word Detection")

    # import sys;sys.exit(0)

    # config = df[df['config_name'] == 'st_time_vww_int_'].iloc[0]
    # config = df[df['config_name'] == 'st_time_ic_int_'].iloc[0]
    # config = df[df['config_name'] == 'glow_quant_ic_float_'].iloc[0]
    # config = df[df['config_name'] == 'tiny_engine_vww_int_nosoftmax_'].iloc[0]
    # ref_row = (df[df['config_name'] == config['ref_config_name']]).iloc[0]
    # plot_speedup("Per-Layer Speedup", ref_row, config)
    # #import sys; sys.exit(0)

    # config = df[df['config_name'] == 'st_balanced_ic_int_'].iloc[0]
    # ref_row = (df[df['config_name'] == config['ref_config_name']]).iloc[0]
    # plot_sankey("Per-Layer Runtime Flow", ref_row, config)

    # config = df[df['config_name'] == 'st_time_ic_int_'].iloc[0]
    # ref_row = (df[df['config_name'] == config['ref_config_name']]).iloc[0]
    # plot_sankey("Per-Layer Runtime Flow", ref_row, config)

    # config = df[df['config_name'] == 'st_ram_ic_int_'].iloc[0]
    # ref_row = (df[df['config_name'] == config['ref_config_name']]).iloc[0]
    # plot_sankey("Per-Layer Runtime Flow", ref_row, config)


    

    # import sys;sys.exit(0)
    
    # config = df[df['config_name'] == 'glow_noquant_kws_int_'].iloc[0]
    # ref_row = (df[df['config_name'] == config['ref_config_name']]).iloc[0]
    # plot_sankey("Per-Layer Runtime Flow", ref_row, config)
    # plot_speedup("Per-Layer Speedup", ref_row, config)
    
    # config = df[df['config_name'] == 'glow_quant_kws_float_'].iloc[0]
    # ref_row = (df[df['config_name'] == config['ref_config_name']]).iloc[0]
    # plot_sankey("Per-Layer Runtime Flow", ref_row, config)
    # plot_speedup("Per-Layer Speedup", ref_row, config)
    
    # config = df[df['config_name'] == 'st_time_kws_int_'].iloc[0]
    # ref_row = (df[df['config_name'] == config['ref_config_name']]).iloc[0]
    # plot_sankey("Per-Layer Runtime Flow", ref_row, config)
    # plot_speedup("Per-Layer Speedup", ref_row, config)

    # export_latex_table(df, 'ad', 'int')
    # export_latex_table(df, 'kws', 'int')
    # export_latex_table(df, 'ic', 'int')
    # export_latex_table(df, 'vww', 'int')

    # export_latex_table(df, 'ad', 'float')
    # export_latex_table(df, 'kws', 'float')
    # export_latex_table(df, 'ic', 'float')
    # export_latex_table(df, 'vww', 'float')
    
    # layer_perf_by_type(df)
    
    
    # plot_sankey("Per-Layer Runtime Flow", ref_row, config)
    # plot_speedup("Per-Layer Speedup", ref_row, config)

    # plot pareto diagrams
    int_df = df[df['dtype'] == 'int']
    float_df = df[df['dtype'] == 'float']

    filtered_df_int_ad = int_df[int_df['model'] == 'ad']
    filtered_df_int_kws = int_df[int_df['model'] == 'kws']
    filtered_df_int_ic = int_df[int_df['model'] == 'ic']
    filtered_df_int_vww = int_df[int_df['model'] == 'vww']

    filtered_df_float_ad = float_df[float_df['model'] == 'ad']
    filtered_df_float_kws = float_df[float_df['model'] == 'kws']
    filtered_df_float_ic = float_df[float_df['model'] == 'ic']
    filtered_df_float_vww = float_df[float_df['model'] == 'vww']
    
    
    plot_ram_flash("RAM vs Flash AD int", filtered_df_int_ad)
    plot_ram_flash("RAM vs Flash KWS int", filtered_df_int_kws)
    plot_ram_flash("RAM vs Flash IC int", filtered_df_int_ic)
    plot_ram_flash("RAM vs Flash VWW int", filtered_df_int_vww)
    import sys; sys.exit(0)

    plot_pareto3d("Pareto Diagram AD int", filtered_df_int_ad)
    plot_pareto3d("Pareto Diagram KWS", filtered_df_int_kws)
    plot_pareto3d("Pareto Diagram IC", filtered_df_int_ic)
    plot_pareto3d("Pareto Diagram VWW", filtered_df_int_vww)


    #import sys; sys.exit(0)
    runtime_over_error(filtered_df_int_ic, "Image Classification")

    plot_deviation(df)


    plot_pareto3d("Pareto Diagram IC float", filtered_df_float_ic)
    plot_pareto3d("Pareto Diagram KWS", filtered_df_int_kws)


    import sys; sys.exit(0)
    plot_pareto3d("Pareto Diagram AD", filtered_df_int_ad)
    plot_pareto3d("Pareto Diagram KWS", filtered_df_int_kws)
    plot_pareto3d("Pareto Diagram IC", filtered_df_int_ic)
    plot_pareto3d("Pareto Diagram VWW", filtered_df_int_vww)
    import sys; sys.exit(0)
    
    return 0

if __name__ == '__main__':
    main()

