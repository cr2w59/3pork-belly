from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from keras.callbacks import ModelCheckpoint, Callback
from keras.optimizers import RMSprop, Adam
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import tensorflow as tf
import os

SEED = 0
np.random.seed(SEED)
tf.set_random_seed(SEED)

# 데이터 로드
df = pd.read_csv('/content/data.csv', encoding='utf-8', header=0)
df.일시=df.일시.astype('float64')

# 상관관계 확인
plt.figure(figsize=(12,12))
sns.heatmap(df.corr(), linewidths=0.1, vmax=0.5, cmap=plt.cm.gist_heat, linecolor='white', annot=True)
plt.show()

# 데이터 분리
X = df.iloc[:,0:7]
Y = df.iloc[:,-1]
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, random_state=SEED)

# 데이터 정규화
X_train_stats = X_train.describe().T
def norm(x):
  return (x - X_train_stats['mean']) / X_train_stats['std']

normed_X_train = norm(X_train)
normed_X_test = norm(X_test)

# 모델 만들기
def create_model():
  model = Sequential()
  model.add(Dense(64, activation='relu', input_shape=[len(X_train.keys())]))
  model.add(Dense(32, activation='relu'))
  model.add(Dense(1))

  optimizer = RMSprop(lr=0.001, epsilon=1e-08)

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['accuracy', 'mae', 'mse'])
  return model

# 체크포인트 설정
CHECK_DIR = './check/'
if not os.path.exists(CHECK_DIR):
  os.mkdir(CHECK_DIR)

checkpoint_path = "./check/cp-{epoch:04d}.ckpt"
cp_callback = ModelCheckpoint(checkpoint_path, verbose=1, save_weights_only=True, save_best_only=True)

# 모델 학습 및 저장
model = create_model()
model.save_weights(checkpoint_path.format(epoch=0))
model.fit(normed_X_train, Y_train,
          epochs = 3500, callbacks = [cp_callback],validation_data = (normed_X_test, Y_test),verbose=0)

# 테스트 데이터를 이용한 예측값 시각화
Y_pred = model.predict(normed_X_test).flatten()
plt.scatter(Y_test, Y_pred)
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.axis('equal')
plt.axis('square')
plt.xlim(1000,2600)
plt.ylim(1000,2600)
_ = plt.plot([-100, 100], [-100, 100])

# 테스트 데이터를 이용한 오차 시각화
error = Y_pred - Y_test
plt.hist(error, bins = 25)
plt.xlabel("Prediction Error")
_ = plt.ylabel("Count")

# 모델 복원 및 절대 오차 확인
model = create_model()
model.load_weights('./check/cp-2905.ckpt')
_, _, mae, _ = model.evaluate(normed_X_test, Y_test, verbose=2)
print("복원된 모델의 절대 오차: {:5.2f}원".format(mae))

# 모델 전체 저장
from keras.models import load_model
model.save('model.h5')