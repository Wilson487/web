import json
import requests

json_str = json.dumps(data)
json_data = json.loads(json_str)
API_key = "XXX"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q="
UNITS = "metric"
LANG = "zh_tw"
