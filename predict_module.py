from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2
import tensorflow as tf

# Load the model
model = load_model('MobileNetV2_Normal_fine_tune_1018.h5')
# model = load_model('val_loss0.00038_TeachableMachine224x224_Square_White.h5')

def Is_Particular_Gesture( img ):
    class_names = [0, 1]
    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # Replace this with the path to your image
    image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #image = img.convert('RGB')
    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    #image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image = cv2.resize( image, size,fx=0,fy=0, interpolation = cv2.INTER_CUBIC )

    #turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(x=tf.data.Dataset.from_tensors(data))
    #prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    print("Class: ", class_name)
    print("Confidence Score: ", confidence_score)
    return class_name
