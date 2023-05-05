import os

def compile(glow_compiler, model_path, use_profile: bool, workdir, model_profile=None):
    bundle_dir = os.path.join(workdir, 'build')
    dot_graph = os.path.join(workdir, "graph.dot")
    pdf_graph = os.path.join(workdir, "graph.pdf")

    if use_profile:
        assert model_profile is not None 
        return_code = os.system(f'{glow_compiler} -backend=CPU -target=arm -float-abi=hard -mcpu=cortex-m4 -model={model_path} -emit-bundle={bundle_dir} -llvm-compiler-opt=O3 -llvm-opt=O3 -verbose-compilation -load-profile={model_profile} -instrument-ir -compilation-log -g -dump-graph-DAG={dot_graph} -optimize-ir -use-cmsis')
    else:
        return_code = os.system(f'{glow_compiler} -backend=CPU -target=arm -float-abi=hard -mcpu=cortex-m4 -model={model_path} -emit-bundle={bundle_dir} -llvm-compiler-opt=O3 -llvm-opt=O3 -verbose-compilation -instrument-ir -compilation-log -g -dump-graph-DAG={dot_graph} -optimize-ir -use-cmsis')

    os.system(f"dot -Tpdf {dot_graph} -o {pdf_graph}")

    if return_code == 0:
        return bundle_dir
    else:
        raise RuntimeError(f"Model compiling returned error code {return_code}!") 
