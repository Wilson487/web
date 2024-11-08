from ttkbootstrap import *
import sys
import os
from PIL import Image, ImageTk
import requests

#######################設定工作目錄########################
os.chdir(sys.path[0])  # 設定工作目錄
#######################定義常數########################
API_KEY = "4b8d9fe291a337d9f58e4044ea9f2027"  # API Key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"  # API URL
UNITS = "metric"  # 單位 (公制)
LANG = "zh_tw"  # 語言 (繁體中文)
ICON_BASE_URL = "https://openweathermap.org/img/wn/"  # 天氣圖標基礎 URL


#######################定義函數########################
def get_weather_info():
    global UNITS, current_temperature
    city_name = city_name_entry.get()
    send_url = f"{BASE_URL}appid={API_KEY}&q={city_name}&units={UNITS}&lang={LANG}"
    response = requests.get(send_url)
    info = response.json()
    if "weather" in info and "main" in info:
        current_temperature = info["main"]["temp"]
        weather_description = info["weather"][0]["description"]
        icon_code = info["weather"][0]["icon"]
        icon_url = f"{ICON_BASE_URL}{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        if icon_response.status_code == 200:
            with open(f"{icon_code}.png", "wb") as icon_file:
                icon_file.write(icon_response.content)
        image = Image.open(f"{icon_code}.png")
        tk_image = ImageTk.PhotoImage(image)
        icon_label.config(image=tk_image)
        icon_label.image = tk_image
        temperature_label.config(
            text=f"溫度: {current_temperature}°{'C' if UNITS == 'metric' else 'F'}"
        )
        description_label.config(text=f"描述: {weather_description}")
    else:
        description_label.config(text="描述: 找不到該城市")


def on_switch_change():
    global UNITS, current_temperature
    UNITS = "metric" if check_type.get() else "imperial"
    if temperature_label["text"] != "溫度: ?°C":
        if UNITS == "metric":
            current_temperature = round((current_temperature - 32) * 5 / 9, 2)
        else:
            current_temperature = round(current_temperature * 9 / 5 + 32, 2)
        temperature_label.config(
            text=f"溫度: {current_temperature}°{'C' if UNITS == 'metric' else 'F'}"
        )


#######################建立視窗########################
window = tk.Tk()
window.title("Weather App")
#######################設定字型########################
font_size = 20
window.option_add("*font", ("Helvetica", font_size))
#######################建立變數########################
check_type = BooleanVar()
check_type.set(True)
#######################建立標籤########################
city_name_label = Label(window, text="請輸入想搜尋的城市:")
city_name_label.grid(row=0, column=0)
icon_label = Label(window, text="天氣圖標")
icon_label.grid(row=1, column=0)
temperature_label = Label(window, text="溫度: ?°C")
temperature_label.grid(row=1, column=1)
description_label = Label(window, text="描述: ?")
description_label.grid(row=1, column=2)
#######################建立輸入框########################
city_name_entry = Entry(window)
city_name_entry.grid(row=0, column=1)
#######################建立按鈕########################
search_button = Button(
    window, text="獲得天氣資訊", command=get_weather_info, style="my.TButton"
)
search_button.grid(row=0, column=2)
#######################建立Checkbutton########################
check = Checkbutton(
    window,
    variable=check_type,
    onvalue=True,
    offvalue=False,
    command=on_switch_change,
    style="my.TCheckbutton",
    text="溫度單位(°C/°F)",
)
check.grid(row=2, column=1, padx=10, pady=10)
#######################運行應用程式########################
window.mainloop()
