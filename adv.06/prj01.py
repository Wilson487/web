import requests

#######################定義常數########################
API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANG = "zh_tw"
########################主程式########################
city_name = "Paris"

send_url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units={UNITS}&lang={LANG}"
print(f"發送的URL:{send_url}")
response = requests.get(send_url)
requests.raise_for_status()
info = response.json()
if "city" in info:
    for forecast in info["list"]:
        dt_txt = forecast["dt_txt"]
        temp = forecast["main"]["temp"]
        weather_description = forecast["weather"][0]["description"]
        print(f"{dt_txt}-溫度:{temp}℃，天氣描述:{weather_description}")
else:
    print("查詢失敗")
