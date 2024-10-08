################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_avgpool_s8.c \
../Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_max_pool_s8.c \
../Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_pool_q7_HWC.c 

OBJS += \
./Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_avgpool_s8.o \
./Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_max_pool_s8.o \
./Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_pool_q7_HWC.o 

C_DEPS += \
./Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_avgpool_s8.d \
./Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_max_pool_s8.d \
./Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_pool_q7_HWC.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/%.o Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/%.su: ../Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/%.c Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32L4R5xx -c -I../Core/Src/TinyEngine/src/arm_cmsis/ActivationFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/BasicMathFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/ConcatenationFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/ConvolutionFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/FullyConnectedFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/NNSupportFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/ReshapeFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/SoftmaxFunctions -I../Core/Src/TinyEngine/src/arm_cmsis/SVDFunctions -I../Core/Src/TinyEngine/include -I../Core/Src/TinyEngine/include/arm_cmsis -I../Core/Src/TinyEngine/codegen/Include -I../Core/Inc -I../Core/Src -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../Drivers/CMSIS/Include -O3 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-Src-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-PoolingFunctions

clean-Core-2f-Src-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-PoolingFunctions:
	-$(RM) ./Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_avgpool_s8.d ./Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_avgpool_s8.o ./Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_avgpool_s8.su ./Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_max_pool_s8.d ./Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_max_pool_s8.o ./Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_max_pool_s8.su ./Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_pool_q7_HWC.d ./Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_pool_q7_HWC.o ./Core/Src/TinyEngine/src/arm_cmsis/PoolingFunctions/arm_pool_q7_HWC.su

.PHONY: clean-Core-2f-Src-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-PoolingFunctions

