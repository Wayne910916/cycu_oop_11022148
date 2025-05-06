import sys
import os

# 將 src 資料夾加入模組搜尋路徑
sys.path.append(r"C:\Users\User\Documents\GitHub\cycu_oop_11022148\20250506\src")

# 匯入模組
from cycu_11022148.hw import hello, world

if __name__ == "__main__":
    hello()
    world()
    print("Hello, World!")
    print("World!")