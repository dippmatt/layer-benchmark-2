################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_w.c \
../Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_x.c \
../Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_y.c \
../Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_z.c 

OBJS += \
./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_w.o \
./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_x.o \
./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_y.o \
./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_z.o 

C_DEPS += \
./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_w.d \
./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_x.d \
./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_y.d \
./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_z.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/%.o Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/%.su: ../Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/%.c Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32L4R5xx -c -I../Core/Inc -I../Core/Src/TinyEngine/src/arm_cmsis/ActivationFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/BasicMathFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/ConvolutionFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/NNSupportFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/ReshapeFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/SoftmaxFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/SVDFunctions -I../Core/Src -I../Core/Src/TinyEngine/include -I../Core/Src/TinyEngine/include/arm_cmsis -I../Core/Src/TinyEngine/codegen/Include -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../Drivers/CMSIS/Include -Ofast -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-Src-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-ConcatenationFunctions

clean-Core-2f-Src-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-ConcatenationFunctions:
	-$(RM) ./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_w.d ./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_w.o ./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_w.su ./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_x.d ./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_x.o ./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_x.su ./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_y.d ./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_y.o ./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_y.su ./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_z.d ./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_z.o ./Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions/arm_concatenation_s8_z.su

.PHONY: clean-Core-2f-Src-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-ConcatenationFunctions

