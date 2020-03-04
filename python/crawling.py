from bs4 import BeautifulSoup
from selenium import webdriver
import time
import datetime as dt
import pandas as pd

path = "D:/devTools/Anaconda3/chromedriver.exe"
driver = webdriver.Chrome(path)

sd = dt.date(year=2010,month=1,day=1)
ed = sd
yesterday = 1883    #2009-12-31 삼겹살 가격
while(ed != dt.date(year=2020,month=3,day=1)):
    url = f'https://www.kamis.or.kr/customer/price/retail/period.do?action=daily&startday={str(sd)}&endday={str(ed)}&countycode=1101&itemcategorycode=500&itemcode=514&kindcode=&productrankcode=&convert_kg_yn=N'
    driver.get(url)
    html = driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    t1 = soup.find('table',id='itemTable_2')
    try:
        last = int(t1.find('td',class_='last').text.replace(',',''))
        with open('./data/price.csv', mode='a') as f:
            f.write(f'{sd},{last}\n')
    except:
        yesterday = last
        with open('./data/price.csv', mode='a') as f:
            f.write(f'{sd},{yesterday}\n')
    sd = sd + dt.timedelta(days=1)
    ed = sd

driver.close()