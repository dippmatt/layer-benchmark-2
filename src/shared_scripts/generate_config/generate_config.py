import json

config = {
    "arguments": {
    	"-tiny_engine_submodule": "/home/matthias/Documents/BA/layer-benchmark-2/third_party/tinyengine",
        "-model": "/home/matthias/Documents/BA/results/models_and_data/anomaly_detection/trained_models/ad01_int8.tflite",
        "-input_tensors": "/home/matthias/Documents/BA/results/models_and_data/anomaly_detection/bin_data/int8.npz",
        "-workdir": "/home/matthias/Documents/BA/layer-benchmark-2/src/tiny_engine/workdir",
        "-cube_template": "/home/matthias/Documents/BA/layer-benchmark-2/src/tiny_engine/cube_templates/TinyEngineTemplateCleanR5Zi",
        "-cube_template_ref": "/home/matthias/Documents/BA/layer-benchmark-2/src/tiny_engine/cube_templates/TinyEngineTemplateCleanR5Zi_ref",
        "-cube_template_empty": "/home/matthias/Documents/BA/layer-benchmark-2/src/tiny_engine/cube_templates/TinyEngineTemplateCleanR5Zi_ref_empty",
        "-out_dir": "/home/matthias/Documents/BA/results/glow/usecases/test",
        "-repetitions": "1"
    },
    "parameters": [

    ]
}

fname = "tiny_engine_ad_quant.json"
with open(fname, "w") as config_file:
    json.dump(config, config_file, indent=4)

print(f"Configuration file '{fname}' generated.")
