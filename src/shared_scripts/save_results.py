from pathlib import Path
import numpy as np
import shutil

def save_results(out_dir: Path,
                workdir: Path,
                layer_list: list,
                ram: int,
                flash: int,
                per_layer_timings_mean: np.array,
                per_layer_timings_std_dev: np.array,
                all_layers_timings_mean: np.array,
                all_layers_timings_std_dev: np.array,
                mcu_tensor_values: np.array,
                ref_tensor_values: np.array):
    """Saves the results to a file.
    """
    step_output = dict()

    if layer_list is not None:
        # save each line in layer list to a file
        layer_list_file = out_dir / Path("layer_list.txt")
        with open(layer_list_file, 'w') as file:
            for layer in layer_list:
                file.write(layer + '\n')

    if ram is not None and flash is not None:
        ram_flash_file = out_dir / Path("ram_flash.txt")
        with open(ram_flash_file, 'w') as file:
            file.write("RAM: " + str(ram) + "\n" + "FLASH: " + str(flash) + "\n")
    
    # save layer timings mean as npz
    if per_layer_timings_mean is not None:
        per_layer_timings_mean_file = out_dir / Path("per_layer_timings_mean.npz")
        np.savez(per_layer_timings_mean_file, per_layer_timings_mean)

    # save layer timings standard deviation as npz
    if per_layer_timings_std_dev is not None:
        per_layer_timings_std_dev_file = out_dir / Path("per_layer_timings_std_dev.npz")
        np.savez(per_layer_timings_std_dev_file, per_layer_timings_std_dev)

    # save all layers timings mean as npz
    if all_layers_timings_mean is not None:
        all_layers_timings_mean_file = out_dir / Path("all_layers_timings_mean.npz")
        np.savez(all_layers_timings_mean_file, all_layers_timings_mean)

    # save all layers timings standard deviation as npz
    if all_layers_timings_std_dev is not None:
        all_layers_timings_std_dev_file = out_dir / Path("all_layers_timings_std_dev.npz")
        np.savez(all_layers_timings_std_dev_file, all_layers_timings_std_dev)

    # save mcu tensor values as npz
    if mcu_tensor_values is not None:
        mcu_tensor_values_file = out_dir / Path("mcu_tensor_values.npz")
        np.savez(mcu_tensor_values_file, mcu_tensor_values)
    
    # save reference tensor values as npz
    if ref_tensor_values is not None:
        ref_tensor_values_file = out_dir / Path("ref_tensor_values.npz")
        np.savez(ref_tensor_values_file, ref_tensor_values)

    # copy the entire workdir
    if workdir is not None:
        workdir_dst = out_dir / Path("workdir")
        workdir_dst.mkdir(parents=True, exist_ok=True)
        workdir_src = workdir
        shutil.copytree(workdir_src, workdir_dst, dirs_exist_ok=True)

    step_output["Success"] = True
    return step_output

if __name__ == "__main__":

    out_dir = "tmp"
    workdir = None
    layer_list = ["layer1", "layer2", "layer3"]
    ram = 100
    flash = 100
    per_layer_timings_mean = np.array([1,2,3])
    per_layer_timings_std_dev = np.array([6])
    all_layers_timings_mean = np.array([9])
    all_layers_timings_std_dev = np.array([8])
    mcu_tensor_values = np.array([7])
    ref_tensor_values = np.array([4])
    

    save_results(out_dir,
                workdir,
                layer_list,
                ram,
                flash,
                per_layer_timings_mean,
                per_layer_timings_std_dev,
                all_layers_timings_mean,
                all_layers_timings_std_dev,
                mcu_tensor_values,
                ref_tensor_values)