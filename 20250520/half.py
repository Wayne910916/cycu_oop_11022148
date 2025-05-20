import pandas as pd
import sys

# 設定輸出編碼
sys.stdout.reconfigure(encoding='utf-8')

# 載入 CSV 檔案，指定編碼
file_path = "c:/Users/User/Desktop/cycu_oop_11022148/20250520/midterm_scores.csv"
data = pd.read_csv(file_path, encoding='utf-8')  # 如果是 Big5 編碼，改為 encoding='big5'

# 計算每位學生不及格科目的數量
data['Fail_Count'] = (data.iloc[:, 2:] < 60).sum(axis=1)

# 計算科目數的一半
half_subjects = (data.shape[1] - 3) / 2  # 減去 Name 和 StudentID 兩欄

# 篩選出超過一半科目不及格的學生
students_half_fail = data[data['Fail_Count'] > half_subjects]

# 將結果存成新的 CSV 檔案
output_file = "c:/Users/User/Desktop/cycu_oop_11022148/20250520/students_half_fail.csv"
students_half_fail.to_csv(output_file, index=False, encoding='utf-8-sig')  # 使用 utf-8-sig 以支援 Excel 開啟

# 輸出結果
print("超過一半科目不及格的學生的成績已存成 CSV 檔案：")
print(output_file)