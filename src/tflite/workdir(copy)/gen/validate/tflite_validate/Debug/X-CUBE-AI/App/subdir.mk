################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CC_SRCS += \
../X-CUBE-AI/App/debug_log_imp.cc \
../X-CUBE-AI/App/tflm_c.cc 

C_SRCS += \
../X-CUBE-AI/App/aiPbIO.c \
../X-CUBE-AI/App/aiPbMemRWServices.c \
../X-CUBE-AI/App/aiPbMgr.c \
../X-CUBE-AI/App/aiTestHelper.c \
../X-CUBE-AI/App/aiTestUtility.c \
../X-CUBE-AI/App/aiValidation_TFLM.c \
../X-CUBE-AI/App/ai_device_adaptor.c \
../X-CUBE-AI/App/app_x-cube-ai.c \
../X-CUBE-AI/App/lc_print.c \
../X-CUBE-AI/App/network.c \
../X-CUBE-AI/App/pb_common.c \
../X-CUBE-AI/App/pb_decode.c \
../X-CUBE-AI/App/pb_encode.c \
../X-CUBE-AI/App/stm32msg.pb.c 

C_DEPS += \
./X-CUBE-AI/App/aiPbIO.d \
./X-CUBE-AI/App/aiPbMemRWServices.d \
./X-CUBE-AI/App/aiPbMgr.d \
./X-CUBE-AI/App/aiTestHelper.d \
./X-CUBE-AI/App/aiTestUtility.d \
./X-CUBE-AI/App/aiValidation_TFLM.d \
./X-CUBE-AI/App/ai_device_adaptor.d \
./X-CUBE-AI/App/app_x-cube-ai.d \
./X-CUBE-AI/App/lc_print.d \
./X-CUBE-AI/App/network.d \
./X-CUBE-AI/App/pb_common.d \
./X-CUBE-AI/App/pb_decode.d \
./X-CUBE-AI/App/pb_encode.d \
./X-CUBE-AI/App/stm32msg.pb.d 

CC_DEPS += \
./X-CUBE-AI/App/debug_log_imp.d \
./X-CUBE-AI/App/tflm_c.d 

OBJS += \
./X-CUBE-AI/App/aiPbIO.o \
./X-CUBE-AI/App/aiPbMemRWServices.o \
./X-CUBE-AI/App/aiPbMgr.o \
./X-CUBE-AI/App/aiTestHelper.o \
./X-CUBE-AI/App/aiTestUtility.o \
./X-CUBE-AI/App/aiValidation_TFLM.o \
./X-CUBE-AI/App/ai_device_adaptor.o \
./X-CUBE-AI/App/app_x-cube-ai.o \
./X-CUBE-AI/App/debug_log_imp.o \
./X-CUBE-AI/App/lc_print.o \
./X-CUBE-AI/App/network.o \
./X-CUBE-AI/App/pb_common.o \
./X-CUBE-AI/App/pb_decode.o \
./X-CUBE-AI/App/pb_encode.o \
./X-CUBE-AI/App/stm32msg.pb.o \
./X-CUBE-AI/App/tflm_c.o 


# Each subdirectory must supply rules for building sources it contributes
X-CUBE-AI/App/%.o X-CUBE-AI/App/%.su: ../X-CUBE-AI/App/%.c X-CUBE-AI/App/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DTFLM_RUNTIME -DCMSIS_NN -DTFLM_RUNTIME_USE_ALL_OPERATORS=0 -DTF_LITE_STATIC_MEMORY -DTF_LITE_DISABLE_X86_NEON -DTF_LITE_MCU_DEBUG_LOG -DARM_MATH -DARM_MATH_LOOPUNROLL -DARM_MATH_DSP -DARM_MATH_CM4 -D__FPU_PRESENT=1U -DUSE_HAL_DRIVER -DSTM32L4R5xx -c -I../X-CUBE-AI/App -I../X-CUBE-AI -I../X-CUBE-AI/Target -I../Core/Inc -I../Middlewares/tensorflow/third_party/cmsis_nn/Include -I../Middlewares/tensorflow -I../Middlewares/tensorflow/third_party/cmsis_nn/Include/Internal -I../Middlewares/ST/AI/Inc -I../Middlewares/tensorflow/third_party/cmsis_nn -I../Middlewares/tensorflow/third_party/flatbuffers/include -I../Middlewares/tensorflow/third_party/cmsis/CMSIS/Core/Include -I../Middlewares/tensorflow/third_party/gemmlowp -I../Middlewares/tensorflow/third_party/cmsis/CMSIS/Core -I../Middlewares/tensorflow/third_party/ruy -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -O3 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"
X-CUBE-AI/App/%.o X-CUBE-AI/App/%.su: ../X-CUBE-AI/App/%.cc X-CUBE-AI/App/subdir.mk
	arm-none-eabi-g++ "$<" -mcpu=cortex-m4 -std=gnu++14 -g3 -DDEBUG -DTFLM_RUNTIME -DCMSIS_NN -DTFLM_RUNTIME_USE_ALL_OPERATORS=0 -DTF_LITE_STATIC_MEMORY -DTF_LITE_DISABLE_X86_NEON -DTF_LITE_MCU_DEBUG_LOG -DARM_MATH -DARM_MATH_LOOPUNROLL -DARM_MATH_DSP -DARM_MATH_CM4 -D__FPU_PRESENT=1U -DUSE_HAL_DRIVER -DSTM32L4R5xx -c -I../X-CUBE-AI/App -I../X-CUBE-AI -I../X-CUBE-AI/Target -I../Core/Inc -I../Middlewares/tensorflow/third_party/cmsis_nn/Include -I../Middlewares/tensorflow -I../Middlewares/tensorflow/third_party/cmsis_nn/Include/Internal -I../Middlewares/ST/AI/Inc -I../Middlewares/tensorflow/third_party/cmsis_nn -I../Middlewares/tensorflow/third_party/flatbuffers/include -I../Middlewares/tensorflow/third_party/cmsis/CMSIS/Core/Include -I../Middlewares/tensorflow/third_party/gemmlowp -I../Middlewares/tensorflow/third_party/cmsis/CMSIS/Core -I../Middlewares/tensorflow/third_party/ruy -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -Os -ffunction-sections -fdata-sections -fno-exceptions -fno-rtti -fno-use-cxa-atexit -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-X-2d-CUBE-2d-AI-2f-App

clean-X-2d-CUBE-2d-AI-2f-App:
	-$(RM) ./X-CUBE-AI/App/aiPbIO.d ./X-CUBE-AI/App/aiPbIO.o ./X-CUBE-AI/App/aiPbIO.su ./X-CUBE-AI/App/aiPbMemRWServices.d ./X-CUBE-AI/App/aiPbMemRWServices.o ./X-CUBE-AI/App/aiPbMemRWServices.su ./X-CUBE-AI/App/aiPbMgr.d ./X-CUBE-AI/App/aiPbMgr.o ./X-CUBE-AI/App/aiPbMgr.su ./X-CUBE-AI/App/aiTestHelper.d ./X-CUBE-AI/App/aiTestHelper.o ./X-CUBE-AI/App/aiTestHelper.su ./X-CUBE-AI/App/aiTestUtility.d ./X-CUBE-AI/App/aiTestUtility.o ./X-CUBE-AI/App/aiTestUtility.su ./X-CUBE-AI/App/aiValidation_TFLM.d ./X-CUBE-AI/App/aiValidation_TFLM.o ./X-CUBE-AI/App/aiValidation_TFLM.su ./X-CUBE-AI/App/ai_device_adaptor.d ./X-CUBE-AI/App/ai_device_adaptor.o ./X-CUBE-AI/App/ai_device_adaptor.su ./X-CUBE-AI/App/app_x-cube-ai.d ./X-CUBE-AI/App/app_x-cube-ai.o ./X-CUBE-AI/App/app_x-cube-ai.su ./X-CUBE-AI/App/debug_log_imp.d ./X-CUBE-AI/App/debug_log_imp.o ./X-CUBE-AI/App/debug_log_imp.su ./X-CUBE-AI/App/lc_print.d ./X-CUBE-AI/App/lc_print.o ./X-CUBE-AI/App/lc_print.su ./X-CUBE-AI/App/network.d ./X-CUBE-AI/App/network.o ./X-CUBE-AI/App/network.su ./X-CUBE-AI/App/pb_common.d ./X-CUBE-AI/App/pb_common.o ./X-CUBE-AI/App/pb_common.su ./X-CUBE-AI/App/pb_decode.d ./X-CUBE-AI/App/pb_decode.o ./X-CUBE-AI/App/pb_decode.su ./X-CUBE-AI/App/pb_encode.d ./X-CUBE-AI/App/pb_encode.o ./X-CUBE-AI/App/pb_encode.su ./X-CUBE-AI/App/stm32msg.pb.d ./X-CUBE-AI/App/stm32msg.pb.o ./X-CUBE-AI/App/stm32msg.pb.su ./X-CUBE-AI/App/tflm_c.d ./X-CUBE-AI/App/tflm_c.o ./X-CUBE-AI/App/tflm_c.su

.PHONY: clean-X-2d-CUBE-2d-AI-2f-App
