import tensorflow as tf
import numpy as np
from data.config import MODELPATH


class Model:
    def __init__(self, filename: str):
        self.model: tf.keras.Model = tf.keras.models.load_model(
            MODELPATH + filename,
            custom_objects={
                'custom_loss': self.custom_loss
                }
        )

    def custom_loss(y_true, y_pred):
        return tf.abs(y_true - y_pred)
        