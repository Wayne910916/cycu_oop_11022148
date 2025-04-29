import csv
import os
import requests
import json
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def download_and_parse_stops(route_code, save_path):
    """
    根據公車路線代碼從指定 URL 提取站點資料，並儲存為 CSV 檔案
    :param route_code: 公車路線代碼
    :param save_path: 儲存檔案的路徑
    """
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_code}"  # 替換為實際的下載 URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # 檢查是否下載成功
        soup = BeautifulSoup(response.content, 'html.parser')

        # 找到 GoDirectionRoute 區塊
        go_direction = soup.find('div', id='GoDirectionRoute')
        if not go_direction:
            print("無法找到 GoDirectionRoute 區塊")
            return

        # 提取站點資料
        stops = []
        for li in go_direction.find_all('li'):
            stop_name = li.find('span', class_='auto-list-stationlist-place')
            latitude = li.find('input', {'name': 'item.Latitude'})
            longitude = li.find('input', {'name': 'item.Longitude'})

            if stop_name and latitude and longitude:
                stops.append({
                    'stop_name': stop_name.text.strip(),
                    'latitude': latitude['value'],
                    'longitude': longitude['value']
                })

        # 將站點資料儲存為 CSV
        with open(save_path, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['stop_name', 'latitude', 'longitude'])
            writer.writeheader()
            writer.writerows(stops)

        print(f"成功儲存站點資料至 CSV 檔案：{save_path}")

    except requests.RequestException as e:
        print(f"下載失敗：{e}")

def read_csv_route(csv_path):
    """
    從 CSV 檔案讀取站點資料
    :param csv_path: CSV 檔案路徑
    :return: 站點資料列表，包括站名、緯度、經度
    """
    stops = []
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                stop_name = row['stop_name']
                latitude = float(row['latitude'])
                longitude = float(row['longitude'])
                stops.append((stop_name, latitude, longitude))
            except ValueError as e:
                print(f"跳過無效資料：{row}，錯誤：{e}")
    return stops

def read_geojson_stops(geojson_path):
    """
    從 GeoJSON 檔案讀取其他公車站點資料
    :param geojson_path: GeoJSON 檔案路徑
    :return: 站點資料列表，包括站名、緯度、經度
    """
    stops = []
    with open(geojson_path, mode='r', encoding='utf-8') as file:
        data = json.load(file)
        for feature in data['features']:
            try:
                stop_name = feature['properties']['BSM_CHINES']
                coordinates = feature['geometry']['coordinates']
                stops.append((stop_name, coordinates[1], coordinates[0]))  # 經緯度順序為 (緯度, 經度)
            except KeyError as e:
                print(f"跳過無效資料：{feature}，缺少鍵：{e}")
    return stops

def plot_route_with_highlight(csv_path, geojson_path, target_stop=None, image_path=None):
    """
    繪製路線圖，將目標路線的站點改為紅色，其他公車站點改為灰色，並在指定站點旁放置小人圖樣
    :param csv_path: 目標路線的 CSV 檔案路徑
    :param geojson_path: 其他公車站點的 GeoJSON 檔案路徑
    :param target_stop: 指定的站名（可選）
    :param image_path: 小人圖樣的路徑（可選）
    """
    # 從 CSV 檔案讀取目標路線的站點資料
    target_stops = read_csv_route(csv_path)

    # 從 GeoJSON 檔案讀取其他公車站點資料
    other_stops = read_geojson_stops(geojson_path)

    # 提取其他公車站點的經緯度
    other_latitudes = [stop[1] for stop in other_stops]
    other_longitudes = [stop[2] for stop in other_stops]

    # 提取目標路線的經緯度
    target_latitudes = [stop[1] for stop in target_stops]
    target_longitudes = [stop[2] for stop in target_stops]

    # 繪製圖表
    plt.figure(figsize=(10, 6))

    # 繪製其他公車站點（灰色點）
    plt.scatter(other_longitudes, other_latitudes, c='gray', label="其他公車站點", alpha=0.5)

    # 繪製目標路線的站點（紅色點）
    plt.scatter(target_longitudes, target_latitudes, c='red', label="目標路線", alpha=0.8)

    # 在指定站點放置小人圖樣
    if target_stop and image_path:
        for stop_name, lat, lon in target_stops:
            if stop_name == target_stop:
                try:
                    img = plt.imread(image_path)
                    imagebox = OffsetImage(img, zoom=0.025)  # 縮小小人圖樣，與站點大小一致
                    ab = AnnotationBbox(imagebox, (lon + 0.0001, lat + 0.0001), frameon=False)  # 偏移小人位置到站點旁邊
                    plt.gca().add_artist(ab)

                    # 在圖上顯示站名和經緯度
                    plt.text(lon, lat, f"{stop_name}\n({lat:.6f}, {lon:.6f})", fontsize=8, ha='center', color='blue')
                except FileNotFoundError:
                    print(f"無法找到圖像檔案：{image_path}")

    # 顯示圖例
    plt.legend()
    plt.show()

def main():
    route_code = input("請輸入目標公車路線代碼：")
    save_path = f"C:\\Users\\User\\Desktop\\cycu_oop_11022148\\bus_stops_{route_code}.csv"
    download_and_parse_stops(route_code, save_path)

    target_stop = input("請輸入目標站名（可選，按 Enter 跳過）：")
    geojson_path = r"C:\Users\User\Desktop\cycu_oop_11022148\20250422\bus_stop2.geojson"
    image_path = r"C:\Users\User\Desktop\cycu_oop_11022148\小人.png"
    plot_route_with_highlight(save_path, geojson_path, target_stop if target_stop else None, image_path if target_stop else None)

if __name__ == "__main__":
    main()