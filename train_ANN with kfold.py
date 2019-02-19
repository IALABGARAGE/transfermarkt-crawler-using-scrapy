import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV

from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.wrappers.scikit_learn import KerasClassifier

import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

config = tf.ConfigProto(
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.8)
    # device_count = {'GPU': 1}
)
config.gpu_options.allow_growth = True
session = tf.Session(config=config)
set_session(session)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def load_data():

    print("-------------- Chargement des données--------------")

    df_clean = pd.read_csv('dataset_football_cleaned.csv')
    df_clean['end_contract'] = df_clean['end_contract'].fillna(1)
    df_clean = df_clean.dropna()

    le_nation = OneHotEncoder(handle_unknown='ignore')
    le_ligue = OneHotEncoder(handle_unknown='ignore')
    le_equipe = OneHotEncoder(handle_unknown='ignore')
    le_poste = OneHotEncoder(handle_unknown='ignore')

    le_nation.fit(np.array((df_clean['nation'])).reshape(-1,1))
    le_ligue.fit(np.array((df_clean['league'])).reshape(-1,1))
    le_equipe.fit(np.array((df_clean['team'])).reshape(-1,1))
    le_poste.fit(np.array((df_clean['position'])).reshape(-1,1))


    df_clean['nation'] = le_nation.transform(np.array(df_clean['nation']).reshape(-1,1)).toarray()
    df_clean['league'] = le_ligue.transform(np.array(df_clean['league']).reshape(-1,1)).toarray()
    df_clean['team'] = le_equipe.transform(np.array(df_clean['team']).reshape(-1,1)).toarray()
    df_clean['position'] = le_poste.transform(np.array(df_clean['position']).reshape(-1,1)).toarray()


    X = df_clean.drop(['price'],axis=1)
    y = df_clean['price']

    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)
    print("-------------- Données chargées --------------")


    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.07, random_state=42)

    return X,y

def build_model(learn_rate=0.01, lbd=10e-10):


    # Initialising the ANN : création des différentes couches

    model = Sequential()

    model.add(Dense(units=256, activation='relu', input_dim=X.shape[1]))
    model.add(Dropout(0.2))

    model.add(Dense(units=256, activation='relu'))
    model.add(Dropout(0.2))

    model.add(Dense(units=256, activation='relu'))
    model.add(Dropout(0.2))

    model.add(Dense(units=256, activation='relu'))
    model.add(Dropout(0.2))

    model.add(Dense(units=256, activation='relu'))
    model.add(Dropout(0.2))

    model.add(Dense(1))


    opt = optimizers.RMSprop(lr=learn_rate, decay=lbd)

    model.compile(optimizer=opt, loss='mse', metrics=['accuracy'])

    # callbacks = [EarlyStopping(monitor='loss', patience=30)]

    return model

def plot_training(history):

    print(history.history.keys())

    # summarize history for loss
    plt.plot(history.history['mean_absolute_error'])
    plt.plot(history.history['val_mean_absolute_error'])

    plt.title('model mean_absolute_error')
    plt.ylabel('mean_absolute_error')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    return

def predict():
    prediction = (pd.concat([pd.DataFrame(model.predict(X_test)),y_test.reset_index(drop=True)], axis=-1))
    return prediction





X,Y = load_data()


model = KerasClassifier(build_fn=build_model)

# define the grid search parameters
batch_size = [1,5]
epochs = [10]
learn_rate  = [0.005, 0.0005]
param_grid = dict(learn_rate=learn_rate, batch_size=batch_size, epochs=epochs)
grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=1)
grid_result = grid.fit(X, Y)
# summarize results


print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))

means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']

for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))




# history = model.fit(X_train, y_train,
#                              batch_size=1,
#                              epochs=500,
#                              callbacks=callbacks,
#                              validation_data=(X_test, y_test))
