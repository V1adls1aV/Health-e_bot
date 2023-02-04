import tensorflow as tf
import numpy as np
from PIL import Image
from data.config import MODELPATH


class TextModel:
    def __init__(self, filename='text_model.h5'):
        self.model: tf.keras.Model = tf.keras.models.load_model(
            MODELPATH + filename
        )

    def predict(self, image: Image) -> float:
        image = image.resize((256, 256))
        image = np.array([np.array(image) / 255.0])
        return float(self.model.predict(image))

