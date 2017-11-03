import os
import numpy as np

x_path = None
y_path = None


def load_training_data(x_path,y_path,genre):
    X_data = []
    Y_data = []
    names = []
    print('[*] Loading data...')

    x_path = os.path.join(x_path, genre)
    y_path = os.path.join(y_path, genre)

    for i, filename in enumerate(os.listdir(x_path)):
        #TAKE ONLY NPY FILENAMES NOT THE MIDI FILES
        if filename.split('.')[-1] == 'npy':
            names.append(filename)

    for i, filename in enumerate(names):
        abs_x_path = os.path.join(x_path,filename)
        abs_y_path = os.path.join(y_path,filename)
        loaded_x = np.load(abs_x_path)

        X_data.append(loaded_x)

        loaded_y = np.load(abs_y_path)
        loaded_y = loaded_y/127
        Y_data.append(loaded_y)
        assert X_data[i].shape[0] == Y_data[i].shape[0]


    return X_data, Y_data



def load_data():
    data = {}
    data["classical"] = {}
    data["jazz"] = {}


    c_train_X , c_train_Y = load_training_data(x_path, y_path, "classical")

    data["classical"]["X"] = c_train_X
    data["classical"]["Y"] = c_train_Y

    j_train_X , j_train_Y = load_training_data(x_path, y_path, "jazz")

    data["jazz"]["X"] = j_train_X
    data["jazz"]["Y"] = j_train_Y

    return data