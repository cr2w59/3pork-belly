# -*- coding: utf-8 -*-
"""modeling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10CkEEXz_psfeQUTSgVQyTFN9B-IEoLSI
"""

# Commented out IPython magic to ensure Python compatibility.
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import ModelCheckpoint, EarlyStopping

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import tensorflow as tf
import os
# %tensorflow_version 1.x

SEED = 0
np.random.seed(SEED)
tf.set_random_seed(SEED)

df = pd.read_csv('/content/data.csv', encoding='utf-8', header=0)

df['평균 풍속(km/h)'] = df['평균 풍속(m/s)'].values * 3.6

df['평균체감온도(°C)'] = 13.12+(0.6215*df['평균기온(°C)'].values)-(11.37*df['평균 풍속(km/h)'].values**0.15)+(0.3965*df['평균 풍속(km/h)'].values**0.15)

df = df[['일시', '평균기온(°C)', '최저기온(°C)', '최고기온(°C)', '평균체감온도(°C)', '일강수량(mm)', '평균 풍속(km/h)','평균 상대습도(%)', '가격']]

df.head()

plt.figure(figsize=(10,10))
sns.heatmap(data = df.corr(), annot=True,fmt = '.2f', linewidths=.5, cmap='Reds')

data = df[['일시', '평균기온(°C)', '최저기온(°C)', '최고기온(°C)', '평균체감온도(°C)', '가격']]

set = data.values
X = set[:,1:5]
Y = set[:,-1]

model = Sequential()
model.add(Dense(32,input_dim=4,activation="relu"))
model.add(Dropout(0.3))
for i in range(2):
    model.add(Dense(32,activation="relu"))
    model.add(Dropout(0.3))
model.add(Dense(1))

model.compile(loss='mean_squared_error', optimizer='adagrad')

hist = model.fit(x_train, y_train, epochs=200, batch_size=32, validation_data=(x_val, y_val))