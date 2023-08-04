import serial
import subprocess
from pathlib import Path
from color_print import Color, print_in_color

# dummy value to emulate conntected MCU
EMULATE_MCU = False


def get_mcu_dev(cube_programmer: Path):
    step_output = dict()

    if not EMULATE_MCU:
        location, speed, port = get_uart(str(cube_programmer))
        stm_port = location
        baudrate = speed
    parity = serial.PARITY_NONE
    stopbits = serial.STOPBITS_ONE
    bytesize = serial.EIGHTBITS
    if not EMULATE_MCU:
        ser = serial.Serial(
            port=stm_port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize)
    else:
        print_in_color(Color.RED, "ASSUMING BOARD IS NOT CONNECTED. USING DUMMY SERIAL!")
        print_in_color(Color.RED, "Unset EMULATE_MCU in get_mcu.py if using real board.")
        ser = None
    step_output['serial'] = ser
    return step_output

def get_uart(stm_cube_programmer):
    ################# Example Response from cube programmer #################
    #     -------------------------------------------------------------------
    #                         STM32CubeProgrammer v2.12.0                  
    #     -------------------------------------------------------------------

    # =====  UART Interface  =====

    # Total number of serial ports available: 2

    # Port: ttyACM0
    # Location: /dev/ttyACM0
    # Description: STM32 STLink
    # Manufacturer: STMicroelectronics

    # Port: ttyS0
    # Location: /dev/ttyS0
    # Description: N/A
    # Manufacturer: N/A

    #response_lines = os.popen(f"{stm_cube_programmer} -l uart" ).readlines()
    result = subprocess.run([f'{stm_cube_programmer}', '-l', 'uart'], capture_output=True, text=True, check=True)
    response_lines = result.stdout.split('\n')
    port = None
    location = None

    for i, line in enumerate(response_lines):
        if "Description: STM32 STLink" in line:
            port = response_lines[i-2].rstrip("\n").split("Port: ")
            port = port[1]
            location = response_lines[i-1].rstrip("\n").split("Location: ")
            location = location[1]
            break

    assert location is not None, "Did not find STM32 Nucleo Board connected to UART."
    # Manually set speed to 115200, 
    # because reading it only works when the project has already been flashed.
    # ToDo: cleaner solution: extract uart baud rate from source files of Cube IDE template project
    speed = 115200
    
    return location, speed, port