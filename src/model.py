import numpy as np


class ProjectModel:
    def __init__(self, model):
        self.model = model
        self.X_acc = None
        self.y_acc = None
        self.iter = 0

    def fit(self, X, y):
        self.iter += 1
        if self.X_acc is None:
            self.X_acc = X
            self.y_acc = y
        else:
            self.X_acc = np.concatenate([self.X_acc, X])
            self.y_acc = np.concatenate([self.y_acc, y])
        self.model.fit(self.X_acc, self.y_acc)

    def predict(self, X):
        return self.model.predict(X)
    
    def score(self):
        if self.X_acc is None:
            return None
        return self.model.score(self.X_acc, self.y_acc)
    
    def is_fit(self):
        return not (self.X_acc is None)
    
    def get_iter(self):
        return self.iter
