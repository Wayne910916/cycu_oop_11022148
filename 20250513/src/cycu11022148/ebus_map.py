import requests
from bs4 import BeautifulSoup

def get_bus_stops(route_code):
    """
    根據公車幹線代號抓取所有停靠站並返回
    :param route_code: 公車幹線代號
    :return: 停靠站名稱列表
    """
    # 建立目標網址，將路線代號填入
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_code}"
    try:
        # 發送 HTTP GET 請求
        response = requests.get(url)
        response.raise_for_status()  # 確保請求成功，否則拋出例外
        soup = BeautifulSoup(response.content, 'html.parser')  # 解析 HTML 內容

        # 查看完整的 HTML 結構
        print(soup.prettify())  # 查看完整的 HTML 結構

        # 找到包含去程站點的區塊
        go_direction = soup.find('div', id='GoDirectionRoute')

        # 檢查是否正確找到目標區塊
        print(go_direction)  # 檢查是否正確找到目標區塊

        if not go_direction:
            print("無法找到 GoDirectionRoute 區塊")  # 如果找不到，提示錯誤訊息
            return []

        # 提取站點名稱
        stops = []
        for li in go_direction.find_all('li'):  # 遍歷所有站點列表項
            stop_name = li.find('span', class_='auto-list-stationlist-place')  # 找到站名
            if stop_name:
                stops.append(stop_name.text.strip())  # 去除多餘空白並加入列表

        return stops  # 返回站點名稱列表

    except requests.RequestException as e:
        print(f"下載失敗：{e}")  # 如果請求失敗，提示錯誤訊息
        return []

def main():
    """
    提供命令列介面，讓使用者輸入公車幹線代號並列印停靠站
    """
    # 提示使用者輸入公車路線代號
    route_code = input("請輸入公車幹線代號：")
    stops = get_bus_stops(route_code)  # 呼叫函數抓取停靠站
    if stops:
        # 如果有抓取到站點，列印結果
        print(f"公車路線 {route_code} 的停靠站如下：")
        for idx, stop in enumerate(stops, start=1):  # 列出站點名稱，並加上編號
            print(f"{idx}. {stop}")
    else:
        # 如果沒有抓取到站點，提示錯誤訊息
        print(f"未找到公車路線 {route_code} 的停靠站")

if __name__ == "__main__":
    main()  # 執行主程式