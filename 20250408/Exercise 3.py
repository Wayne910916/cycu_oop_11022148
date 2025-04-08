import asyncio
from playwright.async_api import async_playwright
import csv

async def fetch_all_data(route_id, output_file="all_data.csv"):
    """
    抓取指定公車代碼的所有站點資料，並將其彙整成一個 CSV 檔案。

    參數:
    - route_id: 公車代碼 (例如 '0100000A00')
    - output_file: 輸出的完整 CSV 檔案名稱
    """
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # 設置 headless=True 以便自動執行
        context = await browser.new_context()
        page = await context.new_page()

        try:
            print(f"正在載入網址: {url}")
            await page.goto(url)
            await page.wait_for_selector("#GoDirectionRoute", state="attached", timeout=30000)
            await page.wait_for_selector("#BackDirectionRoute", state="attached", timeout=30000)

            print("抓取去程資料...")
            outbound_data = await parse_stops(page, "#GoDirectionRoute", "去程")

            print("抓取返程資料...")
            return_data = await parse_stops(page, "#BackDirectionRoute", "返程")

            # 合併去程與返程資料
            all_data = outbound_data + return_data

            # 將所有資料寫入 CSV
            await write_to_csv(output_file, all_data)

            print(f"所有資料已儲存為 {output_file}")

        except Exception as e:
            print(f"發生錯誤: {e}")
        finally:
            await browser.close()

async def parse_stops(page, container_selector, direction):
    """
    解析站點資料。

    參數:
    - page: Playwright 的頁面對象
    - container_selector: 容器的 CSS 選擇器 (去程或返程)
    - direction: 方向 (去程或返程)
    """
    stops = await page.query_selector_all(f"{container_selector} li a.auto-list-link.auto-list-stationlist-link")
    data = []
    for stop in stops:
        arrival_info_element = await stop.query_selector(".auto-list-stationlist-position-time")
        arrival_info = await arrival_info_element.inner_text() if arrival_info_element else "未知"

        stop_number_element = await stop.query_selector(".auto-list-stationlist-number")
        stop_number = (await stop_number_element.inner_text()).strip() if stop_number_element else "未知"

        stop_name_element = await stop.query_selector(".auto-list-stationlist-place")
        stop_name = (await stop_name_element.inner_text()).strip() if stop_name_element else "未知"

        stop_id_element = await stop.query_selector("input#item_UniStopId")
        stop_id = await stop_id_element.get_attribute("value") if stop_id_element else "未知"

        latitude_element = await stop.query_selector("input#item_Latitude")
        latitude = await latitude_element.get_attribute("value") if latitude_element else "未知"

        longitude_element = await stop.query_selector("input#item_Longitude")
        longitude = await longitude_element.get_attribute("value") if longitude_element else "未知"

        data.append([direction, arrival_info, stop_number, stop_name, stop_id, latitude, longitude])

    return data

async def write_to_csv(file_name, data):
    """
    將資料寫入 CSV 檔案。

    參數:
    - file_name: 輸出的檔案名稱
    - data: 要寫入的資料
    """
    with open(file_name, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["方向", "公車到達時間", "車站序號", "車站名稱", "車站編號", "緯度", "經度"])
        writer.writerows(data)

if __name__ == "__main__":
    # 讓使用者輸入公車代碼
    route_id = input("請輸入公車代碼 (例如 '0100000A00'): ")
    asyncio.run(fetch_all_data(route_id))