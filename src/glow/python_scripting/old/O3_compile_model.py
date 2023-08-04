import os

def compile(glow_compiler, model_path, use_profile: bool, workdir, nxp: bool, model_profile=None):
    bundle_dir = os.path.join(workdir, 'build')
    dot_graph = os.path.join(workdir, "graph.dot")
    pdf_graph = os.path.join(workdir, "graph.pdf")

    # Only the non-open-source glow compiler from NXP can use ARM's CMSIS library.
    if nxp:
        cmsis_arg = ' -use-cmsis'
    else:
        cmsis_arg = ''

    if use_profile:
        assert model_profile is not None 
        return_code = os.system(f'{glow_compiler} -backend=CPU -target=arm -float-abi=hard -mcpu=cortex-m4 -model={model_path} -emit-bundle={bundle_dir} -llvm-compiler-opt=O3 -llvm-opt=O3 -verbose-compilation -load-profile={model_profile} -instrument-ir -compilation-log -g -dump-graph-DAG={dot_graph} -optimize-ir{cmsis_arg}')
    else:
        return_code = os.system(f'{glow_compiler} -backend=CPU -target=arm -float-abi=hard -mcpu=cortex-m4 -model={model_path} -emit-bundle={bundle_dir} -llvm-compiler-opt=O3 -llvm-opt=O3 -verbose-compilation -instrument-ir -compilation-log -g -dump-graph-DAG={dot_graph} -optimize-ir{cmsis_arg}')

    os.system(f"dot -Tpdf {dot_graph} -o {pdf_graph}")

    if return_code == 0:
        return bundle_dir
    else:
        raise RuntimeError(f"Model compiling returned error code {return_code}! \
                           Check if you can use the \'-use-cmsis\' compile argument. \
                           It only works when using the glow compiler from NXP. Check -h for more detailes.") 
