################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1_x_n_s8.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1x1_HWC_q7_fast_nonsquare.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1x1_s8_fast.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_basic.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_fast.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_fast_nonsquare.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_RGB.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_basic.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_basic_nonsquare.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_fast.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_fast_nonsquare.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_fast_s16.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_s16.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_s8.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_wrapper_s16.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_wrapper_s8.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_3x3_s8.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s16.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s8.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s8_opt.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_u8_basic_ver1.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_wrapper_s8.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_separable_conv_HWC_q7.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_separable_conv_HWC_q7_nonsquare.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_depthwise_conv_s8_core.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_q7_q15.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_q7_q15_reordered.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_s8_s16.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_s8_s16_reordered.c \
../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_s8.c 

OBJS += \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1_x_n_s8.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1x1_HWC_q7_fast_nonsquare.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1x1_s8_fast.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_basic.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_fast.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_fast_nonsquare.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_RGB.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_basic.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_basic_nonsquare.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_fast.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_fast_nonsquare.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_fast_s16.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_s16.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_s8.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_wrapper_s16.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_wrapper_s8.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_3x3_s8.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s16.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s8.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s8_opt.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_u8_basic_ver1.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_wrapper_s8.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_separable_conv_HWC_q7.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_separable_conv_HWC_q7_nonsquare.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_depthwise_conv_s8_core.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_q7_q15.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_q7_q15_reordered.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_s8_s16.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_s8_s16_reordered.o \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_s8.o 

C_DEPS += \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1_x_n_s8.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1x1_HWC_q7_fast_nonsquare.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1x1_s8_fast.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_basic.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_fast.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_fast_nonsquare.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_RGB.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_basic.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_basic_nonsquare.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_fast.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_fast_nonsquare.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_fast_s16.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_s16.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_s8.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_wrapper_s16.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_wrapper_s8.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_3x3_s8.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s16.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s8.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s8_opt.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_u8_basic_ver1.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_wrapper_s8.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_separable_conv_HWC_q7.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_separable_conv_HWC_q7_nonsquare.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_depthwise_conv_s8_core.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_q7_q15.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_q7_q15_reordered.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_s8_s16.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_s8_s16_reordered.d \
./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_s8.d 


# Each subdirectory must supply rules for building sources it contributes
Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/%.o Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/%.su: ../Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/%.c Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32L4R5xx -c -I../Core/Inc -I../Core/Src/TinyEngine/include/arm_cmsis -I../Core/Src/TinyEngine/include -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-ConvolutionFunctions

clean-Core-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-ConvolutionFunctions:
	-$(RM) ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1_x_n_s8.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1_x_n_s8.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1_x_n_s8.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1x1_HWC_q7_fast_nonsquare.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1x1_HWC_q7_fast_nonsquare.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1x1_HWC_q7_fast_nonsquare.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1x1_s8_fast.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1x1_s8_fast.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_1x1_s8_fast.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_basic.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_basic.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_basic.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_fast.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_fast.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_fast.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_fast_nonsquare.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_fast_nonsquare.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q15_fast_nonsquare.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_RGB.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_RGB.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_RGB.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_basic.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_basic.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_basic.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_basic_nonsquare.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_basic_nonsquare.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_basic_nonsquare.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_fast.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_fast.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_fast.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_fast_nonsquare.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_fast_nonsquare.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_HWC_q7_fast_nonsquare.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_fast_s16.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_fast_s16.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_fast_s16.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_s16.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_s16.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_s16.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_s8.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_s8.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_s8.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_wrapper_s16.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_wrapper_s16.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_wrapper_s16.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_wrapper_s8.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_wrapper_s8.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_convolve_wrapper_s8.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_3x3_s8.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_3x3_s8.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_3x3_s8.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s16.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s16.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s16.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s8.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s8.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s8.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s8_opt.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s8_opt.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_s8_opt.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_u8_basic_ver1.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_u8_basic_ver1.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_u8_basic_ver1.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_wrapper_s8.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_wrapper_s8.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_conv_wrapper_s8.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_separable_conv_HWC_q7.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_separable_conv_HWC_q7.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_separable_conv_HWC_q7.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_separable_conv_HWC_q7_nonsquare.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_separable_conv_HWC_q7_nonsquare.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_depthwise_separable_conv_HWC_q7_nonsquare.su
	-$(RM) ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_depthwise_conv_s8_core.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_depthwise_conv_s8_core.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_depthwise_conv_s8_core.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_q7_q15.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_q7_q15.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_q7_q15.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_q7_q15_reordered.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_q7_q15_reordered.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_q7_q15_reordered.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_s8_s16.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_s8_s16.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_s8_s16.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_s8_s16_reordered.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_s8_s16_reordered.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_kernel_s8_s16_reordered.su ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_s8.d ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_s8.o ./Core/TinyEngine/src/arm_cmsis/ConvolutionFunctions/arm_nn_mat_mult_s8.su

.PHONY: clean-Core-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-ConvolutionFunctions

