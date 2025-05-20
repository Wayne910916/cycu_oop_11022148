import geopandas as gpd
import matplotlib.pyplot as plt
from PIL import Image
import os
import csv
import requests
from bs4 import BeautifulSoup

# 設定 matplotlib 字體以支援中文
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 使用微軟正黑體
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 設定檔案路徑
shapefile_path = r"C:\Users\User\Desktop\cycu_oop_11022148\20250520\taipei_town\COUNTY_MOI_1140318.shp"
output_jpg = r"C:\Users\User\Desktop\cycu_oop_11022148\20250520\taipei_map_with_stops.jpg"
bus_stops_csv = r"C:\Users\User\Desktop\cycu_oop_11022148\20250520\bus_stops.csv"  # 公車站點 CSV 檔案

# 檢查 Shapefile 是否存在
if not os.path.exists(shapefile_path):
    print(f"Shapefile 檔案不存在：{shapefile_path}")
    print("請確認檔案是否存在，並檢查路徑是否正確。")
    exit()

# 下載並解析公車站點資料
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

# 讀取公車站點 CSV 檔案
def read_csv_route(csv_path):
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

# 讀取 Shapefile 檔案
try:
    gdf = gpd.read_file(shapefile_path)
    gdf = gdf.to_crs("EPSG:4326")  # 確保座標系統為 WGS84
except Exception as e:
    print(f"讀取 Shapefile 時發生錯誤：{e}")
    print("請確認檔案是否完整，並檢查是否包含 .shp, .shx, .dbf 等相關檔案。")
    exit()

# 提示用戶輸入公車路線代碼並下載站點資料
route_code = input("請輸入目標公車路線代碼：")
download_and_parse_stops(route_code, bus_stops_csv)

# 讀取公車站點資料
bus_stops = read_csv_route(bus_stops_csv)

# 提取公車站點的經緯度範圍
stop_lats = [stop[1] for stop in bus_stops]
stop_lons = [stop[2] for stop in bus_stops]
lat_min, lat_max = min(stop_lats), max(stop_lats)
lon_min, lon_max = min(stop_lons), max(stop_lons)

# 繪製地圖（聚焦公車路線部分）
fig, ax = plt.subplots(figsize=(10, 10))

# 繪製完整行政區輪廓（包括內部邊界）
gdf.plot(ax=ax, color="none", edgecolor="black", linewidth=0.5)

# 繪製公車站點
for stop_name, lat, lon in bus_stops:
    ax.scatter(lon, lat, color='red', s=10, label="公車站點" if '公車站點' not in ax.get_legend_handles_labels()[1] else "")

# 設定地圖範圍（聚焦公車路線部分，並增加適當邊距）
margin = 0.5  # 增加邊距
ax.set_xlim(lon_min - margin, lon_max + margin)
ax.set_ylim(lat_min - margin, lat_max + margin)

# 移除軸線和刻度
ax.axis("off")

# 設定標題
plt.title("公車路線聚焦圖", fontsize=16)

# 顯示圖例
plt.legend()

# 儲存為 PNG
png_file = r"C:\Users\User\Desktop\cycu_oop_11022148\20250520\taipei_map_with_stops_zoomed.png"
plt.savefig(png_file, dpi=300, bbox_inches="tight")
plt.close()

# 將 PNG 轉換為 JPG
image = Image.open(png_file)
rgb_image = image.convert("RGB")
rgb_image.save(output_jpg, "JPEG")

print(f"地圖已儲存為 {output_jpg}，請檢查該檔案。")