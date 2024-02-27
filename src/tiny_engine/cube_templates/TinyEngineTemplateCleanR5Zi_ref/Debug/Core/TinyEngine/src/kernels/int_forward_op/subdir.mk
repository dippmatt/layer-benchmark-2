################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/TinyEngine/src/kernels/int_forward_op/add.c \
../Core/TinyEngine/src/kernels/int_forward_op/arm_convolve_s8_4col.c \
../Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel3_input3_s8_s16.c \
../Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel_s8_s16_reordered_8mul.c \
../Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel_s8_s16_reordered_oddch.c \
../Core/TinyEngine/src/kernels/int_forward_op/avgpooling.c \
../Core/TinyEngine/src/kernels/int_forward_op/concat_ch.c \
../Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8.c \
../Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_SRAM.c \
../Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch16.c \
../Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch24.c \
../Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch48.c \
../Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch8.c \
../Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_kbuf.c \
../Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_oddch.c \
../Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_skip_pad.c \
../Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel2x3_inputch3_stride2_pad1.c \
../Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3_inputch3_stride2_pad1.c \
../Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3_stride1_pad1.c \
../Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3x2_inputch3_stride2_pad1.c \
../Core/TinyEngine/src/kernels/int_forward_op/convolve_u8_kernel3_inputch3_stride1_pad1.c \
../Core/TinyEngine/src/kernels/int_forward_op/convolve_u8_kernel3_inputch3_stride2_pad1.c \
../Core/TinyEngine/src/kernels/int_forward_op/element_mult.c \
../Core/TinyEngine/src/kernels/int_forward_op/fully_connected.c \
../Core/TinyEngine/src/kernels/int_forward_op/mat_mul_fp.c \
../Core/TinyEngine/src/kernels/int_forward_op/mat_mult_kernels.c \
../Core/TinyEngine/src/kernels/int_forward_op/maxpooling.c \
../Core/TinyEngine/src/kernels/int_forward_op/patchpadding_convolve_s8_kernel3_inputch3_stride2.c \
../Core/TinyEngine/src/kernels/int_forward_op/patchpadding_depthwise_kernel3x3_stride1_inplace_CHW.c \
../Core/TinyEngine/src/kernels/int_forward_op/patchpadding_depthwise_kernel3x3_stride2_inplace_CHW.c \
../Core/TinyEngine/src/kernels/int_forward_op/patchpadding_kbuf_convolve_s8_kernel3_inputch3_stride2.c \
../Core/TinyEngine/src/kernels/int_forward_op/stable_softmax.c \
../Core/TinyEngine/src/kernels/int_forward_op/upsample_byte.c 

OBJS += \
./Core/TinyEngine/src/kernels/int_forward_op/add.o \
./Core/TinyEngine/src/kernels/int_forward_op/arm_convolve_s8_4col.o \
./Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel3_input3_s8_s16.o \
./Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel_s8_s16_reordered_8mul.o \
./Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel_s8_s16_reordered_oddch.o \
./Core/TinyEngine/src/kernels/int_forward_op/avgpooling.o \
./Core/TinyEngine/src/kernels/int_forward_op/concat_ch.o \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8.o \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_SRAM.o \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch16.o \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch24.o \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch48.o \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch8.o \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_kbuf.o \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_oddch.o \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_skip_pad.o \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel2x3_inputch3_stride2_pad1.o \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3_inputch3_stride2_pad1.o \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3_stride1_pad1.o \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3x2_inputch3_stride2_pad1.o \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_u8_kernel3_inputch3_stride1_pad1.o \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_u8_kernel3_inputch3_stride2_pad1.o \
./Core/TinyEngine/src/kernels/int_forward_op/element_mult.o \
./Core/TinyEngine/src/kernels/int_forward_op/fully_connected.o \
./Core/TinyEngine/src/kernels/int_forward_op/mat_mul_fp.o \
./Core/TinyEngine/src/kernels/int_forward_op/mat_mult_kernels.o \
./Core/TinyEngine/src/kernels/int_forward_op/maxpooling.o \
./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_convolve_s8_kernel3_inputch3_stride2.o \
./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_depthwise_kernel3x3_stride1_inplace_CHW.o \
./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_depthwise_kernel3x3_stride2_inplace_CHW.o \
./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_kbuf_convolve_s8_kernel3_inputch3_stride2.o \
./Core/TinyEngine/src/kernels/int_forward_op/stable_softmax.o \
./Core/TinyEngine/src/kernels/int_forward_op/upsample_byte.o 

C_DEPS += \
./Core/TinyEngine/src/kernels/int_forward_op/add.d \
./Core/TinyEngine/src/kernels/int_forward_op/arm_convolve_s8_4col.d \
./Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel3_input3_s8_s16.d \
./Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel_s8_s16_reordered_8mul.d \
./Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel_s8_s16_reordered_oddch.d \
./Core/TinyEngine/src/kernels/int_forward_op/avgpooling.d \
./Core/TinyEngine/src/kernels/int_forward_op/concat_ch.d \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8.d \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_SRAM.d \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch16.d \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch24.d \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch48.d \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch8.d \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_kbuf.d \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_oddch.d \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_skip_pad.d \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel2x3_inputch3_stride2_pad1.d \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3_inputch3_stride2_pad1.d \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3_stride1_pad1.d \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3x2_inputch3_stride2_pad1.d \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_u8_kernel3_inputch3_stride1_pad1.d \
./Core/TinyEngine/src/kernels/int_forward_op/convolve_u8_kernel3_inputch3_stride2_pad1.d \
./Core/TinyEngine/src/kernels/int_forward_op/element_mult.d \
./Core/TinyEngine/src/kernels/int_forward_op/fully_connected.d \
./Core/TinyEngine/src/kernels/int_forward_op/mat_mul_fp.d \
./Core/TinyEngine/src/kernels/int_forward_op/mat_mult_kernels.d \
./Core/TinyEngine/src/kernels/int_forward_op/maxpooling.d \
./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_convolve_s8_kernel3_inputch3_stride2.d \
./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_depthwise_kernel3x3_stride1_inplace_CHW.d \
./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_depthwise_kernel3x3_stride2_inplace_CHW.d \
./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_kbuf_convolve_s8_kernel3_inputch3_stride2.d \
./Core/TinyEngine/src/kernels/int_forward_op/stable_softmax.d \
./Core/TinyEngine/src/kernels/int_forward_op/upsample_byte.d 


# Each subdirectory must supply rules for building sources it contributes
Core/TinyEngine/src/kernels/int_forward_op/%.o Core/TinyEngine/src/kernels/int_forward_op/%.su: ../Core/TinyEngine/src/kernels/int_forward_op/%.c Core/TinyEngine/src/kernels/int_forward_op/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32L4R5xx -c -I../Core/Inc -I../Core/Src/TinyEngine/include/arm_cmsis -I../Core/Src/TinyEngine/include -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../Drivers/CMSIS/Include -O3 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-TinyEngine-2f-src-2f-kernels-2f-int_forward_op

clean-Core-2f-TinyEngine-2f-src-2f-kernels-2f-int_forward_op:
	-$(RM) ./Core/TinyEngine/src/kernels/int_forward_op/add.d ./Core/TinyEngine/src/kernels/int_forward_op/add.o ./Core/TinyEngine/src/kernels/int_forward_op/add.su ./Core/TinyEngine/src/kernels/int_forward_op/arm_convolve_s8_4col.d ./Core/TinyEngine/src/kernels/int_forward_op/arm_convolve_s8_4col.o ./Core/TinyEngine/src/kernels/int_forward_op/arm_convolve_s8_4col.su ./Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel3_input3_s8_s16.d ./Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel3_input3_s8_s16.o ./Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel3_input3_s8_s16.su ./Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel_s8_s16_reordered_8mul.d ./Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel_s8_s16_reordered_8mul.o ./Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel_s8_s16_reordered_8mul.su ./Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel_s8_s16_reordered_oddch.d ./Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel_s8_s16_reordered_oddch.o ./Core/TinyEngine/src/kernels/int_forward_op/arm_nn_mat_mult_kernel_s8_s16_reordered_oddch.su ./Core/TinyEngine/src/kernels/int_forward_op/avgpooling.d ./Core/TinyEngine/src/kernels/int_forward_op/avgpooling.o ./Core/TinyEngine/src/kernels/int_forward_op/avgpooling.su ./Core/TinyEngine/src/kernels/int_forward_op/concat_ch.d ./Core/TinyEngine/src/kernels/int_forward_op/concat_ch.o ./Core/TinyEngine/src/kernels/int_forward_op/concat_ch.su ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8.d ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8.o ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8.su ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_SRAM.d ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_SRAM.o ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_SRAM.su ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch16.d ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch16.o ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch16.su ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch24.d ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch24.o ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch24.su ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch48.d ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch48.o ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch48.su ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch8.d ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch8.o ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_ch8.su ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_kbuf.d ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_kbuf.o ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_kbuf.su ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_oddch.d ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_oddch.o ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_oddch.su ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_skip_pad.d ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_skip_pad.o ./Core/TinyEngine/src/kernels/int_forward_op/convolve_1x1_s8_skip_pad.su ./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel2x3_inputch3_stride2_pad1.d ./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel2x3_inputch3_stride2_pad1.o ./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel2x3_inputch3_stride2_pad1.su ./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3_inputch3_stride2_pad1.d ./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3_inputch3_stride2_pad1.o ./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3_inputch3_stride2_pad1.su ./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3_stride1_pad1.d ./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3_stride1_pad1.o ./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3_stride1_pad1.su ./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3x2_inputch3_stride2_pad1.d ./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3x2_inputch3_stride2_pad1.o ./Core/TinyEngine/src/kernels/int_forward_op/convolve_s8_kernel3x2_inputch3_stride2_pad1.su ./Core/TinyEngine/src/kernels/int_forward_op/convolve_u8_kernel3_inputch3_stride1_pad1.d ./Core/TinyEngine/src/kernels/int_forward_op/convolve_u8_kernel3_inputch3_stride1_pad1.o ./Core/TinyEngine/src/kernels/int_forward_op/convolve_u8_kernel3_inputch3_stride1_pad1.su ./Core/TinyEngine/src/kernels/int_forward_op/convolve_u8_kernel3_inputch3_stride2_pad1.d ./Core/TinyEngine/src/kernels/int_forward_op/convolve_u8_kernel3_inputch3_stride2_pad1.o ./Core/TinyEngine/src/kernels/int_forward_op/convolve_u8_kernel3_inputch3_stride2_pad1.su ./Core/TinyEngine/src/kernels/int_forward_op/element_mult.d ./Core/TinyEngine/src/kernels/int_forward_op/element_mult.o ./Core/TinyEngine/src/kernels/int_forward_op/element_mult.su ./Core/TinyEngine/src/kernels/int_forward_op/fully_connected.d ./Core/TinyEngine/src/kernels/int_forward_op/fully_connected.o ./Core/TinyEngine/src/kernels/int_forward_op/fully_connected.su ./Core/TinyEngine/src/kernels/int_forward_op/mat_mul_fp.d ./Core/TinyEngine/src/kernels/int_forward_op/mat_mul_fp.o ./Core/TinyEngine/src/kernels/int_forward_op/mat_mul_fp.su ./Core/TinyEngine/src/kernels/int_forward_op/mat_mult_kernels.d ./Core/TinyEngine/src/kernels/int_forward_op/mat_mult_kernels.o ./Core/TinyEngine/src/kernels/int_forward_op/mat_mult_kernels.su ./Core/TinyEngine/src/kernels/int_forward_op/maxpooling.d ./Core/TinyEngine/src/kernels/int_forward_op/maxpooling.o ./Core/TinyEngine/src/kernels/int_forward_op/maxpooling.su ./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_convolve_s8_kernel3_inputch3_stride2.d
	-$(RM) ./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_convolve_s8_kernel3_inputch3_stride2.o ./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_convolve_s8_kernel3_inputch3_stride2.su ./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_depthwise_kernel3x3_stride1_inplace_CHW.d ./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_depthwise_kernel3x3_stride1_inplace_CHW.o ./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_depthwise_kernel3x3_stride1_inplace_CHW.su ./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_depthwise_kernel3x3_stride2_inplace_CHW.d ./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_depthwise_kernel3x3_stride2_inplace_CHW.o ./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_depthwise_kernel3x3_stride2_inplace_CHW.su ./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_kbuf_convolve_s8_kernel3_inputch3_stride2.d ./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_kbuf_convolve_s8_kernel3_inputch3_stride2.o ./Core/TinyEngine/src/kernels/int_forward_op/patchpadding_kbuf_convolve_s8_kernel3_inputch3_stride2.su ./Core/TinyEngine/src/kernels/int_forward_op/stable_softmax.d ./Core/TinyEngine/src/kernels/int_forward_op/stable_softmax.o ./Core/TinyEngine/src/kernels/int_forward_op/stable_softmax.su ./Core/TinyEngine/src/kernels/int_forward_op/upsample_byte.d ./Core/TinyEngine/src/kernels/int_forward_op/upsample_byte.o ./Core/TinyEngine/src/kernels/int_forward_op/upsample_byte.su

.PHONY: clean-Core-2f-TinyEngine-2f-src-2f-kernels-2f-int_forward_op

