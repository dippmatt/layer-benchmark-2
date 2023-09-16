import json

config = {
    "arguments": {
        "-model": "/home/matthias/Documents/BA/results/models_and_data/visual_wake_words/trained_models/vww_96_int8_no_softmax.tflite",
        "-input_tensors": "/home/matthias/Documents/BA/results/models_and_data/visual_wake_words/bin_data/person/float32.npz",
        "-workdir": "/home/matthias/Documents/BA/layer-benchmark-2/src/st/workdir",
        "-cube_template": "/home/matthias/Documents/BA/layer-benchmark-2/src/st/cube_templates/template_cube_ai_8_1_balanced",
        "-cube_template_ref": "/home/matthias/Documents/BA/layer-benchmark-2/src/st/cube_templates/EvalAIModel2_ref",
        "-cube_template_empty": "/home/matthias/Documents/BA/layer-benchmark-2/src/st/cube_templates/EvalAIModel2_empty",
        "-out_dir": "/home/matthias/Documents/BA/results/glow/usecases/test",
        "-repetitions": "1"
    },
    "parameters": [

    ]
}

fname = "st_vww_quant.json"
with open(fname, "w") as config_file:
    json.dump(config, config_file, indent=4)

print(f"Configuration file '{fname}' generated.")
