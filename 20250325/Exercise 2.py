import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import font_manager

# 手動設定字型路徑（請確認字型路徑是否正確）
font_path = 'C:/Windows/Fonts/msjh.ttc'  # 微軟正黑體字型路徑
font_prop = font_manager.FontProperties(fname=font_path)
rcParams['font.sans-serif'] = font_prop.get_name()
rcParams['axes.unicode_minus'] = False  # 解決負號無法顯示的問題

# 讀取清理後的 CSV 檔案
file_path = r'C:/Users/User/Desktop/cycu_oop_11022148/20250325/ExchangeRate_Cleaned.csv'
df = pd.read_csv(file_path, encoding='utf-8-sig')

# 確保欄位名稱正確
if '資料日期' not in df.columns or '現金買入' not in df.columns or '現金賣出' not in df.columns:
    print("欄位名稱不正確，請檢查檔案內容。")
    exit()

# 將資料日期轉換為日期格式
df['資料日期'] = pd.to_datetime(df['資料日期'], format='%Y%m%d')

# 繪製匯率走勢圖
plt.figure(figsize=(12, 6))
plt.plot(df['資料日期'], df['現金買入'], label='現金買入', marker='o')
plt.plot(df['資料日期'], df['現金賣出'], label='現金賣出', marker='o')

# 設定圖表標題與軸標籤
plt.title('現金買入與現金賣出匯率走勢圖', fontsize=16)
plt.xlabel('日期', fontsize=12)
plt.ylabel('匯率', fontsize=12)
plt.legend()
plt.grid()

# 顯示圖表
plt.show()