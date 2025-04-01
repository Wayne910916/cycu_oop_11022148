import os
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def extract_stations_and_links_with_rendering(url, output_folder):
    # 確保輸出資料夾存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 使用 Playwright 瀏覽器進行渲染
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 啟動無頭瀏覽器
        page = browser.new_page()

        # 發送 GET 請求以獲取 HTML 原始碼
        page.goto(url)
        soup = BeautifulSoup(page.content(), 'html.parser')  # 使用 BeautifulSoup 解析 HTML

        # 去程與回程的區塊
        outbound_section = soup.find_all('tr', {'class': ['ttego1', 'ttego2']})  # 去程
        inbound_section = soup.find_all('tr', {'class': ['tteback1', 'tteback2']})  # 回程

        # 提取去程車站
        print(f"{'去程車站'.center(50)}")
        print(f"{'車站名稱'.center(20)} | {'檔案名稱'}")
        print("-" * 50)
        if outbound_section:
            for index, stop in enumerate(outbound_section):
                link_element = stop.find('a', href=True)
                if link_element:
                    station_name = link_element.text.strip()
                    station_link = link_element['href']
                    stop_code = station_link.split('=')[-1]
                    file_name = f"bus_stop_{stop_code}.html"
                    file_path = os.path.join(output_folder, file_name)

                    # 渲染超連結內容
                    full_link = f"https://pda5284.gov.taipei/MQS/{station_link}"
                    page.goto(full_link)

                    # 等待到站時間的元素載入完成
                    try:
                        page.wait_for_selector(f'td#tte{stop_code}', timeout=5000)  # 等待到站時間元素
                    except:
                        print(f"無法載入到站時間，車站: {station_name}")

                    rendered_content = page.content()

                    # 使用 BeautifulSoup 解析渲染後的內容
                    rendered_soup = BeautifulSoup(rendered_content, 'html.parser')

                    # 提取到站時間資訊
                    arrival_time_element = rendered_soup.find('td', {'id': f"tte{stop_code}"})
                    arrival_time = arrival_time_element.text.strip() if arrival_time_element else "無到站時間"

                    # 在超連結後面添加到站時間
                    if link_element:
                        link_element.insert_after(rendered_soup.new_tag("p", string=f"到站時間: {arrival_time}"))

                    # 儲存渲染過的 HTML 檔案
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(rendered_soup.prettify())

                    print(f"{str(index).rjust(2)}. {station_name.center(20)} | {file_name}")
        else:
            print("無去程資料")

        # 提取回程車站
        print(f"\n{'回程車站'.center(50)}")
        print(f"{'車站名稱'.center(20)} | {'檔案名稱'}")
        print("-" * 50)
        if inbound_section:
            for index, stop in enumerate(inbound_section):
                link_element = stop.find('a', href=True)
                if link_element:
                    station_name = link_element.text.strip()
                    station_link = link_element['href']
                    stop_code = station_link.split('=')[-1]
                    file_name = f"bus_stop_{stop_code}.html"
                    file_path = os.path.join(output_folder, file_name)

                    # 渲染超連結內容
                    full_link = f"https://pda5284.gov.taipei/MQS/{station_link}"
                    page.goto(full_link)

                    # 等待到站時間的元素載入完成
                    try:
                        page.wait_for_selector(f'td#tte{stop_code}', timeout=5000)  # 等待到站時間元素
                    except:
                        print(f"無法載入到站時間，車站: {station_name}")

                    rendered_content = page.content()

                    # 使用 BeautifulSoup 解析渲染後的內容
                    rendered_soup = BeautifulSoup(rendered_content, 'html.parser')

                    # 提取到站時間資訊
                    arrival_time_element = rendered_soup.find('td', {'id': f"tte{stop_code}"})
                    arrival_time = arrival_time_element.text.strip() if arrival_time_element else "無到站時間"

                    # 在超連結後面添加到站時間
                    if link_element:
                        link_element.insert_after(rendered_soup.new_tag("p", string=f"到站時間: {arrival_time}"))

                    # 儲存渲染過的 HTML 檔案
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(rendered_soup.prettify())

                    print(f"{str(index).rjust(2)}. {station_name.center(20)} | {file_name}")
        else:
            print("無回程資料")

        browser.close()

# 目標網站 URL
url = "https://pda5284.gov.taipei/MQS/route.jsp?rid=10417"

# 指定輸出資料夾
output_folder = r"C:\Users\User\Desktop\cycu_oop_11022148\20250401"

# 呼叫函式
extract_stations_and_links_with_rendering(url, output_folder)