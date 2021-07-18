# -*- encoding: utf-8 -*-

import json
import requests
from requests.api import request

class Weather:
    API_KEY = "e8db9e21c8c3494bda08cdc02e4f99f3"
    
    def get_forecast(self):
        API_URL = f'http://api.openweathermap.org/data/2.5/forecast?&id=3865086&units=metric&appid={self.API_KEY}'

        response = requests.get(API_URL)

        print(response.status_code)
        text = json.dumps(response.json(), sort_keys=True, indent=2)
        print(text)
    
    def get_weather_report(self):
        API_URL = f'http://api.openweathermap.org/data/2.5/weather?&id=3865086&units=metric&appid={self.API_KEY}'

        response = requests.get(API_URL)
        name = response.json()['name'] # Nombre de la ciudad
        main = response.json()['main'] # Sensacion termica, humedad, presion, temperatura
        weather = response.json()['weather'] # Descripcion
        wind = response.json()['wind'] # Orientacion, rafaga maxima, velocidad

        print(f'{name}\n')
        print(f'{main}\n')
        print(f'{weather}\n')
        print(f'{wind}\n')


Weather.get_weather_report()