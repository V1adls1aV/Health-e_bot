import numpy as np
from PIL import Image

from tf_models.model import Model


class TextModel(Model):
    def __init__(self, filename='text_model.h5'):
        super().__init__(filename)

    def predict(self, image: Image) -> float:
        image = image.resize((256, 256))
        image = np.array([np.array(image) / 255.0])
        return float(self.model.predict(image))

