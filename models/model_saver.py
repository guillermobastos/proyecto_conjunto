import os
import pickle

def save_model(model, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as file:
        pickle.dump(model, file)
    print(f"Modelo guardado en {filepath}")
