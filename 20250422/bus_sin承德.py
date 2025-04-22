import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import pandas as pd

def read_bus_data_from_csv(csv_file):
    """
    從 CSV 檔案讀取公車站點資料
    :param csv_file: CSV 檔案路徑
    :return: 公車站點資料 (list of dict)
    """
    # 讀取 CSV 檔案
    df = pd.read_csv(csv_file, header=None, names=["到達時間", "車站序號", "車站名稱", "車站編號", "緯度", "經度"])
    # 將資料轉換為字典列表
    bus_data = df.to_dict(orient="records")
    return bus_data

def generate_geojson_from_data(bus_data):
    """
    將公車站點資料轉換為 GeoDataFrame
    :param bus_data: 公車站點資料 (list of dict)
    :return: GeoDataFrame
    """
    geometry = [Point(stop["經度"], stop["緯度"]) for stop in bus_data]
    gdf = gpd.GeoDataFrame(bus_data, geometry=geometry)
    return gdf

def plot_bus_route(bus_data, output_image):
    """
    繪製單一路線的公車站點地圖，並儲存為圖片
    :param bus_data: 公車站點資料 (list of dict)
    :param output_image: 輸出的圖片檔案名稱
    """
    # 將公車站點資料轉換為 GeoDataFrame
    gdf = generate_geojson_from_data(bus_data)

    # 檢查資料是否正確載入
    if gdf.empty:
        print("無法生成地圖，公車站點資料為空。")
        return

    # 繪製地圖
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf.plot(ax=ax, color='blue', markersize=50, alpha=0.7, label='Bus Stops')

    # 繪製連接線（路線）
    if len(gdf) > 1:
        gdf = gdf.sort_values(by="車站序號")  # 按車站序號排序
        ax.plot(gdf.geometry.x, gdf.geometry.y, color='red', linewidth=2, label='Route')

    # 設定地圖標題與圖例
    ax.set_title("承德幹線路線圖", fontsize=16)
    ax.legend()
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)

    # 儲存地圖為圖片
    plt.savefig(output_image, format='jpg', dpi=300)
    print(f"地圖已儲存為 {output_image}")

# 主程式
if __name__ == "__main__":
    # 指定 CSV 檔案路徑
    csv_file = r"C:\Users\User\Desktop\cycu_oop_11022148\0161000900.csv"

    # 讀取公車站點資料
    bus_data = read_bus_data_from_csv(csv_file)

    # 指定輸出的圖片檔案名稱
    output_image = r"C:\Users\User\Desktop\cycu_oop_11022148\承德幹線路線圖.jpg"

    # 繪製公車路線圖並儲存為圖片
    plot_bus_route(bus_data, output_image)