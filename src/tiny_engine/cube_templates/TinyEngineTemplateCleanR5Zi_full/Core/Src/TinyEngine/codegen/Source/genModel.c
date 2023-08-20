/* Automatically generated source file */
#include <float.h>
#include <tinyengine_function.h>
#include <tinyengine_function_fp.h>

#include "genNN.h"
#include "genModel.h"
#include "genInclude.h"

/* Variables used by all ops */
ADD_params add_params;
int i;
int8_t *int8ptr,*int8ptr2;
int32_t *int32ptr;
float *fptr,*fptr2,*fptr3;

signed char* getInput() {
    return &buffer0[16384];
}
signed char* getOutput() {
    return NNoutput;
}
void end2endinference(q7_t* img){
    invoke(NULL);
}
void invoke(float* labels){
/* layer 0:CONV_2D */
convolve_s8_kernel3_stride1_pad1(&buffer0[16384],32,32,3,(const q7_t*) weight0,bias0,shift0,multiplier0,-128,128,-128,127,&buffer0[0],32,32,16,sbuf,-128);
/* layer 1:CONV_2D */
convolve_s8_kernel3_stride1_pad1(&buffer0[0],32,32,16,(const q7_t*) weight1,bias1,shift1,multiplier1,-128,128,-128,127,&buffer0[16384],32,32,16,sbuf,-128);
/* layer 2:CONV_2D */
convolve_s8_kernel3_stride1_pad1(&buffer0[16384],32,32,16,(const q7_t*) weight2,bias2,shift2,multiplier2,4,128,-128,127,&buffer0[32768],32,32,16,sbuf,-128);
/* layer 3:ADD */
add_fpreq(16384, &buffer0[0],0.039393551647663116,-128,&buffer0[32768],0.10419496148824692,4,0.050945673137903214,-128,&buffer0[16384]);
/* layer 4:CONV_2D */
convolve_s8_kernel3_inputch3_stride2_pad1(&buffer0[16384],32,32,16,(const q7_t*) weight3,bias3,shift3,multiplier3,-128,128,-128,127,&buffer0[0],16,16,32,sbuf,kbuf,-128);
/* layer 5:CONV_2D */
convolve_s8_kernel3_stride1_pad1(&buffer0[0],16,16,32,(const q7_t*) weight4,bias4,shift4,multiplier4,4,128,-128,127,&buffer0[8192],16,16,32,sbuf,-128);
/* layer 6:CONV_2D */
convolve_1x1_s8_ch16(&buffer0[16384],32,32,16,(const q7_t*) weight5,bias5,shift5,multiplier5,-17,128,-128,127,&buffer0[0],16,16,32,sbuf);
/* layer 7:ADD */
add_fpreq(8192, &buffer0[0],0.044761426746845245,-17,&buffer0[8192],0.11311884224414825,4,0.0532362163066864,-128,&buffer0[16384]);
/* layer 8:CONV_2D */
convolve_s8_kernel3_inputch3_stride2_pad1(&buffer0[16384],16,16,32,(const q7_t*) weight6,bias6,shift6,multiplier6,-128,128,-128,127,&buffer0[0],8,8,64,sbuf,kbuf,-128);
/* layer 9:CONV_2D */
convolve_s8_kernel3_stride1_pad1(&buffer0[0],8,8,64,(const q7_t*) weight7,bias7,shift7,multiplier7,-2,128,-128,127,&buffer0[4096],8,8,64,sbuf,-128);
/* layer 10:CONV_2D */
convolve_1x1_s8(&buffer0[16384],16,16,32,(const q7_t*) weight8,bias8,shift8,multiplier8,38,128,-128,127,&buffer0[0],8,8,64,sbuf);
/* layer 11:ADD */
add_fpreq(4096, &buffer0[0],0.08385830372571945,38,&buffer0[4096],0.21724364161491394,-2,0.1270691454410553,-128,&buffer0[8192]);
/* layer 12:AVERAGE_POOL_2D */
avg_pooling(&buffer0[8192],8,8,64,8,8,1,1,-128,127,&buffer0[0]);
/* layer 13:CONV_2D */
convolve_1x1_s8(&buffer0[64],1,1,64,(const q7_t*) weight9,bias9,shift9,multiplier9,24,128,-128,127,&buffer0[64],1,1,10,sbuf);
}
void invoke_inf(){
/* layer 0:CONV_2D */
convolve_s8_kernel3_stride1_pad1(&buffer0[16384],32,32,3,(const q7_t*) weight0,bias0,shift0,multiplier0,-128,128,-128,127,&buffer0[0],32,32,16,sbuf,-128);
/* layer 1:CONV_2D */
convolve_s8_kernel3_stride1_pad1(&buffer0[0],32,32,16,(const q7_t*) weight1,bias1,shift1,multiplier1,-128,128,-128,127,&buffer0[16384],32,32,16,sbuf,-128);
/* layer 2:CONV_2D */
convolve_s8_kernel3_stride1_pad1(&buffer0[16384],32,32,16,(const q7_t*) weight2,bias2,shift2,multiplier2,4,128,-128,127,&buffer0[32768],32,32,16,sbuf,-128);
/* layer 3:ADD */
add_fpreq(16384, &buffer0[0],0.039393551647663116,-128,&buffer0[32768],0.10419496148824692,4,0.050945673137903214,-128,&buffer0[16384]);
/* layer 4:CONV_2D */
convolve_s8_kernel3_inputch3_stride2_pad1(&buffer0[16384],32,32,16,(const q7_t*) weight3,bias3,shift3,multiplier3,-128,128,-128,127,&buffer0[0],16,16,32,sbuf,kbuf,-128);
/* layer 5:CONV_2D */
convolve_s8_kernel3_stride1_pad1(&buffer0[0],16,16,32,(const q7_t*) weight4,bias4,shift4,multiplier4,4,128,-128,127,&buffer0[8192],16,16,32,sbuf,-128);
/* layer 6:CONV_2D */
convolve_1x1_s8_ch16(&buffer0[16384],32,32,16,(const q7_t*) weight5,bias5,shift5,multiplier5,-17,128,-128,127,&buffer0[0],16,16,32,sbuf);
/* layer 7:ADD */
add_fpreq(8192, &buffer0[0],0.044761426746845245,-17,&buffer0[8192],0.11311884224414825,4,0.0532362163066864,-128,&buffer0[16384]);
/* layer 8:CONV_2D */
convolve_s8_kernel3_inputch3_stride2_pad1(&buffer0[16384],16,16,32,(const q7_t*) weight6,bias6,shift6,multiplier6,-128,128,-128,127,&buffer0[0],8,8,64,sbuf,kbuf,-128);
/* layer 9:CONV_2D */
convolve_s8_kernel3_stride1_pad1(&buffer0[0],8,8,64,(const q7_t*) weight7,bias7,shift7,multiplier7,-2,128,-128,127,&buffer0[4096],8,8,64,sbuf,-128);
/* layer 10:CONV_2D */
convolve_1x1_s8(&buffer0[16384],16,16,32,(const q7_t*) weight8,bias8,shift8,multiplier8,38,128,-128,127,&buffer0[0],8,8,64,sbuf);
/* layer 11:ADD */
add_fpreq(4096, &buffer0[0],0.08385830372571945,38,&buffer0[4096],0.21724364161491394,-2,0.1270691454410553,-128,&buffer0[8192]);
/* layer 12:AVERAGE_POOL_2D */
avg_pooling(&buffer0[8192],8,8,64,8,8,1,1,-128,127,&buffer0[0]);
/* layer 13:CONV_2D */
convolve_1x1_s8(&buffer0[64],1,1,64,(const q7_t*) weight9,bias9,shift9,multiplier9,24,128,-128,127,&buffer0[64],1,1,10,sbuf);
}
