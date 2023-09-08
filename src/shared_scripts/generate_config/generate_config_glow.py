import json

config = {
    "arguments": {
        "-model": "/home/matthias/Documents/BA/results/models_and_data/anomaly_detection/trained_models/ad01_int8.tflite",
        "-input_tensors": "/home/matthias/Documents/BA/results/models_and_data/anomaly_detection/bin_data/int8.npz",
        "-representative_tensors": "/home/matthias/Documents/BA/results/models_and_data/anomaly_detection/bin_data/representative_dataset_fp32.npz",
        "-workdir": "/home/matthias/Documents/BA/layer-benchmark-2/src/glow/workdir",
        "-glow_compiler": "/opt/nxp/Glow/bin/model-compiler",
        "-glow_profiler": "/opt/nxp/Glow/bin/model-profiler",
        "-cube_template": "/home/matthias/Documents/BA/layer-benchmark-2/src/glow/cube_templates/Glow_Template/",
        "-cube_template_ref": "/home/matthias/Documents/BA/layer-benchmark-2/src/glow/cube_templates/Glow_Template_ref/",
        "-cube_template_empty": "/home/matthias/Documents/BA/layer-benchmark-2/src/glow/cube_templates/Glow_Template_empty/",
        "-out_dir": "/home/matthias/Documents/BA/results/glow/usecases/test",
        "-repetitions": "1"
    },
    "parameters": [
        "-nxp"
    ]
}

with open("glow_ad_quant.json", "w") as config_file:
    json.dump(config, config_file, indent=4)

print("Configuration file 'glow_config.json' generated.")
