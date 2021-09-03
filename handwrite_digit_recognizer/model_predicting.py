from keras.models import load_model
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class Model:
    def __init__(self):
        self.model = load_model('saved_model.h5')

    def predict(self, matrix):
        new_case = matrix.reshape((-1, 28, 28, 1))
        return self.model.predict(new_case)[0]
