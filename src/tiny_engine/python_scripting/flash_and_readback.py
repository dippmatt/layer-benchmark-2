import serial
from pathlib import Path
import multiprocessing
import subprocess

def flash_and_readback(cube_programmer: Path,  workdir: Path, ser: serial.Serial, cube_template: Path, cube_template_no_ir: Path):
    """Flashes the STM32 MCU with the cube_template elf file and reads back the UART output.
    Then flashes the cube_template_no_ir elf file and reads back the UART output.
    Logs of the UART output are saved to the workdir.
    """
    step_output = dict()
    log_file_path = workdir / Path("uart_log.txt")
    # Use multiprocessing for simultaneous flashing and reading back.
    # This is necessary because the STM32 MCU will reset after flashing.
    # The UART output is only available for a short time after reset.
    
    # All arguments for methods in 'Process' are passed as 'copy by value',
    # therefore we need a list from manager
    manager = multiprocessing.Manager()
    reps = manager.list()
    tensor_values = manager.list()
    readback_args = (ser, reps, tensor_values, log_file_path, False)
    flash_args = (cube_programmer, cube_template)

    readback_process = multiprocessing.Process(target=readback, args=readback_args)
    flash_process = multiprocessing.Process(target=flash_mcu, args=flash_args)

    # flash cube template
    readback_process.start()
    flash_process.start()

    flash_process.join()
    readback_process.join()

    assert readback_process.exitcode == 0, "UART Readback of STM32 MCU encountered an error."
    assert flash_process.exitcode == 0, "Flashing STM32 MCU encountered an error."

    reps_no_ir = manager.list()
    tensor_values_no_ir = manager.list()
    readback_args = (ser, reps_no_ir, tensor_values_no_ir, log_file_path, True)
    flash_args = (cube_programmer, cube_template_no_ir)

    readback_process = multiprocessing.Process(target=readback, args=readback_args)
    flash_process = multiprocessing.Process(target=flash_mcu, args=flash_args)

    # flash cube template without IR
    readback_process.start()
    flash_process.start()

    flash_process.join()
    readback_process.join()

    assert readback_process.exitcode == 0, "UART Readback of STM32 MCU encountered an error."
    assert flash_process.exitcode == 0, "Flashing STM32 MCU encountered an error."

    step_output["tensor_values"] = tensor_values
    step_output["reps"] = reps
    step_output["reps_all_layers"] = reps_no_ir

    return step_output


def flash_mcu(stm_cube_programmer, cube_template):
    # assert os.system(f"{stm_cube_programmer} -c port=SWD -w {cube_template} -rst") == 0, "Flashing cube_template failed"
    result = subprocess.run([f'{stm_cube_programmer}', '-c', 'port=SWD', '-w', f'{cube_template}', '-rst'], capture_output=True, text=True)
    assert result.returncode == 0, "Flashing cube_template failed"
    # uart readback & flash cube_template_no_ir
    return


def readback(ser, reps, tensor_values, log_file_path, NO_IR=False):
    """Reads back the UART output from the STM32 MCU.
    We extract the following information from the cube_template project:
    - Per layer execution time, in us. We repeat the measurement NUM_REPS times.
    - Model output, in float or int8 format.
    We extract the following information from the cube_template_no_ir project:
    - Whole model execution time, in us. We repeat the measurement NUM_REPS times.
    """
    # Define the states using constants (enum-like)
    STATES = {
        "UNKNOWN": 0,
        "TIMING_BENCHMARK": 1,
        "ONE_TIMING_REPETITION": 2,
        "VALUE_BENCHMARK": 3,
    }

    with open(log_file_path, "a") as log_file:
        # Initialize the state
        current_state = STATES["UNKNOWN"]
        lines = []
        while True:
            line = ser.readline().decode().strip('\r\n\x00')
            
            # for debugging
            # print(current_state, line)
            
            # Check the state and perform transitions based on the special strings in the UART line
            if current_state != STATES["UNKNOWN"]:
                log_file.write(line + "\n")

            if current_state == STATES["UNKNOWN"]:
                if 'Start of benchmark.' in line:
                    current_state = STATES["TIMING_BENCHMARK"]

            elif current_state == STATES["TIMING_BENCHMARK"]:
                if 'Profiling "MAIN loop timing" sequence:' in line:
                    current_state = STATES["ONE_TIMING_REPETITION"]
                #elif 'Finished timing measurements!' in line:

            elif current_state == STATES["ONE_TIMING_REPETITION"]:
                if 'Profiling "MAIN loop timing" sequence:' in line:
                    lines = []
                    continue
                elif 'Finished timing measurements!' in line:
                    current_state = STATES["VALUE_BENCHMARK"]
                else:
                    if 'START' in line:
                        continue
                    elif 'END' in line:
                        if NO_IR:
                            reps.append(line)
                        else:
                            reps.append(lines.copy())
                    elif 'STOP' in line:
                        lines.append(line)

            elif current_state == STATES["VALUE_BENCHMARK"]:
                # not interested in the values
                # we have them already from the cube_template project
                if NO_IR:
                    return 0
                if "End of benchmark." in line:
                    return 0
                elif 'Tensor values:' in line:
                    continue
                else:
                    tensor_values.append(line)
    