from pathlib import Path
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

def read_layer_names(layer_names_txt):
    with open(layer_names_txt, 'r') as f:
        lines = f.readlines()
    layer_names = []
    for line in lines:
        layer_names.append(line.strip())
    return layer_names


def data_metrics(tensor_values, tensor_values_ref):
    # print(tensor_values.shape)
    # print(tensor_values_ref.shape)
    # print(tensor_values.dtype)
    # print(tensor_values_ref.dtype)
    # import sys; sys.exit()
    tensor_values = tensor_values.astype(np.float64)
    tensor_values_ref = tensor_values_ref.astype(np.float64)

    return_metrics = {}
    return_metrics['rmse'] = rmse(tensor_values_ref, tensor_values)
    return_metrics['mae'] = mae(tensor_values_ref, tensor_values)
    return_metrics['l2r'] = l2r(tensor_values_ref, tensor_values)
    # if return_metrics['l2r'] > 1.1:
    #     print("large error")
    return return_metrics



def plot_sankey(layer_assignment: list, ref_names: list, reference_timings: np.array, target_names: list ,target_timings: np.array):
    # Extract source and target nodes from the data structure
    ref_len = len(ref_names)
    labels = ref_names + target_names
    
    reference_nodes = []
    target_nodes = []
    values = []

    for mapping in layer_assignment :
        for source, targets in mapping.items():
            # extract the timing value of the tflite reference layer
            source_value = reference_timings[source]
            # now handle the one to many relation to target layers
            target_values = target_timings[np.array(targets)]
            # if type(target_values) != np.ndarray:
            #     target_values = [target_values]
            print(type(targets))
            if type(targets) != tuple:
                targets = (targets,)
            for target in targets:
                target_value = target_timings[target]
                values.append(target_value)
                reference_nodes.append(source)
                target_nodes.append(target + ref_len)
                # reference_nodes.append(source_value)
                # target_nodes.append(target)
            continue
        
    # Create a Plotly Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=labels
        ),
        link=dict(
            source=reference_nodes,
            target=target_nodes,
            value=values
        )
    )])
    fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
    fig.show()
    return

    # Update layout for better visibility
    fig.update_layout(title_text="Sankey Diagram for Correspondence",
                    font_size=10,
                    width=800,
                    height=600)

    # Show the Sankey diagram
    fig.show()


def plot_sankey2(layer_assignment: list, ref_names: list, reference_timings: np.array, target_names: list ,target_timings: np.array):
    # Extract source and target nodes from the data structure
    ref_len = len(ref_names)
    labels = ref_names + target_names
    
    reference_nodes = []
    target_nodes = []
    values = []

    for mapping in layer_assignment :
        for source, targets in mapping.items():
            # extract the timing value of the tflite reference layer
            source_value = reference_timings[source]
            # now handle the one to many relation to target layers
            target_values = target_timings[np.array(targets)]
            # if type(target_values) != np.ndarray:
            #     target_values = [target_values]
            print(type(targets))
            if type(targets) != tuple:
                targets = (targets,)
            for target in targets:
                target_value = target_timings[target]
                values.append(target_value)
                reference_nodes.append(source)
                target_nodes.append(target + ref_len)
                # reference_nodes.append(source_value)
                # target_nodes.append(target)
            continue
        
    # Create a Plotly Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=labels
        ),
        link=dict(
            source=reference_nodes,
            target=target_nodes,
            value=values
        )
    )])
    fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
    fig.show()
    return

    # Update layout for better visibility
    fig.update_layout(title_text="Sankey Diagram for Correspondence",
                    font_size=10,
                    width=800,
                    height=600)

    # Show the Sankey diagram
    fig.show()


def rmse(ref, pred):
  """Return Root Mean Squared Error (RMSE)."""
  return np.sqrt(((ref - pred).astype(np.float64) ** 2).mean())


def mae(ref, pred):
  """Return Mean Absolute Error (MAE)."""
  return (np.abs(ref - pred).astype(np.float64)).mean()


def l2r(ref, pred):
  """Compute L2 relative error"""
  def magnitude(v):
    return np.sqrt(np.sum(np.square(v).flatten()))
  mag = magnitude(pred) + np.finfo(np.float32).eps
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
    timings_dir = Path(__file__).parent / Path('..', '..', 'data_gen')

    df = pd.DataFrame(columns=['model', 'framework', 'dtype', 'flash', 'ram', 'avg_timing', 'config_name', 'layer_names', 'rmse', 'mae', 'l2r', 'std_dev', 'std_dev_per_layer', 'per_layer_timings', 'sum_timing', 'layer_assignments'])
    
    # Sanity check: verify the naming scheme of the benchmark folders
    framework_counter = 0
    model_counter = 0
    quant_counter = 0

    #########################################################################
    ######     Loop over all benchmarks and fill pandas data frame     ######
    #########################################################################
    
    for benchmark in timings_dir.iterdir():
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

        #print(std_dev)
        new_row_data['std_dev'] = float(std_dev)

        ###################################################
        ###### STD DEVIATION PER LAYER ######
        ###################################################

        std_dev_file_per_layer = Path(benchmark, 'per_layer_timings_std_dev.npz')
        if not std_dev_file_per_layer.exists():
            # print(new_row_data['framework'])
            # print(std_dev_timing.shape)
            # print()
            std_dev = np.array([0])
        else:
            input_data = np.load(std_dev_file_per_layer)
            std_dev_per_layer =input_data['arr_0']
            #print(std_dev_per_layer)
     
        if std_dev_per_layer.shape == (1,):
            std_dev_per_layer = std_dev_per_layer[0]
        else:
            std_dev_per_layer = std_dev_per_layer

        #print(std_dev)
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
        new_row_data['rmse'] = metrics['rmse']
        new_row_data['mae'] = metrics['mae']
        new_row_data['l2r'] = metrics['l2r'] + 1
        # print(metrics)

        # add the new row to the df
        df.loc[len(df)] = new_row_data
    
    ############################################################
    ######     Postprocess data & Perform experiments     ######
    ############################################################
    
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
    layer_assignment_ic_18 = [{0: (0), 1: (1), 2: (2), 3: (3,4), 4: (6), 5: (7), 6: (5), 7: (8,9), 8: (11), 9: (13), 10: (10), 11: (13,14), 12: (15), 13: (16), 14: (16), 15: (17)}]
    layer_assignment_ic_21 = [{0: (0), 1: (1,2), 2: (3,4), 3: (5), 4: (6,7), 5: (8,9), 6: (10), 7: (11), 8: (12,13), 9: (14,15), 10: (16), 11: (17), 12: (18), 13: (19), 14: (19), 15: (20)}]
    layer_assignment_ic_22 = [{0: (0,1), 1: (2,3), 2: (4), 3: (5,6), 4: (8,9), 5: (10), 6: (7), 7: (11,12), 8: (14,15), 9: (16), 10: (13), 11: (17,18), 12: (19), 13: (20), 14: (20), 15: (21)}]

    # Original VWW model has 31 layers
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

        if row['model'] == 'vww':
            if 'nosoftmax' in config_name:
                # ignore all models without softmax
                continue
            else:
                if layer_number[-1] == 31:
                    df.at[index, 'layer_assignments'] = layer_assignment_vww_31
                elif layer_number[-1] == 43:
                    df.at[index, 'layer_assignments'] = layer_assignment_vww_43
                elif layer_number[-1] == 57:
                    df.at[index, 'layer_assignments'] = layer_assignment_vww_57
            #print(f"VWW model of {config_name} has {layer_number} layers.")
            # for layer in row['layer_names']:
            #     print(layer)
            # print()
            # print()

    # get tflite per layer timings for each use case as reference to calculate sankey diagrams
    # also create mean over all repetitions ( axis per_layer_ref_timings_tflite.shape[0])
    for index, row in df.iterrows():
        if row['framework'] == 'tflite':
            if row['model'] == 'ad':
                per_layer_ref_timings_tflite_ad = np.mean(row['per_layer_timings'], axis=0)
                ref_names_tflite_ad = row['layer_names'][:per_layer_ref_timings_tflite_ad.shape[0]]
            if row['model'] == 'kws':
                per_layer_ref_timings_tflite_kws = np.mean(row['per_layer_timings'], axis=0)
                ref_names_tflite_kws = row['layer_names'][:per_layer_ref_timings_tflite_kws.shape[0]]
            if row['model'] == 'ic':
                per_layer_ref_timings_tflite_ic = np.mean(row['per_layer_timings'], axis=0)
                ref_names_tflite_ic = row['layer_names'][:per_layer_ref_timings_tflite_ic.shape[0]]
            if row['model'] == 'vww':
                per_layer_ref_timings_tflite_vww = np.mean(row['per_layer_timings'], axis=0)
                ref_names_tflite_vww = row['layer_names'][:per_layer_ref_timings_tflite_vww.shape[0]]
    
    print(per_layer_ref_timings_tflite_ad.shape)
    print(per_layer_ref_timings_tflite_kws.shape)
    print(per_layer_ref_timings_tflite_ic.shape)
    print(per_layer_ref_timings_tflite_vww.shape)

    for index, row in df.iterrows():
        if not pd.isna(row['layer_assignments']):
            # get the reference for the corresponding model
            if row['model'] == 'ad':
                per_layer_ref_timings_tflite = per_layer_ref_timings_tflite_ad
                ref_names_tflite = ref_names_tflite_ad
            if row['model'] == 'kws':
                per_layer_ref_timings_tflite = per_layer_ref_timings_tflite_kws
                ref_names_tflite = ref_names_tflite_kws
            if row['model'] == 'ic':
                per_layer_ref_timings_tflite = per_layer_ref_timings_tflite_ic
                ref_names_tflite = ref_names_tflite_ic
            if row['model'] == 'vww':
                per_layer_ref_timings_tflite = per_layer_ref_timings_tflite_vww
                ref_names_tflite = ref_names_tflite_vww
            # get the mean over all repetitions
            per_layer_mean = np.mean(row['per_layer_timings'], axis=0)
            target_names = row['layer_names'][:per_layer_mean.shape[0]]
            
            print(per_layer_mean)
            plot_sankey2(row['layer_assignments'], ref_names_tflite, per_layer_ref_timings_tflite, target_names, per_layer_mean)

        
            import sys;sys.exit()

    
    
    #################################################
    ####              Visualisation              ####
    #################################################
    # model_name = 'kws'
    #framework_name = 'tiny_engine'
    # filtered_df = df[df['framework'] != framework_name]
    #data_type = 'int'
    #filtered_df = df[df['dtype'] == data_type]
    filtered_df = df

    #filtered_df['ram_flash_product'] = filtered_df['ram'] * filtered_df['flash'] / 10E6
    #filtered_df = filtered_df.sort_values(by='ram_flash_product')
    fig = px.scatter(filtered_df, x='ram', y='sum_timing', color='framework',
                 facet_col='model', title='Timing vs Memory', size='l2r', hover_data=['config_name', 'ram', 'flash', 'dtype', 'framework', 'avg_timing', 'l2r'])
   
    fig.show()
    return 0

if __name__ == '__main__':
    main()

