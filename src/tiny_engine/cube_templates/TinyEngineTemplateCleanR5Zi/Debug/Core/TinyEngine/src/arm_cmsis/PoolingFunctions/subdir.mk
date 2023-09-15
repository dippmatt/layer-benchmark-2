################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_avgpool_s8.c \
../Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_max_pool_s8.c \
../Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_pool_q7_HWC.c 

OBJS += \
./Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_avgpool_s8.o \
./Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_max_pool_s8.o \
./Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_pool_q7_HWC.o 

C_DEPS += \
./Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_avgpool_s8.d \
./Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_max_pool_s8.d \
./Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_pool_q7_HWC.d 


# Each subdirectory must supply rules for building sources it contributes
Core/TinyEngine/src/arm_cmsis/PoolingFunctions/%.o Core/TinyEngine/src/arm_cmsis/PoolingFunctions/%.su: ../Core/TinyEngine/src/arm_cmsis/PoolingFunctions/%.c Core/TinyEngine/src/arm_cmsis/PoolingFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32L4R5xx -c -I../Core/Inc -I../Core/Src/TinyEngine/include/arm_cmsis -I../Core/Src/TinyEngine/include -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-PoolingFunctions

clean-Core-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-PoolingFunctions:
	-$(RM) ./Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_avgpool_s8.d ./Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_avgpool_s8.o ./Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_avgpool_s8.su ./Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_max_pool_s8.d ./Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_max_pool_s8.o ./Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_max_pool_s8.su ./Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_pool_q7_HWC.d ./Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_pool_q7_HWC.o ./Core/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_pool_q7_HWC.su

.PHONY: clean-Core-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-PoolingFunctions

