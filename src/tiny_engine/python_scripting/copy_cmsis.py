import os 
import sys
import argparse

def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-cube_prj_path', dest='cube_path', type=str, help='Path to the STMicroelectronics CubeIDE project folder.')
    parser.add_argument('-tinyengine_path', dest='tinyengine_path', type=str, help='Path to tinyengine git repo folder.')
    args = parser.parse_args()

    # check path validity
    if not os.path.exists(args.cube_path):
        raise ValueError(f"Path to cube project does not exist: {args.cube_path}")
    if not os.path.exists(args.tinyengine_path):
        raise ValueError(f"Path to tinyengine git repo does not exist: {args.tinyengine_path}")
    
    copy_from_base = args.tinyengine_path
    copy_to_base = os.path.join(args.cube_path, "Core")

    # create tinyenging & cmsis folder in cube project
    cmsis_cube_path = os.path.join(copy_to_base, "Src", "TinyEngine", "include", "arm_cmsis")
    os.system(f'mkdir -p {cmsis_cube_path}')
    cmsis_cube_path = os.path.join(copy_to_base, "Src", "TinyEngine", "src", "arm_cmsis")
    os.system(f'mkdir -p {cmsis_cube_path}')

    ############## copy tinyengine codegen ###############
    copy_from_path = os.path.join(copy_from_base, "codegen")
    copy_to_path = os.path.join(copy_to_base, "Src", "TinyEngine")
    os.system(f"cp -r {copy_from_path} {copy_to_path}")
    
    ############### copy tinyengine files ################
    copy_from_path = os.path.join(copy_from_base, "TinyEngine", "include")
    copy_to_path = os.path.join(copy_to_base, "Src", "TinyEngine")
    os.system(f"cp -r {copy_from_path} {copy_to_path}")

    copy_from_path = os.path.join(copy_from_base, "TinyEngine", "src")
    os.system(f"cp -r {copy_from_path} {copy_to_path}")

    ################## copy cmsis files ##################
    copy_from_base = os.path.join(args.tinyengine_path, "TinyEngine", "third_party", "CMSIS", "CMSIS")

    copy_from_path = os.path.join(copy_from_base, "NN", "Include", "*.h")
    copy_to_path = os.path.join(copy_to_base, "Src", "TinyEngine", "include", "arm_cmsis")
    os.system(f"cp -r {copy_from_path} {copy_to_path}")

    copy_from_path = os.path.join(copy_from_base, "NN", "Source", "*")
    copy_to_path = os.path.join(copy_to_base, "Src", "TinyEngine", "src", "arm_cmsis")
    os.system(f"cp -r {copy_from_path} {copy_to_path}")

    copy_from_path = os.path.join(copy_from_base, "DSP", "Include", "dsp")
    copy_to_path = os.path.join(copy_to_base, "Src", "TinyEngine", "include", "arm_cmsis")
    os.system(f"cp -r {copy_from_path} {copy_to_path}")

    copy_from_path = os.path.join(copy_from_base, "DSP", "Include", "arm_common_tables.h")
    copy_to_path = os.path.join(copy_to_base, "Src", "TinyEngine", "include", "arm_cmsis")
    os.system(f"cp {copy_from_path} {copy_to_path}")

    copy_from_path = os.path.join(copy_from_base, "DSP", "Include", "arm_math_memory.h")
    copy_to_path = os.path.join(copy_to_base, "Src", "TinyEngine", "include", "arm_cmsis")
    os.system(f"cp {copy_from_path} {copy_to_path}")

    copy_from_path = os.path.join(copy_from_base, "DSP", "Include", "arm_math_types.h")
    copy_to_path = os.path.join(copy_to_base, "Src", "TinyEngine", "include", "arm_cmsis")
    os.system(f"cp {copy_from_path} {copy_to_path}")

    copy_from_path = os.path.join(copy_from_base, "DSP", "Include", "arm_math.h")
    copy_to_path = os.path.join(copy_to_base, "Src", "TinyEngine", "include", "arm_cmsis")
    os.system(f"cp {copy_from_path} {copy_to_path}")

    copy_to_base = os.path.join(args.cube_path, "Drivers")
    copy_from_path = os.path.join(copy_from_base, "Core", "Include")
    copy_to_path = os.path.join(copy_to_base, "CMSIS")
    os.system(f"cp -r {copy_from_path} {copy_to_path}")

if __name__ == '__main__':
    import sys
    sys.exit(_main())