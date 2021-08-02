import requests
from datetime import datetime


class Weather:
    
    API_KEY = "e8db9e21c8c3494bda08cdc02e4f99f3"

    def __init__(self):
        self.current_weather = None
        self.__update_weather()
        self.weather_forecast = None
        self.__update_forecast()
        self.city_name = self.current_weather['name']

    def __update_weather(self):
        API_URL = f"http://api.openweathermap.org/data/2.5/weather?id=3865086&units=metric&lang=us&appid={self.API_KEY}"

        if (not self.current_weather or
            ((datetime.now() - self.current_weather_update).seconds > 3600)):
            request = requests.get(API_URL)
            if request.status_code == 200:
                self.current_weather_update = datetime.now()
                self.current_weather = request.json()
            else:
                print(f"Cannot update {request.status_code}")
    
    def __update_forecast(self):
        API_URL = f"http://api.openweathermap.org/data/2.5/onecall?exclude=minutely,hourly,alerts&lat=-38.7196&lon=-62.2724&lang=us&units=metric&cnt=7&appid={self.API_KEY}"

        if (not self.weather_forecast or
            ((datetime.now() - self.weather_forecast_update).seconds > 3600)):
            request = requests.get(API_URL)
            if request.status_code == 200:
                self.weather_forecast_update = datetime.now()
                self.weather_forecast = request.json()
            else:
                print(f"Cannot update {request.status_code}")

    def __get_daily_eference(self, day = 0):
        if day == 0:
            ref = "is"
        else:
            timestamp = self.weather_forecast['daily'][day]['dt']
            day = datetime.fromtimestamp(timestamp).strftime("%A")
            ref = f"on {day} will be"
        
        return ref

    def get_temperature(self, day = 0):

        if (day == 0):
            self.__update_weather()
            temperature = int(self.current_weather['main']['temp'])
            feels_like = int(self.current_weather['main']['feels_like'])
        else:
            return "You cant get the current temperature of tomorrow, you ass"
        
        ref = self.__get_daily_eference(day)
        temperature_unit = "degrees celsius" if temperature > 1 else "degree celsius"

        temperature_str = f'For {self.city_name}, the temperature {ref} {temperature} {temperature_unit} and feels like {feels_like} {temperature_unit}.'

        return temperature_str

    def get_min_max_temperature(self, day = 0):

        if day == 0:
            self.__update_weather()
            minTemp = int(self.current_weather['main']['temp_min'])
            maxTemp = int(self.current_weather['main']['temp_max'])
        else:
            self.__update_forecast()
            if 1 <= day <= 7:
                minTemp = int(self.weather_forecast['daily'][day]['temp']['min'])
                maxTemp = int(self.weather_forecast['daily'][day]['temp']['max'])
            else:
                return "Day out of range"

        ref = self.__get_daily_eference(day)
        minTempUnit = "degrees celsius" if minTemp > 1 else "degree celsius"
        maxTempUnit = "degrees celsius" if maxTemp > 1 else "degree celsius"

        minMaxTempStr = f'For {self.city_name}, the minimum temperature {ref} {minTemp} {minTempUnit} and the maximum temperature {ref} {maxTemp} {maxTempUnit}.'

        return minMaxTempStr

    def getWindData(self, day = 0):
        compass_brackets = ["North", "North East", "East", \
                            "South East", "South", "South West", \
                            "West", "North West", "Notrh"]

        if day == 0:
            self.__update_weather()
            windSpeed = self.current_weather['wind']['speed']
            windDirection = compass_brackets[round(self.current_weather['wind']['deg']/45)]
        else:
            self.__update_forecast()
            if 1 <= day <= 7:
                windSpeed = self.weather_forecast['daily'][day]['wind_speed']
                windDirection = compass_brackets[round(self.weather_forecast['daily'][day]['wind_deg']/45)]
            else:
                return "Day out of range"

        ref = self.__get_daily_eference(day)
        windSpeedUnit = "kilometers per hour" if windSpeed > 1 else "kilometer per hour"

        windStr = f'For {self.city_name}, the wind avarage speed {ref} {windSpeed} {windSpeedUnit} from the {windDirection}.'

        return windStr

    def getRain(self, day = 0):

        if day == 0:
            return "Not yet supported by API"
        else:
            self.__update_forecast()
            if 1 <= day <= 7:
                rainProbability = self.weather_forecast['daily'][day]['pop'] * 100
            else:
                return "Day out of range"

        ref = self.__get_daily_eference(day)
        rainUnit = "percent"

        rainStr = f'For {self.city_name}, the rain chance {ref} {rainProbability} {rainUnit}.'

        return rainStr

    def getPressure(self, day = 0):

        if day == 0:
            self.__update_weather()
            pressure = self.current_weather['main']['pressure']
        else:
            self.__update_forecast()
            if 1 <= day <= 7:
                pressure = self.weather_forecast['daily'][day]['pressure']
            else:
                return "Day out of range"
        
        ref = self.__get_daily_eference(day)
        pressureUnit = "hectopascals" if pressure > 1 else "hectopascal"

        pressureStr = f'For {self.city_name}, the pressure {ref} {pressure} {pressureUnit}'

        return pressureStr

    def getHumidity(self, day = 0):

        if day == 0:
            self.__update_weather()
            humidity = self.current_weather['main']['humidity']
        else:
            self.__update_forecast()
            if 1 <= day <= 7:
                humidity = self.weather_forecast['daily'][day]['humidity']
            else:
                return "Day out of range"

        ref = self.__get_daily_eference(day)
        humidityUnit = "percent"

        humidityStr = f'For {self.city_name}, the humidity {ref} {humidity} {humidityUnit}'

        return humidityStr
