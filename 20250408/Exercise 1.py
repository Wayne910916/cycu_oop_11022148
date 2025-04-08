import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm

def plot_lognormal_cdf(mu, sigma):
    """
    繪製對數常態累積分布函數 (CDF) 圖形並儲存為 JPG 檔案。

    參數:
    - mu: 對數常態分布的均值
    - sigma: 對數常態分布的標準差
    """
    # 設定中文字體
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 微軟正黑體
    plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

    # 計算對數常態分布的參數
    s = sigma
    scale = np.exp(mu)

    # 定義 x 軸範圍
    x = np.linspace(0.01, 10, 1000)

    # 計算累積分布函數 (CDF)
    cdf = lognorm.cdf(x, s, scale=scale)

    # 繪製圖形
    plt.figure(figsize=(8, 6))
    plt.plot(x, cdf, label='對數常態累積分布函數', color='blue')
    plt.title('對數常態累積分布函數', fontsize=14)
    plt.xlabel('x 值', fontsize=12)
    plt.ylabel('累積分布函數 (CDF)', fontsize=12)
    plt.grid(True)
    plt.legend(fontsize=12)

    # 儲存為 JPG 檔案
    filename = f'對數常態累積分布函數_mu{mu}_sigma{sigma}.jpg'
    plt.savefig(filename, format='jpg', dpi=300)
    plt.show()
    print(f"圖形已儲存為 {filename}")

# 主程式
if __name__ == "__main__":
    try:
        mu = float(input("請輸入對數常態分布的均值 (mu)："))
        sigma = float(input("請輸入對數常態分布的標準差 (sigma)："))
        plot_lognormal_cdf(mu, sigma)
    except ValueError:
        print("輸入的參數必須是數值！")