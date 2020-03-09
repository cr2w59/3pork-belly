from flask import Flask, render_template, request
import pandas as pd
from model import predict

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        date = float(request.form['date'])
        avg_temp = float(request.form['avg_temp'])
        min_temp = float(request.form['min_temp'])
        max_temp = float(request.form['max_temp'])
        rain_fall = float(request.form['rain_fall'])
        avg_wind = float(request.form['avg_wind'])
        humidity = float(request.form['humidity'])
        price = 0

        data = {'일시': date, '평균기온(°C)': avg_temp, '최저기온(°C)': min_temp,
                '최고기온(°C)':max_temp,'일강수량(mm)':rain_fall,
                '평균 풍속(m/s)':avg_wind,'평균 상대습도(%)':humidity}
        x = pd.DataFrame(data, columns=['일시','평균기온(°C)','최저기온(°C)','최고기온(°C)','일강수량(mm)','평균 풍속(m/s)','평균 상대습도(%)']) 
        price = predict(x)

        return render_template('index.html', price=price)

if __name__ == '__main__':
    app.run(debug=True)