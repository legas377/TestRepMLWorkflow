import pickle
import os


def save_object(obj, filepath):
    """Сохраняет объект в файл через pickle."""
    with open(filepath, "wb") as f:
        pickle.dump(obj, f)


def load_object(filepath):
    """Загружает объект из файла через pickle."""
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            return pickle.load(f)
    return None
