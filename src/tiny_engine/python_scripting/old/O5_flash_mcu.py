import os

def flash_mcu(stm_cube_programmer, elf_file):
    return os.system(f"{stm_cube_programmer} -c port=SWD -w {elf_file} -rst")