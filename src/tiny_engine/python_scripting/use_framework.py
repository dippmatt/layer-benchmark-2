from os import chdir
import shutil
import subprocess
from pathlib import Path

def use_framework(workdir: Path, submodule_dir: Path, model: Path):
    """copies the tinyengine framework from the submodule to the workdir
    Makes modifications to the framework to make it work with the pipeline,
    notably: a script "custom_tflite.py" to run the framework with any tflite model
    """
    step_output = dict()

    custom_tflite_py = Path.cwd() / Path("custom_tflite.py")
    assert submodule_dir.exists(), "tinyengine submodule not found. Please run 'make init' before using tinyengine."

    # copy tinyengine framework to workdir, copy custom_tflite.py to framework,    
    tinyengine_dir = workdir / Path("tinyengine")
    if not tinyengine_dir.exists():
        shutil.copytree(submodule_dir, tinyengine_dir)
    framework_script = tinyengine_dir / Path("examples", "custom_tflite.py")
    framework_script = framework_script.resolve()
    shutil.copy(custom_tflite_py, tinyengine_dir / framework_script)

    # run custom_tflite.py to generate model source files
    cwd = Path.cwd()
    python_exec = cwd / Path("venv", "bin", "python3")
    python_exec = python_exec
    print(cwd)
    chdir(tinyengine_dir)
    cmd = [python_exec, framework_script, model]
    subprocess.run(cmd)

    chdir(cwd)
    step_output["codegen"] = tinyengine_dir / Path("codegen")
    return step_output
    
    
    

if __name__ == "__main__":
    from pathlib import Path
    
    # Prepare directory structure
    workdir = Path.cwd() / Path("..", "workdir")
    submodule_dir = Path.cwd() / Path("..", "..", "..", "third_party", "tinyengine")
    
    model = Path("/home/matthias/Documents/BA/results/models_and_data/anomaly_detection/trained_models/ad01_int8.tflite")
    prep_tinyengine_framework(workdir, submodule_dir, model)
