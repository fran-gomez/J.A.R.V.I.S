# -*- encoding: utf-8 -*-

import requests
from datetime import date, datetime, timedelta, timezone

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

        if not self.currentWeather or ((datetime.now() - self.currentWeatherUpdate).seconds > 3600):
            request = requests.get(API_URL)
            if request.status_code == 200:
                self.currentWeatherUpdate = datetime.now()
                self.currentWeather = request.json()
            else:
                print(f"Cannot update {request.status_code}")
    
    def __updateForecast(self):
        API_URL = f"http://api.openweathermap.org/data/2.5/onecall?exclude=minutely,hourly,alerts&lat=-38.7196&lon=-62.2724&lang=us&units=metric&cnt=7&appid={self.API_KEY}"

        if not self.weatherForecast or ((datetime.now() - self.weatherForecastUpdate).seconds > 3600):
            request = requests.get(API_URL)
            if request.status_code == 200:
                self.weatherForecastUpdate = datetime.now()
                self.weatherForecast = request.json()
            else:
                print(f"Cannot update {request.status_code}")

    def __getDailyReference(self, day = 0):
        if day == 0:
            ref = "is"
        else:
            timestamp = self.weatherForecast['daily'][day]['dt']
            day = datetime.fromtimestamp(timestamp).strftime("%A")
            ref = f"on {day} will be"
        
        return ref

    def getTemperature(self, day = 0):

        if (day == 0):
            self.__updateWeather()
            temperature = int(self.currentWeather['main']['temp'])
            feelsLike = int(self.currentWeather['main']['feels_like'])
        else:
            return "You cant get the current temperature of tomorrow, you ass"
        
        ref = self.__getDailyReference(day)
        temperatureUnit = "degrees celsius" if temperature > 1 else "degree celsius"

        temperatueStr = f'For {self.cityName}, the temperature {ref} {temperature} {temperatureUnit} and feels like {feelsLike} {temperatureUnit}.'

        return temperatueStr

    def getMinMaxTemperature(self, day = 0):

        if day == 0:
            self.__updateWeather()
            minTemp = int(self.currentWeather['main']['temp_min'])
            maxTemp = int(self.currentWeather['main']['temp_max'])
        else:
            self.__updateForecast()
            if 1 <= day <= 7:
                minTemp = int(self.weatherForecast['daily'][day]['temp']['min'])
                maxTemp = int(self.weatherForecast['daily'][day]['temp']['max'])
            else:
                return "Day out of range"

        ref = self.__getDailyReference(day)
        minTempUnit = "degrees celsius" if minTemp > 1 else "degree celsius"
        maxTempUnit = "degrees celsius" if maxTemp > 1 else "degree celsius"

        minMaxTempStr = f'For {self.cityName}, the minimum temperature {ref} {minTemp} {minTempUnit} and the maximum temperature {ref} {maxTemp} {maxTempUnit}.'

        return minMaxTempStr

    def getWindData(self, day = 0):
        compass_brackets = ["North", "North East", "East", "South East", "South", "South West", "West", "North West", "Notrh"]

        if day == 0:
            self.__updateWeather()
            windSpeed = self.currentWeather['wind']['speed']
            windDirection = compass_brackets[round(self.currentWeather['wind']['deg']/45)]
        else:
            self.__updateForecast()
            if 1 <= day <= 7:
                windSpeed = self.weatherForecast['daily'][day]['wind_speed']
                windDirection = compass_brackets[round(self.weatherForecast['daily'][day]['wind_deg']/45)]
            else:
                return "Day out of range"

        ref = self.__getDailyReference(day)
        windSpeedUnit = "kilometers per hour" if windSpeed > 1 else "kilometer per hour"

        windStr = f'For {self.cityName}, the wind avarage speed {ref} {windSpeed} {windSpeedUnit} from the {windDirection}.'

        return windStr

    def getRain(self, day = 0):

        if day == 0:
            return "Not yet supported by API"
        else:
            self.__updateForecast()
            if 1 <= day <= 7:
                rainProbability = self.weatherForecast['daily'][day]['pop'] * 100
            else:
                return "Day out of range"

        ref = self.__getDailyReference(day)
        rainUnit = "percent"

        rainStr = f'For {self.cityName}, the rain chance {ref} {rainProbability} {rainUnit}.'

        return rainStr

    def getPressure(self, day = 0):

        if day == 0:
            self.__updateWeather()
            pressure = self.currentWeather['main']['pressure']
        else:
            self.__updateForecast()
            if 1 <= day <= 7:
                pressure = self.weatherForecast['daily'][day]['pressure']
            else:
                return "Day out of range"
        
        ref = self.__getDailyReference(day)
        pressureUnit = "hectopascals" if pressure > 1 else "hectopascal"

        pressureStr = f'For {self.cityName}, the pressure {ref} {pressure} {pressureUnit}'

        return pressureStr

    def getHumidity(self, day = 0):

        if day == 0:
            self.__updateWeather()
            humidity = self.currentWeather['main']['humidity']
        else:
            self.__updateForecast()
            if 1 <= day <= 7:
                humidity = self.weatherForecast['daily'][day]['humidity']
            else:
                return "Day out of range"

        ref = self.__getDailyReference(day)
        humidityUnit = "percent"

        humidityStr = f'For {self.cityName}, the humidity {ref} {humidity} {humidityUnit}'

        return humidityStr
