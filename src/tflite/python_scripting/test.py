from pathlib import Path
from flash_and_readback import flash_and_readback
import serial
import subprocess

cube_programmer = Path("/usr/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI")
workdir = Path("/home/matthias/Documents/BA/layer-benchmark-2/src/tflite/workdir")

#subprocess.run(['fuser', '-k', location], capture_output=True, text=True, check=False)
ser = serial.Serial(
    port="/dev/ttyACM0",
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS)

cube_template = Path("/home/matthias/Documents/BA/layer-benchmark-2/src/tflite/workdir/gen/main/tflite_test/Debug/tflite_test.elf")
cube_template_all_layers = Path("/home/matthias/Documents/BA/layer-benchmark-2/src/tflite/workdir/gen/reference/tflite_test/Debug/tflite_test.elf")

assert cube_template.exists(), "Cube template does not exist"
assert cube_template_all_layers.exists(), "Cube template all layers does not exist"

flash_and_readback(cube_programmer,  workdir, ser, cube_template, cube_template_all_layers)
