################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include Drivers/STM32L4xx_HAL_Driver/Src/subdir.mk
-include Core/Startup/subdir.mk
-include Core/Src/TinyEngine/src/kernels/int_forward_op/subdir.mk
-include Core/Src/TinyEngine/src/kernels/fp_requantize_op/subdir.mk
-include Core/Src/TinyEngine/src/kernels/fp_backward_op/subdir.mk
-include Core/Src/TinyEngine/src/arm_cmsis/SoftmaxFunctions/subdir.mk
-include Core/Src/TinyEngine/src/arm_cmsis/SVDFunctions/subdir.mk
-include Core/Src/TinyEngine/src/arm_cmsis/ReshapeFunctions/subdir.mk
-include Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/subdir.mk
-include Core/Src/TinyEngine/src/arm_cmsis/NNSupportFunctions/subdir.mk
-include Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/subdir.mk
-include Core/Src/TinyEngine/src/arm_cmsis/ConvolutionFunctions/subdir.mk
-include Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/subdir.mk
-include Core/Src/TinyEngine/src/arm_cmsis/BasicMathFunctions/subdir.mk
-include Core/Src/TinyEngine/src/arm_cmsis/ActivationFunctions/subdir.mk
-include Core/Src/subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

OPTIONAL_TOOL_DEPS := \
$(wildcard ../makefile.defs) \
$(wildcard ../makefile.init) \
$(wildcard ../makefile.targets) \


BUILD_ARTIFACT_NAME := TinyEngineTemplateCleanR5Zi
BUILD_ARTIFACT_EXTENSION := elf
BUILD_ARTIFACT_PREFIX :=
BUILD_ARTIFACT := $(BUILD_ARTIFACT_PREFIX)$(BUILD_ARTIFACT_NAME)$(if $(BUILD_ARTIFACT_EXTENSION),.$(BUILD_ARTIFACT_EXTENSION),)

# Add inputs and outputs from these tool invocations to the build variables 
EXECUTABLES += \
TinyEngineTemplateCleanR5Zi.elf \

MAP_FILES += \
TinyEngineTemplateCleanR5Zi.map \

SIZE_OUTPUT += \
default.size.stdout \

OBJDUMP_LIST += \
TinyEngineTemplateCleanR5Zi.list \


# All Target
all: main-build

# Main-build Target
main-build: TinyEngineTemplateCleanR5Zi.elf secondary-outputs

# Tool invocations
TinyEngineTemplateCleanR5Zi.elf TinyEngineTemplateCleanR5Zi.map: $(OBJS) $(USER_OBJS) /home/matthias/Documents/BA/layer-benchmark-2/src/tiny_engine/cube_templates/TinyEngineTemplateCleanR5Zi/STM32L4R5ZITX_FLASH.ld makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-gcc -o "TinyEngineTemplateCleanR5Zi.elf" @"objects.list" $(USER_OBJS) $(LIBS) -mcpu=cortex-m4 -T"/home/matthias/Documents/BA/layer-benchmark-2/src/tiny_engine/cube_templates/TinyEngineTemplateCleanR5Zi/STM32L4R5ZITX_FLASH.ld" --specs=nosys.specs -Wl,-Map="TinyEngineTemplateCleanR5Zi.map" -Wl,--gc-sections -static --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -Wl,--start-group -lc -lm -Wl,--end-group
	@echo 'Finished building target: $@'
	@echo ' '

default.size.stdout: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-size  $(EXECUTABLES)
	@echo 'Finished building: $@'
	@echo ' '

TinyEngineTemplateCleanR5Zi.list: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	arm-none-eabi-objdump -h -S $(EXECUTABLES) > "TinyEngineTemplateCleanR5Zi.list"
	@echo 'Finished building: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) TinyEngineTemplateCleanR5Zi.elf TinyEngineTemplateCleanR5Zi.list TinyEngineTemplateCleanR5Zi.map default.size.stdout
	-@echo ' '

secondary-outputs: $(SIZE_OUTPUT) $(OBJDUMP_LIST)

fail-specified-linker-script-missing:
	@echo 'Error: Cannot find the specified linker script. Check the linker settings in the build configuration.'
	@exit 2

warn-no-linker-script-specified:
	@echo 'Warning: No linker script specified. Check the linker settings in the build configuration.'

.PHONY: all clean dependents main-build fail-specified-linker-script-missing warn-no-linker-script-specified

-include ../makefile.targets
