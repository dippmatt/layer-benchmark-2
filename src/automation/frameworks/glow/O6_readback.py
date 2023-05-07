import os

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

    response_lines = os.popen(f"{stm_cube_programmer} -l uart" ).readlines()
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
    speed = int(os.popen(f"stty -F {location} speed").read())
    
    # Manually set speed to 115200, 
    # because reading it only works when the project has already been flashed.
    # ToDo: cleaner solution: extract uart baud rate from source files of Cube IDE template project
    speed = 115200
    
    return location, speed, port

def readback(ser):
    lines = []
    while(1):
        line = ser.readline().decode().strip('\r\n\x00')
        lines.append(line)
        if "END" in line:
            return lines