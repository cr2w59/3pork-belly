import json, sys, os
from keras.optimizers import RMSprop
from keras.models import load_model
from model.modeling import norm, X_train_stats

if __name__!='__main__':
    MODEL_PATH = './service/check/model2.h5'
    model = load_model(MODEL_PATH)
    model.load_weights('./check/cp-2905.ckpt')
    
    optimizer = RMSprop(lr=0.001, epsilon=1e-08)
    model.compile(loss='mse', optimizer=optimizer)
    
def predict(data):
    x = norm(data)
    pred = model.predict(x).flatten() 
    print(pred)
    return float(pred)