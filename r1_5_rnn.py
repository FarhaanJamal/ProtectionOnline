import numpy as np
import tensorflow as tf
import r1_4_rnn_model

def rnn_model(url):
    # Load the pre-trained model from the HDF5 file
    model = tf.keras.models.load_model('model/MODEL_1.h5', compile=False)  # Replace 'your_model.h5' with the path to your HDF5 file
    A = r1_4_rnn_model.extract_info(url)
    # Prepare input data (example)
    # Assuming your input data is a list of lists or a NumPy array


    # Prepare input data for a single sample
    input_data = np.array([A])  # Shape should be (1, input_shape), replace '...' with your actual input values
    print(A)

    # Make predictions
    predictions = model.predict(input_data)
    res = ""
    if predictions[0]==0:
        res = "Good"
    else:
        res = "Bad"
    return res
