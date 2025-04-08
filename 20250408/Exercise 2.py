from datetime import datetime

def calculate_julian_and_weekday(input_time):
    # 將輸入的時間字串轉換為 datetime 格式
    try:
        input_datetime = datetime.strptime(input_time, "%Y-%m-%d %H:%M")
    except ValueError:
        return "輸入時間格式錯誤，請使用 YYYY-MM-DD HH:MM 格式"

    # 計算該天是星期幾
    weekday = input_datetime.strftime("%A")  # 取得星期幾（英文）
    weekday_chinese = {
        "Monday": "星期一",
        "Tuesday": "星期二",
        "Wednesday": "星期三",
        "Thursday": "星期四",
        "Friday": "星期五",
        "Saturday": "星期六",
        "Sunday": "星期日"
    }.get(weekday, "未知")

    # 計算 Julian 日期
    year = input_datetime.year
    month = input_datetime.month
    day = input_datetime.day
    hour = input_datetime.hour
    minute = input_datetime.minute
    second = input_datetime.second

    # 如果月份是 1 月或 2 月，將其視為前一年的第 13 或 14 月
    if month <= 2:
        year -= 1
        month += 12

    # Julian 日期公式
    A = year // 100
    B = 2 - A + (A // 4)
    julian_date = (365.25 * (year + 4716)) // 1 + (30.6001 * (month + 1)) // 1 + day + B - 1524.5
    julian_date += (hour + minute / 60 + second / 3600) / 24  # 加上時間部分

    # 計算輸入時間至現在的經過天數
    now = datetime.now()
    delta_days = (now - input_datetime).total_seconds() / 86400  # 經過的太陽日

    return f"該天是 {weekday_chinese}，Julian 日期為 {julian_date:.5f}，距今經過 {delta_days:.5f} 太陽日"

# 主程式
if __name__ == "__main__":
    input_time = input("請輸入時間（格式為 YYYY-MM-DD HH:MM，例如 2020-04-15 20:30）：")
    result = calculate_julian_and_weekday(input_time)
    print(result)