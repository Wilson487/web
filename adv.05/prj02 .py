import json
import os
import sys

json_str = json

import requests

#################定義常數#################
API_KEY = "5a67c8c7f697cf6dc00b249ed3d17572"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANG = "zh_tw"
ICON_BASE_URL = "https://openweathermap.org/img/wn/"

#################主程式#################
os.chdir(sys.path[0])
city_name = input("請輸入城市名稱")
send_url = f"{BASE_URL}appid={API_KEY}&q={city_name}&units={UNITS}&lang={LANG}"
print(f"發送的URL:{send_url}")
response = requests.get(send_url)
info = response.json()

if "weather" in info and "main" in info:
    current_temperature = info["main"]["temp"]
    weather_description = info["weather"][0]["description"]
    icon_code = info["weather"][0]["icon"]
    print(f"城市:{city_name}")
    print(f"當前溫度:{current_temperature}℃")
    print(f"天氣描述:{weather_description}")
    icon_url = f"{ICON_BASE_URL}{icon_code}@2x.png"
    print(f"下載天氣圖標:{icon_code}")
    icon_response = requests.get(icon_url)

    if icon_response.status_code == 200:
        with open(f"{icon_code}.png", "wb") as icon_file:
            icon_file.write(icon_response.content)
            print(f"圖標已下載到{icon_code}.png")
    else:
        print("圖標下載失敗")
else:
    print("查詢失敗")
