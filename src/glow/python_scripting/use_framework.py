from pathlib import Path
import subprocess
import shutil

def use_framework(quantize: bool, workdir: Path, glow_compiler: Path, glow_profiler: Path, nxp: bool, input_name: str, input_tensors, model):
    step_output = dict()

    if quantize:
        input_tensors_list = gen_tensor_list_file(input_tensors, workdir)
        model_profile = profile(glow_profiler, input_tensors_list, model, input_name, workdir)
        step_output['bundle_dir'], step_output['bundle_dir_no_ir'] = compile(glow_compiler, model, quantize, workdir, nxp, model_profile=model_profile)
    else:
        step_output['bundle_dir'], step_output['bundle_dir_no_ir'] = compile(glow_compiler, model, quantize, workdir, nxp, model_profile=None)
    
    # The compile function generates a log text file depending on the cwd.
    # So copy that log file, that contains the layer names, into workdir.
    instrument_ir_info_src = workdir / Path("..", "..", "instrument-ir.info")
    instrument_ir_info_dst = workdir / "instrument-ir.info"
    shutil.copy(instrument_ir_info_src, instrument_ir_info_dst)
    step_output["layer_list"] = extract_layer_names(instrument_ir_info_dst)
    return step_output


def extract_layer_names(instrument_ir_info: Path):
    """Extracts layer names from the instrument-ir.info file.
    """
    layer_names = []
    with open(instrument_ir_info, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if "Name :" in line:
                layer_name = line.split('Name :')[1].strip('\n')
                layer_name = layer_name.strip(' ')
                layer_names.append(layer_name)
    return layer_names
            


def gen_tensor_list_file(np_array, workdir):
    out_file_name = 'inputtensors.txt'

    tensor_bin_file_dir = workdir / 'bin_files'
    tensor_bin_file_dir.mkdir()

    filenames = []
    for i in range(np_array.shape[0]):
        output_file = tensor_bin_file_dir / f'{i}.bin'
        filenames.append(str(output_file))
        np_array[i].tofile(output_file)

    with open(workdir / out_file_name, 'w') as outfile:
        for filename in filenames:
            outfile.write(filename + '\n')

    return workdir / out_file_name

def profile(glow_profiler, input_tensors_list, model_path, input_name, workdir):
    model_profile = workdir / 'profile.yaml'
    result = subprocess.run([f'{glow_profiler}', f'-model={model_path}', f'-input-dataset={input_name},rawbin,file,{input_tensors_list}', f'-dump-profile={model_profile}'], capture_output=True, text=True)

    if result.returncode == 0:
        return model_profile
    else:
        raise RuntimeError(f"Model profiling returned error code {result.returncode}!\nMessage:\n{result.stderr}") 

def compile(glow_compiler, model_path, use_profile: bool, workdir, nxp: bool, model_profile=None):
    bundle_dir = workdir / 'build' / 'ir'
    bundle_dir_no_ir = workdir / 'build' / 'no-ir'

    for directory_path in [bundle_dir, bundle_dir_no_ir]:
        try:
            path = Path(directory_path)
            path.mkdir(parents=True, exist_ok=True)
            print(f"Directory '{directory_path}' created successfully.")
        except FileExistsError:
            print(f"Directory '{directory_path}' already exists.")
        except Exception as e:
            print(f"Error occurred while creating directory '{directory_path}': {e}")

    dot_graph = workdir / "graph.dot"
    pdf_graph = workdir / "graph.pdf"

    # Only the non-open-source glow compiler from NXP can use ARM's CMSIS library.
    if nxp:
        cmsis_arg = '-use-cmsis'
    else:
        cmsis_arg = ''

    if use_profile:
        assert model_profile is not None 
        result = subprocess.run([f'{glow_compiler}', '-backend=CPU', '-target=arm', '-float-abi=hard', '-mcpu=cortex-m4', f'-model={model_path}', f'-emit-bundle={str(bundle_dir)}', '-llvm-compiler-opt=O3', '-llvm-opt=O3', '-verbose-compilation', f'-load-profile={model_profile}', '-instrument-ir', '-compilation-log', '-g', f'-dump-graph-DAG={str(dot_graph)}', f'-optimize-ir', f'{cmsis_arg}'], capture_output=True, text=True)
        result_no_ir = subprocess.run([f'{glow_compiler}', '-backend=CPU', '-target=arm', '-float-abi=hard', '-mcpu=cortex-m4', f'-model={model_path}', f'-emit-bundle={str(bundle_dir_no_ir)}', '-llvm-compiler-opt=O3', '-llvm-opt=O3', '-verbose-compilation', f'-load-profile={model_profile}', '-compilation-log', '-g', f'-optimize-ir', f'{cmsis_arg}'], capture_output=True, text=True)
        returncode = result.returncode
        returncode_no_ir = result_no_ir.returncode
    else:
        result = subprocess.run([f'{glow_compiler}', '-backend=CPU', '-target=arm', '-float-abi=hard', '-mcpu=cortex-m4', f'-model={model_path}', f'-emit-bundle={str(bundle_dir)}', '-llvm-compiler-opt=O3', '-llvm-opt=O3', '-verbose-compilation', '-instrument-ir', '-compilation-log', '-g', f'-dump-graph-DAG={str(dot_graph)}', f'-optimize-ir', f'{cmsis_arg}'], capture_output=True, text=True)
        result_no_ir = subprocess.run([f'{glow_compiler}', '-backend=CPU', '-target=arm', '-float-abi=hard', '-mcpu=cortex-m4', f'-model={model_path}', f'-emit-bundle={str(bundle_dir_no_ir)}', '-llvm-compiler-opt=O3', '-llvm-opt=O3', '-verbose-compilation', '-compilation-log', '-g', f'-optimize-ir', f'{cmsis_arg}'], capture_output=True, text=True)
        returncode = result.returncode
        returncode_no_ir = result_no_ir.returncode

    if returncode != 0:
        raise RuntimeError(f"Model compiling returned error code {returncode}! \
                           Check if you can use the \'-use-cmsis\' compile argument. \
                           It only works when using the glow compiler from NXP. Check -h for more detailes.\n \
                           Message:\n{result.stderr}") 
    
    if returncode_no_ir != 0:
        raise RuntimeError(f"Model compiling returned error code {returncode}! \
                           Check if you can use the \'-use-cmsis\' compile argument. \
                           It only works when using the glow compiler from NXP. Check -h for more detailes.\n \
                           Message:\n{result.stderr}") 
    
    subprocess.run(['dot', '-Tpdf', f'{str(dot_graph)}', '-o' f'{str(pdf_graph)}'], text=True, check=True)
    
    return bundle_dir, bundle_dir_no_ir