import sys

# 將 20250513 資料夾加入模組搜尋路徑
sys.path.append(r"C:\Users\User\Desktop\cycu_oop_11022148\20250513")

# 匯入類別
from ebus_map import BusRouteFetcher

if __name__ == "__main__":
    # 提示使用者輸入公車幹線代號
    route_code = input("請輸入公車幹線代號：")
    fetcher = BusRouteFetcher(route_code)  # 建立抓取器物件
    fetcher.display_stops()  # 呼叫類別方法顯示停靠站