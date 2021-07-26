# -*- encoding: utf-8 -*-

import requests
import mimic
import json
import datetime

# Referencia del JSON con los resultados en
# https://www.meteored.com.ar/documentacion_api/es/Metadata_latam.pdf

class Weather:
    def __init__(self):
        self.requestWeatherAPI()
        self.unitsStr = {'°C': 'degree Celsius',
                         '°C(p)': 'degrees Celsius',
                         '°F': 'degree Fahrenheit',
                         '°F(p)': 'degrees Fahrenheit',
                         'km/h': 'kilometer per hour',
                         'km/h(p)': 'kilometers per hour',
                         'mph': 'mile per hour',
                         'mph(p)': 'miles per hour',
                         'mm': 'millimeter',
                         'mm(p)': 'millimeters',
                         'in': 'inch',
                         'in(p)': 'inches',
                         'mb': 'milibar',
                         'mb(p)': 'milibars',
                         'm': 'meter',
                         'm(p)': 'meters',
                        }

    # @brief Emite el reporte extendido del clima a 5 dias
    # @requires Conexion a internet
    # @returns Temperatura, presion, humedad y viento para los proximos 5 dias en una determinada cuidad
    def requestWeatherAPI(self):
        API_URL = 'http://api.meteored.com.ar/index.php?api_lang=en&localidad=16884&affiliate_id=4s8w6nd9wumv&v=3.0'

        self.weatherForecast = requests.get(API_URL).json()
        self.cityName = self.weatherForecast['location'][0:12]
        self.units = self.weatherForecast['day']['1']['units']

    def calculateHourIndex(self, hour):

        index = None

        if hour == 'now':
            index = datetime.datetime.now().hour//3
        else:
            index = int(hour)//3

        return index

    def getPluralOrSingularUnit(self, number, unit):

        if number != 1:
            unit += '(p)'

        return unit

    def getTimeString(self, day, hour = None):

        timeStr = None

        if not hour == 'now':

            if day == '1':
                timeStr = 'today'
            elif day == '2':
                timeStr = 'tomorrow'
            else:
                timeStr = f'on {self.weatherForecast["day"][day]["name"]}'

            if hour != None:
                timeStr += ' at {hour} o\'clock'

        else:
            timeStr = hour

        return timeStr

    def getTemperature(self, day = '1', hour = 'now'):

        temperature = int(self.weatherForecast['day'][day]['hour'][self.calculateHourIndex(hour)]['temp'])

        temperatureUnit = self.strUnits[self.getPluraOrSingularUnit(temperature, self.units['temp'])]

        temperatueStr = f'For {self.cityName}, {self.getTimeString(day, hour)}, the temperature is {temperature} {temperatureUnit}.'

        return temperatureStr

    def getMaxMinTemperature(self, day = '1'):

        minTemp = int(self.weatherForecast['day'][day]['tempmin'])
        maxTemp = int(self.weatherForecast['day'][day]['tempmax'])

        minTempUnit = self.strUnits[self.getPluraOrSingularUnit(minTemp, self.units['temp'])]
        maxTempUnit = self.strUnits[self.getPluraOrSingularUnit(maxTemp, self.units['temp'])]

        minMaxTempStr = f'For {self.cityName}, {self.getTimeString(day)}, the minimum temperature is {minTemp} {minTempUnit} and the maximum temperature is {maxTemp} {maxTempUnit}.'

        return minMaxTempStr

    def getWindData(self, day = '1', hour = 'now'):

        windSpeed, windGusts = None

        if hour == None:
            windSpeed = self.weatherForecast['day'][day]['wind']['speed']
            windGusts = self.weatherForecast['day'][day]['wind']['gusts']
        else:
            windSpeed = self.weatherForecast['day'][day]['hour'][self.calculateHourIndex(hour)]['wind']['speed']
            windGusts = self.weatherForecast['day'][day]['hour'][self.calculateHourIndex(hour)]['wind']['gusts']

        windSpeedUnit = self.strUnits[self.getPluralOrSingularUnit(windSpeed, self.units['wind'])]
        windGustsUnit = self.strUnits[self.getPluralOrSingularUnit(windGusts, self.units['wind'])]

        windStr = f'For {self.cityName}, {self.getTimeString(day)}, the wind avarage speed is {windSpeed} {windSpeedUnit} and there are gusts of {windGusts} {windGustsUnit}.'

        return windStr

    def getRain(self, day = '1', hour = 'now'):

        rain = None

        if hour == None:
            rain = self.weatherForecast['day'][day]['rain']
        else:
            rain = self.weatherForecast['day'][day]['hour'][self.calculateHourIndex(hour)]['rain']

        rainUnit = self.strUnits[self.getPluralOrSingularUnit(rain, self.units['rain'])]

        rainStr = f'For {self.cityName}, {self.getTimeString(day)}, the rain level is {rain} {rainUnit}.'

        return rainStr

    def getPressure(self, day = '1', hour = 'now'):

        pressure = None

        if hour == None:
            pressure = self.weatherForecast['day'][day]['pressure']
        else:
            pressure = self.weatherForecast['day'][day]['hour'][self.calculateHourIndex(hour)]['pressure']

        pressureUnit = self.strUnits[self.getPluralOrSingularUnit(pressure, self.units['pressure'])]

        pressureStr = f'For {self.cityName}, {self.getTimeString(day)}, the pressure is {pressure} {pressureUnit}'

        return pressureStr

    def getHumidity(self, day = '1', hour = 'now'):
        pass

engine = mimic.mimic()
#engine.say()

weather = Weather()

print(json.dumps(weather.weatherForecast, indent=4))

#print(weather.units)
