/* Automatically generated source file */
#include <float.h>
#include "arm_nnfunctions.h"

#include "genNN.h"
#include "genModel.h"

#include "tinyengine_function.h"
#include "tinyengine_function_fp.h"

#include "profiling.h"


/* Variables used by all ops */
ADD_params add_params;
//Conv_Params conv_params;
//Depthwise_Params dpconv_params;
int i;
int8_t *int8ptr,*int8ptr2;
int32_t *int32ptr;
float *fptr,*fptr2,*fptr3;

signed char* getInput() {
    return &buffer0[0];
}
signed char* getOutput() {
    return NNoutput;
}
void end2endinference(q7_t* img){
    invoke(NULL);
}
void invoke(float* labels){
/* layer 0:CONV_2D */
convolve_1x1_s8(&buffer0[0],1,1,640,(const q7_t*) weight0,bias0,shift0,multiplier0,-128,-89,-128,127,&buffer0[640],1,1,128,sbuf);
/* layer 1:CONV_2D */
convolve_1x1_s8(&buffer0[640],1,1,128,(const q7_t*) weight1,bias1,shift1,multiplier1,-128,128,-128,127,&buffer0[0],1,1,128,sbuf);
/* layer 2:CONV_2D */
convolve_1x1_s8(&buffer0[0],1,1,128,(const q7_t*) weight2,bias2,shift2,multiplier2,-128,128,-128,127,&buffer0[128],1,1,128,sbuf);
/* layer 3:CONV_2D */
convolve_1x1_s8(&buffer0[128],1,1,128,(const q7_t*) weight3,bias3,shift3,multiplier3,-128,128,-128,127,&buffer0[0],1,1,128,sbuf);
/* layer 4:CONV_2D */
convolve_1x1_s8(&buffer0[0],1,1,128,(const q7_t*) weight4,bias4,shift4,multiplier4,-128,128,-128,127,&buffer0[128],1,1,8,sbuf);
/* layer 5:CONV_2D */
convolve_1x1_s8_ch8(&buffer0[128],1,1,8,(const q7_t*) weight5,bias5,shift5,multiplier5,-128,128,-128,127,&buffer0[0],1,1,128,sbuf);
/* layer 6:CONV_2D */
convolve_1x1_s8(&buffer0[0],1,1,128,(const q7_t*) weight6,bias6,shift6,multiplier6,-128,128,-128,127,&buffer0[128],1,1,128,sbuf);
/* layer 7:CONV_2D */
convolve_1x1_s8(&buffer0[128],1,1,128,(const q7_t*) weight7,bias7,shift7,multiplier7,-128,128,-128,127,&buffer0[0],1,1,128,sbuf);
/* layer 8:CONV_2D */
convolve_1x1_s8(&buffer0[0],1,1,128,(const q7_t*) weight8,bias8,shift8,multiplier8,-128,128,-128,127,&buffer0[640],1,1,128,sbuf);
/* layer 9:CONV_2D */
convolve_1x1_s8(&buffer0[640],1,1,128,(const q7_t*) weight9,bias9,shift9,multiplier9,96,128,-128,127,&buffer0[0],1,1,640,sbuf);
}
void invoke_inf(){
/* layer 0:CONV_2D */
//PROFILING_EVENT("Event 1");
convolve_1x1_s8(&buffer0[0],1,1,640,(const q7_t*) weight0,bias0,shift0,multiplier0,-128,-89,-128,127,&buffer0[640],1,1,128,sbuf);
/* layer 1:CONV_2D */
//PROFILING_EVENT("Event 2");
convolve_1x1_s8(&buffer0[640],1,1,128,(const q7_t*) weight1,bias1,shift1,multiplier1,-128,128,-128,127,&buffer0[0],1,1,128,sbuf);
/* layer 2:CONV_2D */
//PROFILING_EVENT("Event 3");
convolve_1x1_s8(&buffer0[0],1,1,128,(const q7_t*) weight2,bias2,shift2,multiplier2,-128,128,-128,127,&buffer0[128],1,1,128,sbuf);
/* layer 3:CONV_2D */
//PROFILING_EVENT("Event 4");
convolve_1x1_s8(&buffer0[128],1,1,128,(const q7_t*) weight3,bias3,shift3,multiplier3,-128,128,-128,127,&buffer0[0],1,1,128,sbuf);
/* layer 4:CONV_2D */
//PROFILING_EVENT("Event 5");
convolve_1x1_s8(&buffer0[0],1,1,128,(const q7_t*) weight4,bias4,shift4,multiplier4,-128,128,-128,127,&buffer0[128],1,1,8,sbuf);
/* layer 5:CONV_2D */
//PROFILING_EVENT("Event 6");
convolve_1x1_s8_ch8(&buffer0[128],1,1,8,(const q7_t*) weight5,bias5,shift5,multiplier5,-128,128,-128,127,&buffer0[0],1,1,128,sbuf);
/* layer 6:CONV_2D */
//PROFILING_EVENT("Event 7");
convolve_1x1_s8(&buffer0[0],1,1,128,(const q7_t*) weight6,bias6,shift6,multiplier6,-128,128,-128,127,&buffer0[128],1,1,128,sbuf);
/* layer 7:CONV_2D */
//PROFILING_EVENT("Event 8");
//convolve_1x1_s8(&buffer0[128],1,1,128,(const q7_t*) weight7,bias7,shift7,multiplier7,-128,128,-128,127,&buffer0[0],1,1,128,sbuf);
/* layer 8:CONV_2D */
//PROFILING_EVENT("Event 9");
convolve_1x1_s8(&buffer0[0],1,1,128,(const q7_t*) weight8,bias8,shift8,multiplier8,-128,128,-128,127,&buffer0[640],1,1,128,sbuf);
/* layer 9:CONV_2D */
//PROFILING_EVENT("Event 10");
convolve_1x1_s8(&buffer0[640],1,1,128,(const q7_t*) weight9,bias9,shift9,multiplier9,96,128,-128,127,&buffer0[0],1,1,640,sbuf);
//PROFILING_EVENT("Event 11");
}
