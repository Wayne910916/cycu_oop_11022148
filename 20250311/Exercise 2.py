import pandas as pd

# 使用原始字符串來避免路徑問題
df = pd.read_excel(r'C:\Users\User\Desktop\cycu_oop_11022148\20250311\123.xlsx')

# 計算 x 和 y 欄位的和，並將結果存入新欄位 'sum'
df['sum'] = df['x'] + df['y']

# 輸出結果
print(df['sum'])