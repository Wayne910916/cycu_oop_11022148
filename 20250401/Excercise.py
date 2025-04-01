import requests
from bs4 import BeautifulSoup

def extract_stations_and_links(url):
    # 發送 GET 請求以獲取 HTML 原始碼
    response = requests.get(url)
    if response.status_code != 200:
        print("無法連接到網站")
        return

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 去程與回程的區塊
    outbound_section = soup.find_all('tr', {'class': ['ttego1', 'ttego2']})  # 去程
    inbound_section = soup.find_all('tr', {'class': ['tteback1', 'tteback2']})  # 回程

    # 提取去程車站
    print(f"{'去程車站'.center(50)}")
    print(f"{'車站名稱'.center(20)} | {'連結'}")
    print("-" * 50)
    if outbound_section:
        for index, stop in enumerate(outbound_section):
            link_element = stop.find('a', href=True)
            if link_element:
                station_name = link_element.text.strip()
                station_link = link_element['href']
                print(f"{str(index).rjust(2)}. {station_name.center(20)} | {station_link}")
    else:
        print("無去程資料")

    # 提取回程車站
    print(f"\n{'回程車站'.center(50)}")
    print(f"{'車站名稱'.center(20)} | {'連結'}")
    print("-" * 50)
    if inbound_section:
        for index, stop in enumerate(inbound_section):
            link_element = stop.find('a', href=True)
            if link_element:
                station_name = link_element.text.strip()
                station_link = link_element['href']
                print(f"{str(index).rjust(2)}. {station_name.center(20)} | {station_link}")
    else:
        print("無回程資料")

# 目標網站 URL
url = "https://pda5284.gov.taipei/MQS/route.jsp?rid=10417"

# 呼叫函式
extract_stations_and_links(url)