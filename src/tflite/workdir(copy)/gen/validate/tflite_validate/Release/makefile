################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include X-CUBE-AI/App/subdir.mk
-include Middlewares/tensorflow/third_party/cmsis_nn/Source/SoftmaxFunctions/subdir.mk
-include Middlewares/tensorflow/third_party/cmsis_nn/Source/SVDFunctions/subdir.mk
-include Middlewares/tensorflow/third_party/cmsis_nn/Source/ReshapeFunctions/subdir.mk
-include Middlewares/tensorflow/third_party/cmsis_nn/Source/PoolingFunctions/subdir.mk
-include Middlewares/tensorflow/third_party/cmsis_nn/Source/NNSupportFunctions/subdir.mk
-include Middlewares/tensorflow/third_party/cmsis_nn/Source/LSTMFunctions/subdir.mk
-include Middlewares/tensorflow/third_party/cmsis_nn/Source/FullyConnectedFunctions/subdir.mk
-include Middlewares/tensorflow/third_party/cmsis_nn/Source/ConvolutionFunctions/subdir.mk
-include Middlewares/tensorflow/third_party/cmsis_nn/Source/ConcatenationFunctions/subdir.mk
-include Middlewares/tensorflow/third_party/cmsis_nn/Source/BasicMathFunctions/subdir.mk
-include Middlewares/tensorflow/third_party/cmsis_nn/Source/ActivationFunctions/subdir.mk
-include Middlewares/tensorflow/tensorflow/lite/schema/subdir.mk
-include Middlewares/tensorflow/tensorflow/lite/micro/tflite_bridge/subdir.mk
-include Middlewares/tensorflow/tensorflow/lite/micro/memory_planner/subdir.mk
-include Middlewares/tensorflow/tensorflow/lite/micro/kernels/cmsis_nn/subdir.mk
-include Middlewares/tensorflow/tensorflow/lite/micro/kernels/subdir.mk
-include Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/subdir.mk
-include Middlewares/tensorflow/tensorflow/lite/micro/subdir.mk
-include Middlewares/tensorflow/tensorflow/lite/kernels/internal/reference/subdir.mk
-include Middlewares/tensorflow/tensorflow/lite/kernels/internal/subdir.mk
-include Middlewares/tensorflow/tensorflow/lite/kernels/subdir.mk
-include Middlewares/tensorflow/tensorflow/lite/core/c/subdir.mk
-include Middlewares/tensorflow/tensorflow/lite/core/api/subdir.mk
-include Drivers/STM32L4xx_HAL_Driver/Src/subdir.mk
-include Core/Startup/subdir.mk
-include Core/Src/subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(CC_DEPS)),)
-include $(CC_DEPS)
endif
ifneq ($(strip $(C++_DEPS)),)
-include $(C++_DEPS)
endif
ifneq ($(strip $(C_UPPER_DEPS)),)
-include $(C_UPPER_DEPS)
endif
ifneq ($(strip $(CXX_DEPS)),)
-include $(CXX_DEPS)
endif
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
ifneq ($(strip $(CPP_DEPS)),)
-include $(CPP_DEPS)
endif
endif

-include ../makefile.defs

OPTIONAL_TOOL_DEPS := \
$(wildcard ../makefile.defs) \
$(wildcard ../makefile.init) \
$(wildcard ../makefile.targets) \


BUILD_ARTIFACT_NAME := tflite_validate
BUILD_ARTIFACT_EXTENSION := elf
BUILD_ARTIFACT_PREFIX :=
BUILD_ARTIFACT := $(BUILD_ARTIFACT_PREFIX)$(BUILD_ARTIFACT_NAME)$(if $(BUILD_ARTIFACT_EXTENSION),.$(BUILD_ARTIFACT_EXTENSION),)

# Add inputs and outputs from these tool invocations to the build variables 
EXECUTABLES += \
tflite_validate.elf \

MAP_FILES += \
tflite_validate.map \

SIZE_OUTPUT += \
default.size.stdout \

OBJDUMP_LIST += \
tflite_validate.list \


# All Target
all: main-build

# Main-build Target
main-build: tflite_validate.elf secondary-outputs

# Tool invocations
tflite_validate.elf tflite_validate.map: $(OBJS) $(USER_OBJS) /home/matthias/Documents/BA/layer-benchmark-2/src/tflite/workdir/gen/validate/tflite_validate/STM32L4R5ZITX_FLASH.ld makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-g++ -o "tflite_validate.elf" @"objects.list" $(USER_OBJS) $(LIBS) -mcpu=cortex-m4 -T"/home/matthias/Documents/BA/layer-benchmark-2/src/tflite/workdir/gen/validate/tflite_validate/STM32L4R5ZITX_FLASH.ld" --specs=nosys.specs -Wl,-Map="tflite_validate.map" -Wl,--gc-sections -static -Wl,--wrap=malloc -Wl,--wrap=free -u _printf_float --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -Wl,--start-group -lc -lm -lstdc++ -lsupc++ -Wl,--end-group
	@echo 'Finished building target: $@'
	@echo ' '

default.size.stdout: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-size  $(EXECUTABLES)
	@echo 'Finished building: $@'
	@echo ' '

tflite_validate.list: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-objdump -h -S $(EXECUTABLES) > "tflite_validate.list"
	@echo 'Finished building: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) default.size.stdout tflite_validate.elf tflite_validate.list tflite_validate.map
	-@echo ' '

secondary-outputs: $(SIZE_OUTPUT) $(OBJDUMP_LIST)

fail-specified-linker-script-missing:
	@echo 'Error: Cannot find the specified linker script. Check the linker settings in the build configuration.'
	@exit 2

warn-no-linker-script-specified:
	@echo 'Warning: No linker script specified. Check the linker settings in the build configuration.'

.PHONY: all clean dependents main-build fail-specified-linker-script-missing warn-no-linker-script-specified

-include ../makefile.targets
