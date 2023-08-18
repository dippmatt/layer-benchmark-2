################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15.c \
../Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15_opt.c \
../Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15.c \
../Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15_opt.c \
../Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7.c \
../Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7_opt.c \
../Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s16.c \
../Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s8.c 

OBJS += \
./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15.o \
./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15_opt.o \
./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15.o \
./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15_opt.o \
./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7.o \
./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7_opt.o \
./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s16.o \
./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s8.o 

C_DEPS += \
./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15.d \
./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15_opt.d \
./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15.d \
./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15_opt.d \
./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7.d \
./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7_opt.d \
./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s16.d \
./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s8.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/%.o Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/%.su: ../Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/%.c Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32L4R5xx -c -I../Core/Inc -I../Core/Src/TinyEngine/src/arm_cmsis/ActivationFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/BasicMathFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/ConvolutionFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/NNSupportFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/ReshapeFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/SoftmaxFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/SVDFunctions -I../Core/Src -I../Core/Src/TinyEngine/include -I../Core/Src/TinyEngine/include/arm_cmsis -I../Core/Src/TinyEngine/codegen/Include -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../Drivers/CMSIS/Include -Ofast -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-Src-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-FullyConnectedFunctions

clean-Core-2f-Src-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-FullyConnectedFunctions:
	-$(RM) ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15.d ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15.o ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15.su ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15_opt.d ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15_opt.o ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15_opt.su ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15.d ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15.o ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15.su ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15_opt.d ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15_opt.o ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15_opt.su ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7.d ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7.o ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7.su ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7_opt.d ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7_opt.o ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7_opt.su ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s16.d ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s16.o ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s16.su ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s8.d ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s8.o ./Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s8.su

.PHONY: clean-Core-2f-Src-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-FullyConnectedFunctions

