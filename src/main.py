# Dependencies:
# tensorflow==2.10.0
# numpy==1.21.2
# matplotlib==3.4.3
# scikit-image==0.19.2

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, concatenate
from tensorflow.keras.optimizers import Adam
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize

# Function to create a U-Net model for medical image segmentation
def unet_model(input_size=(128, 128, 1)):
    inputs = Input(input_size)
    
    # Contracting path
    conv1 = Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
    conv1 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool1)
    conv2 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = Conv2D(256, (3, 3), activation='relu', padding='same')(pool2)
    conv3 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv3)
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

    # Bottleneck
    conv4 = Conv2D(512, (3, 3), activation='relu', padding='same')(pool3)
    conv4 = Conv2D(512, (3, 3), activation='relu', padding='same')(conv4)

    # Expanding path
    up5 = concatenate([UpSampling2D(size=(2, 2))(conv4), conv3], axis=3)
    conv5 = Conv2D(256, (3, 3), activation='relu', padding='same')(up5)
    conv5 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv5)

    up6 = concatenate([UpSampling2D(size=(2, 2))(conv5), conv2], axis=3)
    conv6 = Conv2D(128, (3, 3), activation='relu', padding='same')(up6)
    conv6 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv6)

    up7 = concatenate([UpSampling2D(size=(2, 2))(conv6), conv1], axis=3)
    conv7 = Conv2D(64, (3, 3), activation='relu', padding='same')(up7)
    conv7 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv7)

    outputs = Conv2D(1, (1, 1), activation='sigmoid')(conv7)

    model = Model(inputs=[inputs], outputs=[outputs])
    model.compile(optimizer=Adam(lr=1e-4), loss='binary_crossentropy', metrics=['accuracy'])
    
    return model

# Function to preprocess the images
def preprocess_images(images):
    processed_images = []
    for img in images:
        img = resize(img, (128, 128, 1), mode='constant', preserve_range=True)
        processed_images.append(img)
    return np.array(processed_images)

# Example usage
if __name__ == "__main__":
    # Load your dataset here
    # For demonstration, let's create dummy data
    images = np.random.rand(10, 256, 256, 1)  # Dummy image data
    masks = np.random.randint(0, 2, (10, 256, 256, 1))  # Dummy mask data

    # Preprocess the images and masks
    processed_images = preprocess_images(images)
    processed_masks = preprocess_images(masks)

    # Create and train the model
    model = unet_model()
    model.fit(processed_images, processed_masks, batch_size=2, epochs=10, validation_split=0.2)

    # Save the model
    model.save('medical_diagnosis_model.h5')

    # Load the model for inference
    loaded_model = tf.keras.models.load_model('medical_diagnosis_model.h5')

    # Perform inference on a new image
    new_image = np.random.rand(1, 256, 256, 1)  # Dummy new image data
    processed_new_image = preprocess_images(new_image)
    prediction = loaded_model.predict(processed_new_image)

    # Plot the results
    plt.imshow(prediction[0].reshape(128, 128), cmap='gray')
    plt.title('Predicted Mask')
    plt.show()