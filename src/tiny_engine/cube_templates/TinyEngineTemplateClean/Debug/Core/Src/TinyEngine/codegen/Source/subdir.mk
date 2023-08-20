################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Src/TinyEngine/codegen/Source/genModel.c 

OBJS += \
./Core/Src/TinyEngine/codegen/Source/genModel.o 

C_DEPS += \
./Core/Src/TinyEngine/codegen/Source/genModel.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Src/TinyEngine/codegen/Source/%.o Core/Src/TinyEngine/codegen/Source/%.su: ../Core/Src/TinyEngine/codegen/Source/%.c Core/Src/TinyEngine/codegen/Source/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32L432xx -c -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../Drivers/CMSIS/Include -I../Core/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Core/Src/TinyEngine/include -I../Core/Src/TinyEngine/include/arm_cmsis -I../Core/Src/TinyEngine/codegen/Include -I../Core/Src/TinyEngine/src/arm_cmsis/ActivationFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/BasicMathFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/ConvolutionFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/NNSupportFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/ReshapeFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/SoftmaxFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/SVDFunctions -O3 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-Src-2f-TinyEngine-2f-codegen-2f-Source

clean-Core-2f-Src-2f-TinyEngine-2f-codegen-2f-Source:
	-$(RM) ./Core/Src/TinyEngine/codegen/Source/genModel.d ./Core/Src/TinyEngine/codegen/Source/genModel.o ./Core/Src/TinyEngine/codegen/Source/genModel.su

.PHONY: clean-Core-2f-Src-2f-TinyEngine-2f-codegen-2f-Source

