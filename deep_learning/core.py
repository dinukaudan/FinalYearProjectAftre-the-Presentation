# multi-class classification with Keras
import csv
from os import path
from pathlib import Path

import numpy
import pandas
from keras.engine.saving import load_model
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import np_utils
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder

# settings
use_big_sample = True

MODEL_SAVE_PATH = './deep_learning/models/saved_model.model'
ENCODER_SAVE_PATH = './deep_learning/models/saved_encoder.npy'
PREDICT_FILE_PATH = "./deep_learning/generated_csv/direct_raw_features.csv"
encoder = LabelEncoder()
model = Sequential()


def is_model_saved():
    return path.exists(MODEL_SAVE_PATH)


def save_encoder():
    numpy.save(ENCODER_SAVE_PATH, encoder.classes_)


def load_encoder():
    new_encoder = LabelEncoder()
    new_encoder.classes_ = numpy.load(ENCODER_SAVE_PATH, allow_pickle=True)
    return new_encoder


# define baseline model
def baseline_model():
    model.add(Dense(50, input_dim=11, activation='relu'))
    model.add(Dense(4, activation='softmax'))
    # Compile model105
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def train_data():
    # load dataset
    dataframe = pandas.read_csv("./deep_learning/generated_csv/direct_features.csv" if use_big_sample else "./deep_learning/csv/mini_sample.csv",
                                header=None)
    dataset = dataframe.values
    X = dataset[1:, 0:11].astype(float)
    Y = dataset[1:, 12]
    # encode class values as integers
    encoder.fit(Y)
    encoded_y = encoder.transform(Y)
    # convert integers to dummy variables (i.e. one hot encoded)
    dummy_y = np_utils.to_categorical(encoded_y)

    estimator = KerasClassifier(build_fn=baseline_model, epochs=100, batch_size=1, verbose=0)
    kfold = KFold(n_splits=10, shuffle=True)
    results = cross_val_score(estimator, X, dummy_y, cv=kfold)
    print(f"Baseline: {results.mean() * 100}% ({results.std() * 100}%)")


def initialize():
    global encoder, model
    encoder = LabelEncoder()
    model = Sequential()
    Path("./deep_learning/models/").mkdir(parents=True, exist_ok=True)


def get_prediction_for_user_id(user_id):
    print(f'USER ID FOR PREDICITON IS {user_id}')
    dic_predict = {}
    with open(PREDICT_FILE_PATH, encoding="utf8") as f:
        users_array = [{k: v for k, v in row.items()}
                       for row in csv.DictReader(f, skipinitialspace=True)]
        for row in users_array:
            key = row['Id']
            dic_predict[key] = row

    if user_id in dic_predict.keys():
        i = 0
        for key in dic_predict.keys():
            i = i + 1
            if str(key) == user_id:
                answer = get_prediction(i)
                return answer
    return None


def get_prediction(i):
    initialize()
    if is_model_saved():
        current_model = load_model(MODEL_SAVE_PATH)
        current_encoder = load_encoder()
    else:
        train_data()
        current_model = model
        current_encoder = encoder
        model.save(MODEL_SAVE_PATH, True)
        save_encoder()

    dataframe = pandas.read_csv(PREDICT_FILE_PATH, header=None)
    dataset = dataframe.values
    Xnew = dataset[i:i + 1, 0:11].astype(float)
    ynew = current_model.predict_classes(Xnew)
    return current_encoder.inverse_transform(ynew)[0]


def train_model():
    initialize()
    train_data()
    model.save(MODEL_SAVE_PATH, True)
    save_encoder()
