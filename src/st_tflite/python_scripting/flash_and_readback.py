from typing import List
import serial
from pathlib import Path
import multiprocessing
import subprocess
from shared_scripts.color_print import print_in_color, Color

def flash_and_readback(cube_programmer: Path,  workdir: Path, ser: serial.Serial, cube_template: Path, cube_template_all_layers: Path):
    """Flashes the STM32 MCU with the cube_template elf file and reads back the UART output.
    Then flashes the cube_template_no_ir elf file and reads back the UART output.
    Logs of the UART output are saved to the workdir.
    """
    step_output = dict()
    log_file_path = workdir / Path("uart_log.txt")
    log_file_path_all_layers = workdir / Path("uart_log_all_layers.txt")
    # Use multiprocessing for simultaneous flashing and reading back.
    # This is necessary because the STM32 MCU will reset after flashing.
    # The UART output is only available for a short time after reset.
    
    # All arguments for methods in 'Process' are passed as 'copy by value',
    # therefore we need a list from manager
    manager = multiprocessing.Manager()
    reps = manager.list()
    readback_args = (ser, reps, log_file_path, False)
    flash_args = (cube_programmer, cube_template)

    readback_process = multiprocessing.Process(target=readback2, args=readback_args)
    flash_process = multiprocessing.Process(target=flash_mcu, args=flash_args)

    # flash cube template
    readback_process.start()
    flash_process.start()

    flash_process.join()
    readback_process.join()

    assert readback_process.exitcode == 0, "UART Readback of STM32 MCU encountered an error."
    assert flash_process.exitcode == 0, "Flashing STM32 MCU encountered an error."

    reps_all_layers = manager.list()
    readback_args = (ser, reps_all_layers, log_file_path_all_layers, True)
    flash_args = (cube_programmer, cube_template_all_layers)

    readback_process = multiprocessing.Process(target=readback2, args=readback_args)
    flash_process = multiprocessing.Process(target=flash_mcu, args=flash_args)

    # flash cube template without IR
    readback_process.start()
    flash_process.start()

    flash_process.join()
    readback_process.join()

    assert readback_process.exitcode == 0, "UART Readback of STM32 MCU encountered an error."
    assert flash_process.exitcode == 0, "Flashing STM32 MCU encountered an error."

    step_output["reps"] = reps
    step_output["reps_all_layers"] = reps_all_layers

    return step_output


def flash_mcu(stm_cube_programmer: Path, cube_template: Path):
    result = subprocess.run([f'{stm_cube_programmer}', '-c', 'port=SWD', '-w', f'{cube_template}', '-rst'], capture_output=True, text=True)
    assert result.returncode == 0, "Flashing cube_template failed"
    return

def readback2(ser: serial.Serial, reps: List, log_file_path: Path, all_layer: bool):
    """Reads back the UART output from the STM32 MCU.
    We extract the following information from the cube_template project:
    - Per layer execution time, in us. We repeat the measurement NUM_REPS times.
    - Model output, in float or int8 format.
    We extract the following information from the cube_template_all_layers project:
    - Whole model execution time, in us. We repeat the measurement NUM_REPS times.
    """
    # Define the states using constants (enum-like)
    STATES = {
        "UNKNOWN": 0,
        "START": 1,
        "TIMING_BENCHMARK": 2,
        "TIMING_SUM": 3
    }

    with open(log_file_path, "a") as log_file:
        # Initialize the state
        current_state = STATES["UNKNOWN"]
        while True:
            line = ser.readline().decode().strip('\r\n\x00')
            
            # Check the state and perform transitions based on the special strings in the UART line
            if current_state != STATES["UNKNOWN"]:
                log_file.write(line + "\n")

            if current_state == STATES["UNKNOWN"]:
                if '# AI system performance measurement' in line:
                    current_state = STATES["START"]

            elif current_state == STATES["START"]:
                # Detect the start of the per-layer timing benchmark
                if not all_layer:
                    if '----------------------------' in line:
                        current_state = STATES["TIMING_BENCHMARK"]
                # Detect the start of the reference timing benchmark
                else:
                    if 'duration' in line:
                        reps.append(line)
                        current_state = STATES["TIMING_SUM"]

            elif current_state == STATES["TIMING_BENCHMARK"]:
                if '----------------------------' in line:
                    current_state = STATES["TIMING_SUM"]
                else:
                    reps.append(line)
            
            elif current_state == STATES["TIMING_SUM"]:
                if 'Finished timing measurements!' in line:
                    return 0
                else:
                    continue
                