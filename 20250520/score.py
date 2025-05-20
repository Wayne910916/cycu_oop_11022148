import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np

# 設定輸出編碼
sys.stdout.reconfigure(encoding='utf-8')

# 設定 matplotlib 字體以支援中文
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 使用 SimHei 字體（黑體）
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 載入 CSV 檔案，指定編碼
file_path = "c:/Users/User/Desktop/cycu_oop_11022148/20250520/midterm_scores.csv"
data = pd.read_csv(file_path, encoding='utf-8')  # 如果是 Big5 編碼，改為 encoding='big5'

# 提取科目名稱（從第三列開始）
subjects = data.columns[2:]

# 設定顏色順序
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'purple']

# 繪製直方圖
plt.figure(figsize=(15, 8))
bin_edges = np.arange(0, 101, 10)  # 成績級距為 10
bar_width = 5 / len(subjects)  # 調整每個科目的長條寬度，讓條狀更寬

for i, subject in enumerate(subjects):
    # 計算每個級距的學生人數
    counts, _ = np.histogram(data[subject], bins=bin_edges)
    # 設定每個科目的長條位置，避免重疊
    bar_positions = bin_edges[:-1] + i * bar_width
    # 繪製長條圖
    plt.bar(bar_positions, counts, width=bar_width, color=colors[i % len(colors)], label=subject, edgecolor='black')

# 圖表標題與標籤（改為中文）
plt.title('成績級距', fontsize=16)
plt.xlabel('成績級距', fontsize=12)
plt.ylabel('學生人數', fontsize=12)
plt.xticks(bin_edges + bar_width * (len(subjects) - 1) / 2, labels=bin_edges)  # 調整 x 軸標籤位置
plt.legend(title='科目', fontsize=10)

# 顯示圖表
plt.tight_layout()
plt.show()