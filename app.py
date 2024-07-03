from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])

def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')
    print(visitor_name)
    
    """clients ip adress"""
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if client_ip == '127.0.0.1':
        client_ip = 'YOUR_PUBLIC_IP_FOR_TESTING'
    
    # Get location and temperature based on IP
    location, temperature = get_location_and_temperature(client_ip)

    response = {
        "client_ip": client_ip,
        "location": location,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"
    }
    return jsonify(response)

def get_location_and_temperature(ip):
    # Use an IP geolocation API (like ipinfo.io)
    try:
        ip_info_response = requests.get(f'https://ipinfo.io/{ip}?token={os.getenv("IPINFO_API_KEY")}')
        ip_info = ip_info_response.json()
        location = ip_info.get('city', 'Unknown')
        
        # Use a weather API to get the temperature (like OpenWeatherMap)
        weather_api_key = os.getenv('OPENWEATHER_API_KEY')
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric'
        weather_info = requests.get(weather_url).json()
        print(weather_info)
        if 'main' in weather_info:
            temperature = weather_info['main']['temp']
        else:
            # Handle missing 'main' key
            print("Error: 'main' key not found in weather_info response.")
            temperature = 'Unknown'
    except Exception as e:
        print(f"An error occurred: {e}")
        location = 'Unknown'
        temperature = 'Unknown'

    return location, temperature
if __name__ == '__main__':
    app.run(debug=True)