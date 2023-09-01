import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import argparse

def load_tflite_model(tflite_model_path):
    interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return interpreter, input_details, output_details

def keras_model():
    model = keras.Sequential(
        [
            layers.Dense(2, activation="relu", name="layer1"),
            layers.Dense(3, activation="relu", name="layer2"),
            layers.Dense(4, name="layer3"),
        ]
    )
    # Call model on a test input
    x = tf.ones((3, 3))
    y = model(x)
    return model
    
def quantize_model(input_model_path, output_model_path):
    model = keras_model()
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.experimental_new_converter = True
    # Post training quantization
    converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_SIZE]

    def representative_dataset_generator():
        for _ in range(100):  # Generate 100 fake samples
            fake_input_data = np.random.normal(size=(1,3)).astype(np.float32)
            yield [fake_input_data]

    # Prepare and save representative data
    representative_data = np.array(list(representative_dataset_generator()))
    quantized_data = np.round(0.02496907487511635 * (representative_data - 122)).astype(np.uint8)
    quantized_data = np.reshape(quantized_data, (100, 1, 3))
    quantized_data = quantized_data[9]
    # print(quantized_data.shape)
    # import sys; sys.exit(0)
    np.savez("/home/matthias/Desktop/model_quant_test.npz", input_tensors=quantized_data)
            
    converter.representative_dataset = representative_dataset_generator
    # Ensure that if any ops can't be quantized, the converter throws an error
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    # Set the input and output tensors to uint8 (APIs added in r2.3)
    converter.inference_input_type = tf.uint8
    converter.inference_output_type = tf.uint8

    tflite_quant_model = converter.convert()

    # Save the quantized model to a file
    with open(output_model_path, 'wb') as f:
        f.write(tflite_quant_model)


def cut_model(original_model, model_save_path):
    # Load the original TFLite model from memory
    with open(original_model, 'rb') as f:
        tflite_model_content = f.read()

    # Load the TFLite model from the content
    interpreter = tf.lite.Interpreter(model_content=tflite_model_content)
    interpreter.allocate_tensors()

    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Extract the first 2 layers of the model
    new_model_content = bytearray()
    for i, op in enumerate(interpreter._get_directly_invoked_ops()):
        if i <= 1:  # Only keep the first 2 layers
            new_model_content += op.node.name.encode('utf-8') + b'\x00'
            new_model_content += op.custom_options_bytes()

    # Save the new model content to a file
    with open(model_save_path, 'wb') as f:
        f.write(new_model_content)

    print("New model saved.")


def run_inference(interpreter, input_details, output_details, input_tensor):
    interpreter.set_tensor(input_details[0]['index'], input_tensor)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data

def main(npz_path, tflite_model_path):
    # Load the NumPy .npz array
    data = np.load(npz_path)
    input_tensor = data['input_tensors'][-1]
    input_tensor = input_tensor.reshape((1, *input_tensor.shape))

    # Load the TFLite model
    interpreter, input_details, output_details = load_tflite_model(tflite_model_path)

    # Run inference
    output_result = run_inference(interpreter, input_details, output_details, input_tensor)

    print("Inference Result:")
    # print(output_result)
    for float in output_result[0]:
        print("{:.2f}".format(float))

def reshape_data(data_path, target_shape):
    data = np.load(data_path)['input_tensors']
    print(data.shape)
    data = data.reshape(target_shape)
    np.savez(data_path, input_tensors=data)
    return

if __name__ == "__main__":

    input_model_path = "/home/matthias/Documents/BA/no_git_layer_benchmark/glow/glow/tests/models/tfliteModels/relu.tflite"
    output_model_path = "/home/matthias/Desktop/model_quant_test_cut.tflite"

    cut_model(input_model_path, output_model_path)
    #quantize_model(input_model_path, output_model_path)
    #print("Quantization complete. Quantized model saved at", output_model_path)
    import sys;sys.exit()

    parser = argparse.ArgumentParser(description="Run inference on a TFLite model using a NumPy .npz array.")
    parser.add_argument("npz_path", type=str, help="Path to the NumPy .npz array file.")
    parser.add_argument("tflite_model_path", type=str, help="Path to the TFLite model file.")
    args = parser.parse_args()

    # rep_data = np.load(args.npz_path + '/representative_dataset_fp32.npz')['input_tensors']
    # fp_data = np.load(args.npz_path + '/float32.npz')['input_tensors']
    # int_data = np.load(args.npz_path + '/int8.npz')['input_tensors']
    # target_shape = (fp_data.shape[0], *rep_data.shape[1:])
    
    # print("Representative shape: ", rep_data.shape)
    # print("Actual fp shape: ", fp_data.shape)
    # print("Actual int shape: ", int_data.shape)
    # print("target_shape: ", target_shape)
    # print()
    # #import sys; sys.exit(0)
    
    # reshape_data(args.npz_path + '/float32.npz', target_shape)
    # reshape_data(args.npz_path + '/int8.npz', target_shape)
    
    # fp_data = np.load(args.npz_path + '/float32.npz')['input_tensors']
    # int_data = np.load(args.npz_path + '/int8.npz')['input_tensors']
    # print()
    # print("Actual fp shape now: ", fp_data.shape)
    # print("Actual int shape now: ", int_data.shape)

    data = np.load(args.npz_path)['input_tensors']
    print(data.shape)
    print(data.dtype)

    main(args.npz_path, args.tflite_model_path)
