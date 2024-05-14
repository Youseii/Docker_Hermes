from flask import Flask, render_template, request
import WazeRouteCalculator
import logging
import requests
import datetime
import creds

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def informations():
    try:
        if request.method == 'POST':
            from_address = request.form.get('from_address')
            to_address = request.form.get('to_address')
            city = request.form.get('city')
        else:
            from_address = 'Place de la Gare, 1, Grenoble, France'
            to_address = 'Cours de Verdun-Gensoul, 14, Lyon, Rhône, France'
            city = "Paris"

    except:
            from_address = 'Place de la Gare, 1, Grenoble, France'
            to_address = 'Cours de Verdun-Gensoul, 14, Lyon, Rhône, France'
            city = "Paris"

    # Logging setup for WazeRouteCalculator
    logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    logger.addHandler(handler)

    region = 'EU'
    vehicle_type = ''
    route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region, vehicle_type)

    time, distance = route.calc_route_info()

    # Weather API call
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    key = creds.api_key
    
    url = base_url + "appid=" + key + "&q=" + city
    rep = requests.get(url).json()

    def kel_to_celsuis(kelvin):
        celsuis = kelvin - 273.15
        fahrenheit = celsuis * (9/5) + 32
        return celsuis, fahrenheit

    temperature_kel = rep['main']['temp']
    temp_celsuis, temps_far = kel_to_celsuis(temperature_kel)
    feel_like_kel = rep['main']['feels_like']
    feel_like_celsuis, feel_like_far = kel_to_celsuis(feel_like_kel)
    wind_speed = rep['wind']['speed']
    humidity = rep['main']['humidity']
    description = rep['weather'][0]['description']
    sunrise_time = datetime.datetime.utcfromtimestamp(rep['sys']['sunrise'] + rep['timezone'])
    sunset_time = datetime.datetime.utcfromtimestamp(rep['sys']['sunset'] + rep['timezone'])

    # Construire le dictionnaire data avec toutes les informations nécessaires
    data = {
        'From': from_address,
        'To': to_address,
        'time': f'{time} minutes',
        'distance': f'{distance} km',
        'city': city,
        'temp_celsuis': f'{temp_celsuis:.2f}°C',
        'temps_far': f'{temps_far:.2f}°F',
        'feel_like_celsuis': f'{feel_like_celsuis:.2f}°C',
        'feel_like_far': f'{feel_like_far:.2f}°F',
        'humidity': f'{humidity}%',
        'wind_speed': f'{wind_speed} m/s',
        'description': description,
        'sunrise_time': sunrise_time,
        'sunset_time': sunset_time
    }

    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
