from bus_fun import fetch_bus_stops
import csv

# 將結果存為 CSV 檔案
def save_to_csv(data, filename):
    """
    將公車站點資料存為 CSV 檔案
    :param data: 公車站點資料列表
    :param filename: 要儲存的 CSV 檔案名稱
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 寫入標題行
        writer.writerow(["到達時間", "車站序號", "車站名稱", "車站編號", "緯度", "經度"])
        # 寫入資料
        writer.writerows(data)

# 主程式
if __name__ == "__main__":
    route_id = input("請輸入公車代碼 (例如 '0100000A00')：")
    result = fetch_bus_stops(route_id)
    if result:
        # 儲存為 CSV 檔案
        filename = f"{route_id}_stops.csv"
        save_to_csv(result, filename)
        print(f"公車站點資料已儲存為 {filename}")
    else:
        print("未能取得任何資料，請檢查公車代碼是否正確。")