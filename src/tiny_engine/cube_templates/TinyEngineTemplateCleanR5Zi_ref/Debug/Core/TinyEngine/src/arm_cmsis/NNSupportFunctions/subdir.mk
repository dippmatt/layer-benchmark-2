################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_accumulate_q7_to_q15.c \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_add_q7.c \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_depthwise_conv_nt_t_padded_s8.c \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_depthwise_conv_nt_t_s8.c \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_core_1x_s8.c \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_core_4x_s8.c \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_kernel_s16.c \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mult_nt_t_s8.c \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mult_q15.c \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mult_q7.c \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_s16.c \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_s8.c \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_svdf_s8.c \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nntables.c \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_no_shift.c \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_reordered_no_shift.c \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_reordered_with_offset.c \
../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_with_offset.c 

OBJS += \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_accumulate_q7_to_q15.o \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_add_q7.o \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_depthwise_conv_nt_t_padded_s8.o \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_depthwise_conv_nt_t_s8.o \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_core_1x_s8.o \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_core_4x_s8.o \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_kernel_s16.o \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mult_nt_t_s8.o \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mult_q15.o \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mult_q7.o \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_s16.o \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_s8.o \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_svdf_s8.o \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nntables.o \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_no_shift.o \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_reordered_no_shift.o \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_reordered_with_offset.o \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_with_offset.o 

C_DEPS += \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_accumulate_q7_to_q15.d \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_add_q7.d \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_depthwise_conv_nt_t_padded_s8.d \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_depthwise_conv_nt_t_s8.d \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_core_1x_s8.d \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_core_4x_s8.d \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_kernel_s16.d \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mult_nt_t_s8.d \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mult_q15.d \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mult_q7.d \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_s16.d \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_s8.d \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_svdf_s8.d \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nntables.d \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_no_shift.d \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_reordered_no_shift.d \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_reordered_with_offset.d \
./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_with_offset.d 


# Each subdirectory must supply rules for building sources it contributes
Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/%.o Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/%.su: ../Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/%.c Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32L4R5xx -c -I../Core/Inc -I../Core/Src/TinyEngine/include/arm_cmsis -I../Core/Src/TinyEngine/include -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-NNSupportFunctions

clean-Core-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-NNSupportFunctions:
	-$(RM) ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_accumulate_q7_to_q15.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_accumulate_q7_to_q15.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_accumulate_q7_to_q15.su ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_add_q7.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_add_q7.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_add_q7.su ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_depthwise_conv_nt_t_padded_s8.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_depthwise_conv_nt_t_padded_s8.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_depthwise_conv_nt_t_padded_s8.su ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_depthwise_conv_nt_t_s8.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_depthwise_conv_nt_t_s8.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_depthwise_conv_nt_t_s8.su ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_core_1x_s8.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_core_1x_s8.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_core_1x_s8.su ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_core_4x_s8.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_core_4x_s8.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_core_4x_s8.su ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_kernel_s16.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_kernel_s16.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mul_kernel_s16.su ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mult_nt_t_s8.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mult_nt_t_s8.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mat_mult_nt_t_s8.su ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mult_q15.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mult_q15.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mult_q15.su ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mult_q7.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mult_q7.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_mult_q7.su ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_s16.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_s16.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_s16.su ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_s8.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_s8.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_s8.su ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_svdf_s8.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_svdf_s8.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nn_vec_mat_mult_t_svdf_s8.su ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nntables.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nntables.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_nntables.su ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_no_shift.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_no_shift.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_no_shift.su ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_reordered_no_shift.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_reordered_no_shift.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_reordered_no_shift.su ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_reordered_with_offset.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_reordered_with_offset.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_reordered_with_offset.su ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_with_offset.d ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_with_offset.o ./Core/TinyEngine/src/arm_cmsis/NNSupportFunctions/arm_q7_to_q15_with_offset.su

.PHONY: clean-Core-2f-TinyEngine-2f-src-2f-arm_cmsis-2f-NNSupportFunctions

