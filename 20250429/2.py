import csv
import requests
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
            stop_name_tag = li.find('span', class_='auto-list-stationlist-place')
            latitude_tag = li.find('input', {'name': 'item.Latitude'})
            longitude_tag = li.find('input', {'name': 'item.Longitude'})
            status_tag = None

            # 確認站點狀態
            if li.find('span', class_='auto-list-stationlist-position auto-list-stationlist-position-now'):
                status_tag = "進站中"
            elif li.find('span', class_='auto-list-stationlist-position auto-list-stationlist-position-none'):
                status_tag = "尚未發車"
            elif li.find('span', class_='auto-list-stationlist-position auto-list-stationlist-position-time'):
                status_tag = li.find('span', class_='auto-list-stationlist-position auto-list-stationlist-position-time').text.strip()

            # 確保站名、經緯度和狀態存在
            if stop_name_tag and latitude_tag and longitude_tag:
                stop_name = stop_name_tag.text.strip()
                latitude = latitude_tag['value']
                longitude = longitude_tag['value']
                status = status_tag if status_tag else "未知"

                stops.append({
                    'stop_name': stop_name,
                    'latitude': latitude,
                    'longitude': longitude,
                    'status': status
                })

        # 將站點資料儲存為 CSV
        with open(save_path, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['stop_name', 'latitude', 'longitude', 'status'])
            writer.writeheader()
            writer.writerows(stops)

        print(f"成功儲存站點資料至 CSV 檔案：{save_path}")

    except requests.RequestException as e:
        print(f"下載失敗：{e}")

def read_csv_route(csv_path):
    """
    從 CSV 檔案讀取站點資料
    :param csv_path: CSV 檔案路徑
    :return: 站點資料列表，包括站名、緯度、經度、狀態
    """
    stops = []
    in_station_stops = []  # 儲存進站中的站點
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                stop_name = row['stop_name']
                latitude = float(row['latitude'])
                longitude = float(row['longitude'])
                status = row['status']
                stops.append((stop_name, latitude, longitude, status))

                # 如果狀態為「進站中」，加入進站中的站點列表
                if status == "進站中":
                    in_station_stops.append((stop_name, latitude, longitude))
            except ValueError as e:
                print(f"跳過無效資料：{row}，錯誤：{e}")
    return stops, in_station_stops

def plot_route_with_highlight(csv_path, target_stop=None, image_path=None, bus_image_path=None):
    """
    繪製路線圖，將目標路線的站點改為紅色，並在進站中的站點放置公車圖樣
    :param csv_path: 目標路線的 CSV 檔案路徑
    :param target_stop: 指定的站名（可選）
    :param image_path: 小人圖樣的路徑（可選）
    :param bus_image_path: 公車圖樣的路徑
    """
    # 從 CSV 檔案讀取目標路線的站點資料
    target_stops, in_station_stops = read_csv_route(csv_path)

    # 提取目標路線的經緯度
    target_latitudes = [stop[1] for stop in target_stops]
    target_longitudes = [stop[2] for stop in target_stops]

    # 繪製圖表
    plt.figure(figsize=(10, 6))

    # 繪製目標路線的站點（紅色點）
    plt.scatter(target_longitudes, target_latitudes, c='red', label="目標路線", alpha=0.8)

    # 在指定站點放置小人圖樣
    if target_stop and image_path:
        for stop_name, lat, lon, status in target_stops:
            if stop_name == target_stop:
                try:
                    img = plt.imread(image_path)
                    imagebox = OffsetImage(img, zoom=0.025)  # 縮小小人圖樣，與站點大小一致
                    ab = AnnotationBbox(imagebox, (lon + 0.0001, lat + 0.0001), frameon=False)  # 偏移小人位置到站點旁邊
                    plt.gca().add_artist(ab)
                except FileNotFoundError:
                    print(f"無法找到圖像檔案：{image_path}")

    # 在進站中的站點放置公車圖樣
    if in_station_stops and bus_image_path:
        for stop_name, lat, lon in in_station_stops:
            try:
                bus_img = plt.imread(bus_image_path)
                bus_imagebox = OffsetImage(bus_img, zoom=0.03)  # 縮小公車圖樣
                bus_ab = AnnotationBbox(bus_imagebox, (lon, lat), frameon=False)  # 放置在站點位置
                plt.gca().add_artist(bus_ab)
            except FileNotFoundError:
                print(f"無法找到公車圖像檔案：{bus_image_path}")

    # 顯示圖例
    plt.legend()
    plt.show()

def main():
    route_code = input("請輸入目標公車路線代碼：")
    save_path = f"C:\\Users\\User\\Desktop\\cycu_oop_11022148\\bus_stops_{route_code}.csv"
    download_and_parse_stops(route_code, save_path)

    target_stop = input("請輸入目標站名（可選，按 Enter 跳過）：")
    image_path = r"C:\Users\User\Desktop\cycu_oop_11022148\小人.png"
    bus_image_path = r"C:\Users\User\Desktop\cycu_oop_11022148\公車.png"
    plot_route_with_highlight(save_path, target_stop if target_stop else None, image_path, bus_image_path)

if __name__ == "__main__":
    main()