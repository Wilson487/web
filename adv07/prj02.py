import requests
import datetime
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os
import sys
from ttkbootstrap import *
from PIL import Image, ImageTk

#######################設定工作目錄########################
os.chdir(sys.path[0])
#######################定義常數########################
API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?"  # 5 Day / 3 Hour Forecast API URL
UNITS = "metric"  # 使用公制單位
LANG = "zh_tw"  # 使用繁體中文
#################定義常數#################
API_KEY = "5a67c8c7f697cf6dc00b249ed3d17572"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANG = "zh_tw"
ICON_BASE_URL = "https://openweathermap.org/img/wn/"


#######################主程式########################
def draw_graph():
    city_name = "Taipei"  # 可以改為任何城市名稱
    # 構建請求 URL
    send_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANG}"
    print(f"發送的 URL：{send_url}")  # 印出發送的 URL
    response = requests.get(send_url)
    response.raise_for_status()  # 檢查請求是否成功
    info = response.json()
    # 準備繪圖數據
    xlist = []  # 準備 x 軸數據
    ylist = []  # 準備 y 軸數據
    if "city" in info:
        # 處理並顯示天氣預報
        for forecast in info["list"]:
            dt_txt = forecast["dt_txt"]  # 預報時間
            temp = forecast["main"]["temp"]  # 預報溫度
            time = datetime.datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S").strftime(
                "%m/%d %H"
            )  # 格式化時間
            xlist.append(time)
            ylist.append(temp)
            print(f"{time} 的溫度是 {temp} 度")
    else:
        print("找不到該城市或無法獲取天氣資訊")
    # https://fonts.google.com/
    font = FontProperties(
        fname="NotoSansTC-Black.otf", size=14
    )  # 設定字型這樣才能顯示中文
    fig, ax = plt.subplots(figsize=(12, 6))  # 設定圖表大小, 單位是英寸
    ax.plot(xlist, ylist)  # 使用軸對象繪製圖表
    ax.set_title("5 天氣溫預測", fontproperties=font)
    ax.set_ylabel("溫度 (°C)", fontproperties=font)
    ax.set_xlabel("日期", fontproperties=font)
    plt.xticks(rotation=45)  # 旋轉 x 軸標籤以避免重疊
    plt.tight_layout()  # 自動調整佈局
    fig.savefig("weather_forecast.png")  # 儲存圖表
    plt.close()

    image = Image.open("weather_forecast.png")
    img = ImageTk.PhotoImage(image)

    canvas.config(width=image.width, height=import_image.height)
    canvas.create_image(image.width // 2, image.height // 2, image=img)
    canvas.image = img


#######################建立視窗###########################
Window = tk.Tk()
Window.title("Weather APP")
#######################建立畫布###########################
canvas = Canvas(Window, width=0, height=0, bg="white")
canvas.pack(row=0, columun=0, padx=10, pady=10)

#########################設定字型###########################
font_size = 20
Window.option_add("*Font", ("Helvetica", font_size))
#########################設定按鈕###########################
style = Style(them="minty")
style.configure("my.TButton", font=("Helvetica", font_size))

#######################建立按鈕###########################
draw_button = Button(Window, text="顯示圖表", command=draw_graph, style="my.TButton")
draw_button.pack(row=1, columun=0, padx=10, pady=10)

######################運行應用程式###########################
Window.mainloop()
