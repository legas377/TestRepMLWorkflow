import numpy as np


class DataLoader:
    def __init__(self, NUM_FEATURES=10):
        np.random.seed(42)
        self.NUM_FEATURES = NUM_FEATURES
        self.weights = np.random.rand(NUM_FEATURES)

    def get_data(self, batch_size=100):
        # Генерация случайных данных
        X = np.random.rand(batch_size, self.NUM_FEATURES) * 10
        y = np.dot(X, self.weights) + np.random.randn(batch_size) * 2
        return X, y
    
    def get_weights(self):
        return self.weights
