import os

def profile(glow_profiler, input_tensors_list, model_path, input_name, workdir):
    model_profile = os.path.join(workdir, 'profile.yaml')
    return_code = os.system(f'{glow_profiler} -model {model_path} -input-dataset={input_name},rawbin,file,{input_tensors_list} -dump-profile={model_profile}')
    
    if return_code == 0:
        return model_profile
    else:
        raise RuntimeError(f"Model profiling returned error code {return_code}!") 
