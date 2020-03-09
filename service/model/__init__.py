import json, sys, os
from sklearn.externals import joblib
from model.modeling import norm, X_train_stats

if __name__!='__main__':
    MODEL_PATH = './service/check/model2.h5'
    model = joblib.load(MODEL_PATH)
    model.load_weights('./check/cp-2905.ckpt')

def predict(data):
    x = norm(data)
    pred = model.predict(x).flatten() 
    return float(pred)