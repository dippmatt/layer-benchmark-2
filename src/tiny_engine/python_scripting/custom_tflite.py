# ----------------------------------------------------------------------
# Project: TinyEngine
# Title:   vww_patchbased.py
#
# Reference papers:
#  - MCUNet: Tiny Deep Learning on IoT Device, NeurIPS 2020
#  - MCUNetV2: Memory-Efficient Patch-based Inference for Tiny Deep Learning, NeurIPS 2021
#  - MCUNetV3: On-Device Training Under 256KB Memory, NeurIPS 2022
# Contact authors:
#  - Wei-Ming Chen, wmchen@mit.edu
#  - Wei-Chen Wang, wweichen@mit.edu
#  - Ji Lin, jilin@mit.edu
#  - Ligeng Zhu, ligeng@mit.edu
#  - Song Han, songhan@mit.edu
#
# Target ISA:  ARMv7E-M
# ----------------------------------------------------------------------

import os
from tempfile import TemporaryDirectory
import argparse

from code_generator.CodeGenerator import CodeGenerator
from code_generator.GeneralMemoryScheduler import GeneralMemoryScheduler
from code_generator.InputResizer import PatchResizer
from code_generator.PatchBasedUtil import getPatchParams
from code_generator.TfliteConvertor import TfliteConvertor

parser = argparse.ArgumentParser()
parser.add_argument("tflite", help="Quantized tflite model file", type=str)
args = parser.parse_args()

# 1: Let's first build our pretrained VWW model
# 2: To deploy the model on MCU, we need to first convert the model to an Intermediate Representation (IR) and
# get the weight parameters and scale parameters.
#tflite_path = "/home/matthias/Documents/BA/results/models_and_data/anomaly_detection/trained_models"
#tflite_path = "/home/matthias/Documents/BA/mlperf_tiny_fresh/tiny/benchmark/training/image_classification/trained_models/pretrainedResnet_no_softmax_quant.tflite"
# unknown 'not implemented error?!'
#tflite_path = "/home/matthias/Documents/BA/mlperf_tiny_fresh/tiny/benchmark/training/keyword_spotting/trained_models/kws_ref_model_no_softmax.tflite"
tflite_path = args.tflite
life_cycle_path = "./lifecycle.png"
# 3. Set up patchbased parameters
use_inplace = True
n_patches = None  # 2x2 patches
split_index = 5  # split at the fifth conv later
# 4. Let's generate source code for on-device deployment

with TemporaryDirectory() as WORKING_DIR:
    if life_cycle_path is None:
        schedule_image_path = os.path.join(WORKING_DIR, "schedule.png")
    else:
        schedule_image_path = life_cycle_path

    tf_convertor = TfliteConvertor(tflite_path)
    tf_convertor.parseOperatorInfo()
    layer = tf_convertor.layer
    outTable = []
    VisaulizeTrainable = False  # disable for code gen
    # Patch-based
    if n_patches is not None:
        patch_params = getPatchParams(layer, split_index, n_patches)
        P_resizer = PatchResizer(layer)
        P_resizer.patchResize(patch_params["layer_cnt"], patch_params["grain_rf"], patch_params["grain_rf_height"])

    memory_scheduler = GeneralMemoryScheduler(
        layer,
        False,
        False,
        outputTables=outTable,
        inplace=use_inplace,
        mem_visual_path=schedule_image_path,
        VisaulizeTrainable=VisaulizeTrainable,
    )
    memory_scheduler.USE_INPLACE = use_inplace
    memory_scheduler.allocateMemory()
    memory_scheduler.dumpLayerMem()

    outTable = tf_convertor.outputTables if hasattr(tf_convertor, "outputTables") else []  # type: ignore
    code_generator = CodeGenerator(
        memsche=memory_scheduler,
        inplace=memory_scheduler.USE_INPLACE,
        unsigned_input=False,
        patch_params=None,
        FP_output=False,
        profile_mode=False,
        fp_requantize=False,
        tflite_op=False,
        dummy_address=False,
        outputTables=outTable,
    )
    # set detection outputs before codegen if any
    code_generator.codeGeneration()

    peakmem = memory_scheduler.buffers["input_output"]


print(f"Peak memory: {peakmem} bytes")
