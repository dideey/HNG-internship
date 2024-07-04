from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')
    print(f"Visitor name: {visitor_name}")
    
    # Get client IP address
    client_ip = request.remote_addr
    print(f"Client IP: {client_ip}")
    
    # Get location and temperature based on IP
    try:
        location, temperature = get_location_and_temperature(client_ip)
        print(f"Location: {location}, Temperature: {temperature}")
    except Exception as e:
        print(f"Error getting location and temperature: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    response = {
        "client_ip": client_ip,
        "location": location,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"
    }
    return jsonify(response)

def get_location_and_temperature(ip):
    try:
        # Use an IP geolocation API (like ipinfo.io)
        ip_info_response = requests.get(f'https://ipinfo.io/{ip}?token=9be2f128220c66')
        ip_info_response.raise_for_status()
        ip_info = ip_info_response.json()
        location = ip_info.get('city', 'Unknown')
        print(f"IP Info: {ip_info}")
        
        # Use a weather API to get the temperature (like OpenWeatherMap)
        weather_api_key = 'c1a78f129e8e837456d9d81cc364db09'
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric'
        weather_info = requests.get(weather_url).json()
        print(f"Weather Info: {weather_info}")
        
        if 'main' in weather_info:
            temperature = weather_info['main']['temp']
        else:
            print("Error: 'main' key not found in weather_info response.")
            temperature = 'Unknown'
    except Exception as e:
        print(f"An error occurred: {e}")
        location = 'Unknown'
        temperature = 'Unknown'

    return location, temperature

if __name__ == '__main__':
    app.run(debug=True)
