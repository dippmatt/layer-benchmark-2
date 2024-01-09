################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CC_SRCS += \
../Middlewares/tensorflow/tensorflow/lite/core/api/error_reporter.cc \
../Middlewares/tensorflow/tensorflow/lite/core/api/flatbuffer_conversions.cc \
../Middlewares/tensorflow/tensorflow/lite/core/api/op_resolver.cc \
../Middlewares/tensorflow/tensorflow/lite/core/api/tensor_utils.cc 

CC_DEPS += \
./Middlewares/tensorflow/tensorflow/lite/core/api/error_reporter.d \
./Middlewares/tensorflow/tensorflow/lite/core/api/flatbuffer_conversions.d \
./Middlewares/tensorflow/tensorflow/lite/core/api/op_resolver.d \
./Middlewares/tensorflow/tensorflow/lite/core/api/tensor_utils.d 

OBJS += \
./Middlewares/tensorflow/tensorflow/lite/core/api/error_reporter.o \
./Middlewares/tensorflow/tensorflow/lite/core/api/flatbuffer_conversions.o \
./Middlewares/tensorflow/tensorflow/lite/core/api/op_resolver.o \
./Middlewares/tensorflow/tensorflow/lite/core/api/tensor_utils.o 


# Each subdirectory must supply rules for building sources it contributes
Middlewares/tensorflow/tensorflow/lite/core/api/%.o Middlewares/tensorflow/tensorflow/lite/core/api/%.su: ../Middlewares/tensorflow/tensorflow/lite/core/api/%.cc Middlewares/tensorflow/tensorflow/lite/core/api/subdir.mk
	arm-none-eabi-g++ "$<" -mcpu=cortex-m4 -std=gnu++14 -DDEBUG -DTFLM_RUNTIME -DCMSIS_NN -DTFLM_RUNTIME_USE_ALL_OPERATORS=0 -DTF_LITE_STATIC_MEMORY -DTF_LITE_DISABLE_X86_NEON -DTF_LITE_MCU_DEBUG_LOG -DARM_MATH -DARM_MATH_LOOPUNROLL -DARM_MATH_DSP -DARM_MATH_CM4 -D__FPU_PRESENT=1U -DUSE_HAL_DRIVER -DSTM32L4R5xx -c -I../X-CUBE-AI/App -I../X-CUBE-AI -I../X-CUBE-AI/Target -I../Core/Inc -I../Middlewares/tensorflow/third_party/cmsis_nn/Include -I../Middlewares/tensorflow -I../Middlewares/tensorflow/third_party/cmsis_nn/Include/Internal -I../Middlewares/ST/AI/Inc -I../Middlewares/tensorflow/third_party/cmsis_nn -I../Middlewares/tensorflow/third_party/flatbuffers/include -I../Middlewares/tensorflow/third_party/cmsis/CMSIS/Core/Include -I../Middlewares/tensorflow/third_party/gemmlowp -I../Middlewares/tensorflow/third_party/cmsis/CMSIS/Core -I../Middlewares/tensorflow/third_party/ruy -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -Os -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Middlewares-2f-tensorflow-2f-tensorflow-2f-lite-2f-core-2f-api

clean-Middlewares-2f-tensorflow-2f-tensorflow-2f-lite-2f-core-2f-api:
	-$(RM) ./Middlewares/tensorflow/tensorflow/lite/core/api/error_reporter.d ./Middlewares/tensorflow/tensorflow/lite/core/api/error_reporter.o ./Middlewares/tensorflow/tensorflow/lite/core/api/error_reporter.su ./Middlewares/tensorflow/tensorflow/lite/core/api/flatbuffer_conversions.d ./Middlewares/tensorflow/tensorflow/lite/core/api/flatbuffer_conversions.o ./Middlewares/tensorflow/tensorflow/lite/core/api/flatbuffer_conversions.su ./Middlewares/tensorflow/tensorflow/lite/core/api/op_resolver.d ./Middlewares/tensorflow/tensorflow/lite/core/api/op_resolver.o ./Middlewares/tensorflow/tensorflow/lite/core/api/op_resolver.su ./Middlewares/tensorflow/tensorflow/lite/core/api/tensor_utils.d ./Middlewares/tensorflow/tensorflow/lite/core/api/tensor_utils.o ./Middlewares/tensorflow/tensorflow/lite/core/api/tensor_utils.su

.PHONY: clean-Middlewares-2f-tensorflow-2f-tensorflow-2f-lite-2f-core-2f-api

