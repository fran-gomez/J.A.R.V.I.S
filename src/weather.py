# -*- encoding: utf-8 -*-

import requests
# import mimic
import json
import datetime

# Referencia del JSON con los resultados en
# https://www.meteored.com.ar/documentacion_api/es/Metadata_latam.pdf

class Weather:
    
    API_KEY = "e8db9e21c8c3494bda08cdc02e4f99f3"

    def __init__(self):
        self.currentWeather = None
        self.__updateWeather()
        self.weatherForecast = None
        self.__updateForecast()
        self.cityName = self.currentWeather['name']

    def __updateWeather(self):
        API_URL = f"http://api.openweathermap.org/data/2.5/weather?id=3865086&units=metric&lang=us&appid={self.API_KEY}"

        if not self.currentWeather or ((datetime.datetime.now() - self.currentWeatherUpdate).seconds > 3600):
            request = requests.get(API_URL)
            if request.status_code == 200:
                self.currentWeatherUpdate = datetime.datetime.now()
                self.currentWeather = request.json()
            else:
                print(f"Cannot update {request.status_code}")
    
    def __updateForecast(self):
        API_URL = f"http://api.openweathermap.org/data/2.5/onecall?exclude=minutely,hourly,alerts&lat=-38.7196&lon=-62.2724&lang=us&units=metric&cnt=7&appid={self.API_KEY}"

        if not self.weatherForecast or ((datetime.datetime.now() - self.weatherForecastUpdate).seconds > 3600):
            request = requests.get(API_URL)
            if request.status_code == 200:
                self.currentWeatherUpdate = datetime.datetime.now()
                self.weatherForecast = request.json()
            else:
                print(f"Cannot update {request.status_code}")

    def getTemperature(self, day = 0):

        if (day == 0):
            self.__updateWeather()
            temperature = int(self.currentWeather['main']['temp'])
            feelsLike = int(self.currentWeather['main']['feels_like'])
        else:
            return "You cant get the current temperature of tomorrow, you ass"
        
        temperatureUnit = "degrees celsius" if temperature > 1 else "degree celsius"

        temperatueStr = f'For {self.cityName}, the temperature is {temperature} {temperatureUnit} and feels like {feelsLike} {temperatureUnit}.'

        return temperatueStr

    def getMinMaxTemperature(self, day = 0):

        if day == 0:
            self.__updateWeather()
            minTemp = int(self.currentWeather['main']['temp_min'])
            maxTemp = int(self.currentWeather['main']['temp_max'])
        else:
            self.__updateForecast()
            count = self.weatherForecast['cnt']
            if day < count:
                minTemp = int(self.weatherForecast['dialy'][day+1]['temp']['min'])
                maxTemp = int(self.weatherForecast['dialy'][day+1]['temp']['max'])
            else:
                return "Day out of range"

        minTempUnit = "degrees celsius" if minTemp > 1 else "degree celsius"
        maxTempUnit = "degrees celsius" if maxTemp > 1 else "degree celsius"

        minMaxTempStr = f'For {self.cityName}, the minimum temperature is {minTemp} {minTempUnit} and the maximum temperature is {maxTemp} {maxTempUnit}.'

        return minMaxTempStr

    def getWindData(self, day = 0):
        compass_brackets = ["North", "North East", "East", "South East", "South", "South West", "West", "North West", "Notrh"]

        if day == 0:
            self.__updateWeather()
            windSpeed = self.currentWeather['wind']['speed']
            windDirection = compass_brackets[round(self.currentWeather['wind']['deg']/45)]
        else:
            self.__updateForecast()
            count = self.weatherForecast['cnt']
            if day < count:
                windSpeed = self.weatherForecast['dialy'][day]['speed']
                windDirection = compass_brackets[round(self.weatherForecast['dialy'][day]['deg']/45)]
            else:
                return "Day out of range"

        windSpeedUnit = "kilometers per hour" if windSpeed > 1 else "kilometer per hour"

        windStr = f'For {self.cityName}, the wind avarage speed is {windSpeed} {windSpeedUnit} from {windDirection}.'

        return windStr

    def getRain(self, day = 0):

        if day == 0:
            return "Not yet supported by API"
        else:
            self.__updateForecast()
            count = self.weatherForecast['cnt']
            if day < count:
                rainProbability = self.weatherForecast['dialy'][day]['pop'] * 100
            else:
                return "Day out of range"

        rainUnit = "percent"

        rainStr = f'For {self.cityName}, the rain chance is {rainProbability} {rainUnit}.'

        return rainStr

    def getPressure(self, day = 0):

        if day == 0:
            self.__updateWeather()
            pressure = self.currentWeather['main']['pressure']
        else:
            self.__updateForecast()
            count = self.weatherForecast['cnt']
            if day < count:
                pressure = self.weatherForecast['dialy'][day]['pressure']
            else:
                return "Day out of range"

        pressureUnit = "hectopascals" if pressure > 1 else "hectopascal"

        pressureStr = f'For {self.cityName}, the pressure is {pressure} {pressureUnit}'

        return pressureStr

    def getHumidity(self, day = 0):

        if day == 0:
            self.__updateWeather()
            humidity = self.currentWeather['main']['humidity']
        else:
            self.__updateForecast()
            count = self.weatherForecast['cnt']
            if day < count:
                humidity = self.weatherForecast['dialy'][day]['humidity']
            else:
                return "Day out of range"

        humidityUnit = "percent"

        humidityStr = f'For {self.cityName}, the humidity is {humidity} {humidityUnit}'

        return humidityStr

weather = Weather()
print(weather.getTemperature())
print(weather.getMinMaxTemperature())
print(weather.getWindData())
print(weather.getPressure())
print(weather.getHumidity())
print(weather.getRain())
