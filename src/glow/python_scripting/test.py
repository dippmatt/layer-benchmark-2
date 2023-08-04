import numpy as np
import tensorflow as tf
import argparse

def load_tflite_model(tflite_model_path):
    interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return interpreter, input_details, output_details

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