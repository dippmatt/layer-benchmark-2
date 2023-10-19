# layer-benchmark-2
Automatically compare machine learning inference on cortex M4 microcontroller on a per-layer basis

### Structure

- src:

Source code for python automation to run frameworks
Note: ST's Cube MX AI, tiny engine & glow frameworks are fully automated, while tflite micro framework (also based on Cube MX projects) is not supported in an automated fashion.

- test_data

Contains test vectors / tensors for each use case (anomaly detection, image classification, keyword spotting, visual wake words)
The test data aims to provide data for two purposes:
 - Data to run inference on. At least one sample per class is provided.
 - Representative data: Some frameworks perform post training quantisation on their own, using float32 data as input to quantize the model (e.g. glow).
 For that purpose more data samples are needed to calibrate quantisation data (offset, scaling). 
 These datasets are equal to the calibration datasets used to quantize the tflite models in mlperf tiny, for each use case respectivly.
 ~100 to ~1000 samples (depending on the use case) are used in mlperf tiny to calibrate the quantised tflite models. Those are found in <test_data> directory as well.
 
- third_party

Contains third party repositories (e.g. tiny_engine repo), needed to compile tflite models into C.

### How to run

1) Create a python environment for each framework (st, tiny_engine, glow)

`cd src/<framework>`
`python3 -m venv venv`
`source venv/bin/activate`
`pyhton3 -m pip install -r requirements.txt`


2) Then we run the frameworks
#TODO
