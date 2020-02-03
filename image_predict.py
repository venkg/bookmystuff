#   Imports
import tensorflow as tf
import numpy as np
import argparse

# Paths to files producted as part of retraining Inception.  Change these if you saved your files in
#   a different location.
#   Retrained graph
MODEL_PATH = "./tmp/output_graph.pb"

#   Remove ugly characters from strings
def filter_delimiters(text):
    filtered = text[:-3]
    filtered = filtered.strip("b'")
    filtered = filtered.strip("\\r'")
    filtered = filtered.strip("'")
    return filtered

def predict_image_class(imagePath, labelPath):
    
    matches = None # Default return to none

    if not tf.gfile.Exists(imagePath):
        tf.logging.fatal('File does not exist %s', imagePath)
        return matches

    # Load the image from file
    image_data = tf.gfile.FastGFile(imagePath, 'rb').read()

    # Load the retrained inception based graph
    with tf.gfile.FastGFile(MODEL_PATH, 'rb') as f:
            # init GraphDef object
            graph_def = tf.GraphDef()
            # Read in the graphy from the file
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')
        # this point the retrained graph is the default graph

    with tf.Session() as sess:
        # These 2 lines are the code that does the classification of the images 
        # using the new classes we retrained Inception to recognize. 
        #   We find the final result tensor by name in the retrained model
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        #   Get the predictions on our image by add the image data to the tensor
        predictions = sess.run(softmax_tensor,
                            {'DecodeJpeg/contents:0': image_data})
        
        # Format predicted classes for display
        #   use np.squeeze to convert the tensor to a 1-d vector of probability values
        predictions = np.squeeze(predictions)

        top_k = predictions.argsort()[-5:][::-1]  # Getting the indicies of the top 5 predictions

        #   read the class labels in from the label file
        f = open(labelPath, 'rb')
        lines = f.readlines()
        labels = [str(w).replace("\n", "") for w in lines]
        print("")
        print ("Image Classification Probabilities")
        #   Output the class probabilites in descending order
        for node_id in top_k:
            human_string = filter_delimiters(labels[node_id])
            score = predictions[node_id]
            print('{0:s} (score = {1:.5f})'.format(human_string, score))

        print("")

        predicted_class_probability = predictions[top_k[0]]
        if(predicted_class_probability < 0.7):
            answer = "unknown"
        else:
            answer = filter_delimiters(labels[top_k[0]])
        return answer
