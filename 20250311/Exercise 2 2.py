import pandas as pd
import matplotlib.pyplot as plt

# 使用原始字符串來避免路徑問題
df = pd.read_excel(r'C:\Users\User\Desktop\cycu_oop_11022148\20250311\123.xlsx')

# 繪製 x 和 y 的散佈圖
plt.scatter(df['x'], df['y'])
plt.xlabel('x')
plt.ylabel('y')
plt.title('x 和 y 的散佈圖')
plt.show()
plt.show()