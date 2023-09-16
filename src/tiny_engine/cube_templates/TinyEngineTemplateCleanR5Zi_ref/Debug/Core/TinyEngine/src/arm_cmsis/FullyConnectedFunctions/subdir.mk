################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15.c \
../Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15_opt.c \
../Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15.c \
../Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15_opt.c \
../Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7.c \
../Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7_opt.c \
../Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s16.c \
../Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s8.c 

OBJS += \
./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15.o \
./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15_opt.o \
./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15.o \
./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15_opt.o \
./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7.o \
./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7_opt.o \
./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s16.o \
./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s8.o 

C_DEPS += \
./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15.d \
./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15_opt.d \
./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15.d \
./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15_opt.d \
./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7.d \
./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7_opt.d \
./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s16.d \
./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s8.d 


# Each subdirectory must supply rules for building sources it contributes
Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/%.o Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/%.su: ../Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/%.c Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32L4R5xx -c -I../Core/Inc -I../Core/Src/TinyEngine/include/arm_cmsis -I../Core/Src/TinyEngine/include -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-FullyConnectedFunctions

clean-Core-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-FullyConnectedFunctions:
	-$(RM) ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15.d ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15.o ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15.su ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15_opt.d ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15_opt.o ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_mat_q7_vec_q15_opt.su ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15.d ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15.o ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15.su ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15_opt.d ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15_opt.o ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q15_opt.su ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7.d ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7.o ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7.su ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7_opt.d ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7_opt.o ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_q7_opt.su ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s16.d ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s16.o ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s16.su ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s8.d ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s8.o ./Core/TinyEngine/src/arm_cmsis/FullyConnectedFunctions/arm_fully_connected_s8.su

.PHONY: clean-Core-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-FullyConnectedFunctions
