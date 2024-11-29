import requests


class WeatherAPI:
    def __init__(self, api_key, units="metric", lang="zh_tw"):
        self.api_key = api_key
        self.units = units
        self.lang = lang
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.icon_base_url = "https://openweathermap.org/img/wn/"

    def get_current_weather(self, city_name):
        send_url = f"{self.base_url}&appid={self.api_key}?q={city_name}&units={self.units}&lang={self.lang}"
        response = requests.get(send_url)
        return response.json()

    def get_forecast(self, city_name):
        send_url = f"{self.forecast_url}q={city_name}&appid={self.api_key}&units={self.units}&lang={self.lang}"
        response = requests.get(send_url)
        response.raise_for_status()
        return response.json()

    def get_icon_url(self, icon_code):
        return f"{self.icon_base_url}{icon_code}@2x.png"

    def get_icon(self, icon_code):
        icon_url = self.get_icon_url(icon_code)
        response = requests.get(icon_url)
        if response.status_code == 200:
            return response.content
        else:
            return None

    async def create_weather_embed(self, city, weather_info):
        unit_symbol = "C" if self.units == "metric" else "F"
        if "weather" in weather_info and "main" in weather_info:
            current_temperature = weather_info["main"]["temp"]
            weather_description = weather_info["weather"][0]["description"]
            icon_code = weather_info["weather"][0]["icon"]
            icon_url = self.get_icon_url(icon_code)
            embed=discord.Embed(
                titke=f"{city}當前的天氣描述"
                description=f"描述{weather_description}",
                color=0x1E90FF,

            )
            embed.set_thumbnail(url=icon_url)
            embed.add_field(name="氣溫", value=f"{current_temperature}度{unit_symbol}",inline=False)
            return embed
        return None
