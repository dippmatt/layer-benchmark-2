import re
import subprocess
from pathlib import Path

def calc_flash_ram(elf_file: Path):
    """Calculate the flash and RAM usage of the project.

    Args:
        elf_file (Path): Path to the reference elf file

    Metrics to calculate ram and flash sizes are equal to 
    ST Cube MX's metrics (e.g. in Network analyze report)
    
    Flash = text + rodata + data
    Ram = data + bss
    Returns: A tuple with the flash and RAM usage in bytes.
    """
    # Define the regular expression patterns for the sections and sizes
    pattern_text = r"\.text\s+(\d+)"
    pattern_data = r"\.data\s+(\d+)"
    pattern_rodata = r"\.rodata\s+(\d+)"
    pattern_bss = r"\.bss\s+(\d+)"

    eabi_size = subprocess.check_output(f'arm-none-eabi-size -A {elf_file}', shell=True, text=True)
    
    text_sizes = re.findall(pattern_text, eabi_size)
    data_sizes = re.findall(pattern_data, eabi_size)
    rodata_sizes = re.findall(pattern_rodata, eabi_size)
    bss_sizes = re.findall(pattern_bss, eabi_size)

    flash = int(data_sizes[0]) + int(rodata_sizes[0]) + int(text_sizes[0])
    ram = int(bss_sizes[0]) + int(data_sizes[0])

    return (ram, flash)