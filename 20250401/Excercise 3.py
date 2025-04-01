import os
from bs4 import BeautifulSoup

def get_bus_arrival_time_for_route(route_name, input_folder):
    # 確保輸入資料夾存在
    if not os.path.exists(input_folder):
        print("指定的資料夾不存在")
        return

    # 遍歷資料夾中的所有 HTML 檔案
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".html"):
            file_path = os.path.join(input_folder, file_name)

            # 使用 BeautifulSoup 解析 HTML 檔案
            with open(file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")

                # 查找指定路線名稱
                route_element = soup.find("a", string=lambda text: text and route_name in text)
                if route_element:
                    print(f"找到路線: {route_name} (檔案: {file_name})")

                    # 提取到站時間
                    arrival_time_element = route_element.find_next("td", {"align": "center", "data-deptimen1": "Y"})
                    if arrival_time_element:
                        arrival_time = arrival_time_element.text.strip()
                        print(f"路線名稱: {route_name}")
                        print(f"到站時間: {arrival_time}")
                        return
                    else:
                        print(f"路線名稱: {route_name}，無到站時間資訊")
                        return

    print(f"找不到名稱為 '{route_name}' 的路線資料")

# 指定輸入資料夾
input_folder = r"C:\Users\User\Desktop\cycu_oop_11022148\20250401"

# 指定路線名稱
route_name = "忠孝幹線"

# 呼叫函式
get_bus_arrival_time_for_route(route_name, input_folder)