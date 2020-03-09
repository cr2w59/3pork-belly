from flask import Flask, render_template, request
import numpy as np
from model import predict

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        # 파라미터를 전달 받습니다.
        avg_temp = float(request.form['avg_temp'])
        min_temp = float(request.form['min_temp'])
        max_temp = float(request.form['max_temp'])
        rain_fall = float(request.form['rain_fall'])

        # 배추 가격 변수를 선언합니다.
        price = 0

        # 입력된 파라미터를 배열 형태로 준비합니다.
        data = ((avg_temp, min_temp, max_temp, rain_fall), (0, 0, 0, 0))
        arr = np.array(data, dtype=np.float32)

        # 입력 값을 토대로 예측 값을 찾아냅니다.
        x_data = arr[0:4]
        
        price = predict(x_data)

        return render_template('index.html', price=price)

if __name__ == '__main__':
    app.run(debug=True)