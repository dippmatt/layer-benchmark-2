################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_q15.c \
../Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_q7.c \
../Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_s8.c \
../Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_u8.c \
../Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_with_batch_q7.c 

OBJS += \
./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_q15.o \
./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_q7.o \
./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_s8.o \
./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_u8.o \
./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_with_batch_q7.o 

C_DEPS += \
./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_q15.d \
./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_q7.d \
./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_s8.d \
./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_u8.d \
./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_with_batch_q7.d 


# Each subdirectory must supply rules for building sources it contributes
Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/%.o Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/%.su: ../Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/%.c Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32L4R5xx -c -I../Core/Inc -I../Core/Src/TinyEngine/include/arm_cmsis -I../Core/Src/TinyEngine/include -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../Drivers/CMSIS/Include -O3 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-SoftmaxFunctions

clean-Core-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-SoftmaxFunctions:
	-$(RM) ./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_q15.d ./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_q15.o ./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_q15.su ./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_q7.d ./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_q7.o ./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_q7.su ./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_s8.d ./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_s8.o ./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_s8.su ./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_u8.d ./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_u8.o ./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_u8.su ./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_with_batch_q7.d ./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_with_batch_q7.o ./Core/TinyEngine/src/arm_cmsis/SoftmaxFunctions/arm_softmax_with_batch_q7.su

.PHONY: clean-Core-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-SoftmaxFunctions

