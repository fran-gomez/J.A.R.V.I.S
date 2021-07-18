# -*- encoding: utf-8 -*-

import requests
import speak

# Referencia del JSON con los resultados en
# https://www.meteored.com.ar/documentacion_api/es/Metadata_latam.pdf

class Weather:
    
    # @brief Emite el reporte extendido del clima a 5 dias
    # @requires Conexion a internet
    # @returns Temperatura, presion, humedad y viento para los proximos 5 dias
    def get_forecast():
        API_URL = 'http://api.meteored.com.ar/index.php?api_lang=ar&localidad=16884&affiliate_id=4s8w6nd9wumv&v=3.0'

        response = requests.get(API_URL)

        return response
    
    # @brief Emite el reporte diario del clima
    # @requires Conexion a internet
    # @returns Temperatura, presion, humedad y viento para el dia de hoy
    def get_weather_report():
        API_URL = 'http://api.meteored.com.ar/index.php?api_lang=ar&localidad=16884&affiliate_id=4s8w6nd9wumv&v=3.0'

        response = requests.get(API_URL)

        city_name = response.json()['location'][0:12]
        today = response.json()['day']['1']['hour'][0]
        units = response.json()['day']['1']['units']

        temperature = f"It's around {today['temp']} degrees"
        pressure = f"The atmospheric pressure is {today['pressure']} hectopascals"
        humidity = f"And the humidity is {today['humidity']} percent."
        winds = f"The winds from {today['wind']['dir']} vary, with gusts of {today['wind']['gusts']} kilometers per hour"

        report = f"The weather for {city_name} today, {temperature}, {pressure}, {humidity} and {winds}"
        print(report)
        speak.speak(report)

        return report


Weather.get_weather_report()