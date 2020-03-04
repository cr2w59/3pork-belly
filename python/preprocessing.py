import pandas as pd

# 날씨
df_w1 = pd.read_csv('./data/weather10to19.csv',encoding='euc-kr', header=0)
df_w2 = pd.read_csv('./data/weather20.csv',encoding='euc-kr', header=0)

df_w = pd.concat([df_w1, df_w2])
df_w = df_w.fillna(0)
df_w = df_w.iloc[:,2:]

# 삼겹살 가격
df_p = pd.read_csv('./data/price.csv',encoding='utf-8', header=0)

# 최종 데이터
df = pd.merge(df_w, df_p)
df.to_csv('./data/data.csv', encoding='utf-8', index=False)