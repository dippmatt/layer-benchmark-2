################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CC_SRCS += \
../Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/non_persistent_arena_buffer_allocator.cc \
../Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/persistent_arena_buffer_allocator.cc \
../Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/recording_single_arena_buffer_allocator.cc \
../Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/single_arena_buffer_allocator.cc 

CC_DEPS += \
./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/non_persistent_arena_buffer_allocator.d \
./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/persistent_arena_buffer_allocator.d \
./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/recording_single_arena_buffer_allocator.d \
./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/single_arena_buffer_allocator.d 

OBJS += \
./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/non_persistent_arena_buffer_allocator.o \
./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/persistent_arena_buffer_allocator.o \
./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/recording_single_arena_buffer_allocator.o \
./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/single_arena_buffer_allocator.o 


# Each subdirectory must supply rules for building sources it contributes
Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/%.o Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/%.su: ../Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/%.cc Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/subdir.mk
	arm-none-eabi-g++ "$<" -mcpu=cortex-m4 -std=gnu++14 -g3 -DDEBUG -DTFLM_RUNTIME -DCMSIS_NN -DTFLM_RUNTIME_USE_ALL_OPERATORS=0 -DTF_LITE_STATIC_MEMORY -DTF_LITE_DISABLE_X86_NEON -DTF_LITE_MCU_DEBUG_LOG -DARM_MATH -DARM_MATH_LOOPUNROLL -DARM_MATH_DSP -DARM_MATH_CM4 -D__FPU_PRESENT=1U -DUSE_HAL_DRIVER -DSTM32L4R5xx -c -I../X-CUBE-AI/App -I../X-CUBE-AI -I../X-CUBE-AI/Target -I../Core/Inc -I../Middlewares/tensorflow/third_party/cmsis_nn/Include -I../Middlewares/tensorflow -I../Middlewares/tensorflow/third_party/cmsis_nn/Include/Internal -I../Middlewares/tensorflow/third_party/cmsis_nn -I../Middlewares/tensorflow/third_party/flatbuffers/include -I../Middlewares/tensorflow/third_party/cmsis/CMSIS/Core/Include -I../Middlewares/tensorflow/third_party/gemmlowp -I../Middlewares/tensorflow/third_party/cmsis/CMSIS/Core -I../Middlewares/tensorflow/third_party/ruy -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -Os -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Middlewares-2f-tensorflow-2f-tensorflow-2f-lite-2f-micro-2f-arena_allocator

clean-Middlewares-2f-tensorflow-2f-tensorflow-2f-lite-2f-micro-2f-arena_allocator:
	-$(RM) ./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/non_persistent_arena_buffer_allocator.d ./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/non_persistent_arena_buffer_allocator.o ./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/non_persistent_arena_buffer_allocator.su ./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/persistent_arena_buffer_allocator.d ./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/persistent_arena_buffer_allocator.o ./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/persistent_arena_buffer_allocator.su ./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/recording_single_arena_buffer_allocator.d ./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/recording_single_arena_buffer_allocator.o ./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/recording_single_arena_buffer_allocator.su ./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/single_arena_buffer_allocator.d ./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/single_arena_buffer_allocator.o ./Middlewares/tensorflow/tensorflow/lite/micro/arena_allocator/single_arena_buffer_allocator.su

.PHONY: clean-Middlewares-2f-tensorflow-2f-tensorflow-2f-lite-2f-micro-2f-arena_allocator

