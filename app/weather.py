import requests
from datetime import datetime


def get_weather(lat, lon):
    endpoint = "https://api.open-meteo.com/v1/forecast"
    parameters = {
        "latitude": lat,
        "longitude": lon,
        # "hourly": "temperature_2m,precipitation",
        # "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation", "rain",
                    "weather_code", "cloud_cover", "surface_pressure", "wind_speed_10m"],
        # "past_days": 3,
        "timezone": "auto",
    }
    try:
        response = requests.get(endpoint, params=parameters)
        response.raise_for_status()
        response_data = response.json()
        print("RESPONSE:", response_data)
        return response_data
    except requests.RequestException as e:
        print(f"Error fetching hourly weather data: {e}")
        return None
    except ValueError as e:
        print(f"Error processing hourly weather data: {e}")
        return None


def convert_hourly_to_datetime(time_string: str) -> datetime:
    try:
        date = datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        date = datetime.strptime(time_string, '%Y-%m-%dT%H:%M')
    return date


def hourly_weather(weather_data):
    print("Hourly Weather Data:")
    if 'hourly' in weather_data:
        times = weather_data['hourly']['time']
        temperatures = weather_data['hourly']['temperature_2m']
        precipitations = weather_data['hourly']['precipitation']
        for time, temp, precip in zip(times, temperatures, precipitations):
            print(f"Time: {convert_hourly_to_datetime(time)}, Temperature: {temp}°C, Precipitation: {precip}mm")
    else:
        print("  No hourly data available.")


def daily_weather(weather_data):
    print("Daily Weather Data:")
    if 'daily' in weather_data:
        # print(data['daily'])
        days = weather_data['daily']['time']
        minimums = weather_data['daily']['temperature_2m_min']
        maximums = weather_data['daily']['temperature_2m_max']
        for day, min_of_the_day, max_of_the_day in zip(days, minimums, maximums):
            print(f"Day: {day}, Min: {min_of_the_day}, Max: {max_of_the_day}")
    else:
        print("  No hourly data available.")


weather_codes = {
    0: {'description': 'Clear sky', 'icon': 'fa-sun'},
    1: {'description': 'Mainly clear', 'icon': 'fa-cloud-sun'},
    2: {'description': 'Partly cloudy', 'icon': 'fa-cloud-sun'},
    3: {'description': 'Overcast', 'icon': 'fa-cloud-meatball'},
    45: {'description': 'Fog and depositing rime fog', 'icon': 'fa-smog'},
    48: {'description': 'Fog and depositing rime fog', 'icon': 'fa-smog'},
    51: {'description': 'Drizzle: Light', 'icon': 'fa-cloud-drizzle'},
    53: {'description': 'Drizzle: Moderate', 'icon': 'fa-cloud-drizzle'},
    55: {'description': 'Drizzle: Dense intensity', 'icon': 'fa-cloud-showers-heavy'},
    56: {'description': 'Freezing Drizzle: Light', 'icon': 'fa-cloud-showers-heavy'},
    57: {'description': 'Freezing Drizzle: Dense intensity', 'icon': 'fa-cloud-showers-heavy'},
    61: {'description': 'Rain: Slight', 'icon': 'fa-cloud-rain'},
    63: {'description': 'Rain: Moderate', 'icon': 'fa-cloud-rain'},
    65: {'description': 'Rain: Heavy intensity', 'icon': 'fa-cloud-showers-heavy'},
    66: {'description': 'Freezing Rain: Light', 'icon': 'fa-cloud-showers-heavy'},
    67: {'description': 'Freezing Rain: Heavy intensity', 'icon': 'fa-cloud-showers-heavy'},
    71: {'description': 'Snowfall: Slight', 'icon': 'fa-snowflake'},
    73: {'description': 'Snowfall: Moderate', 'icon': 'fa-snowflake'},
    75: {'description': 'Snowfall: Heavy intensity', 'icon': 'fa-snowflake'},
    77: {'description': 'Snow grains', 'icon': 'fa-snowflakes'},
    80: {'description': 'Rain showers: Slight', 'icon': 'fa-cloud-showers-heavy'},
    81: {'description': 'Rain showers: Moderate', 'icon': 'fa-cloud-showers-heavy'},
    82: {'description': 'Rain showers: Violent', 'icon': 'fa-cloud-showers-heavy'},
    85: {'description': 'Snow showers: Slight', 'icon': 'fa-snowflakes'},
    86: {'description': 'Snow showers: Heavy', 'icon': 'fa-snowflakes'},
    95: {'description': 'Thunderstorm: Slight or moderate', 'icon': 'fa-bolt'},
    96: {'description': 'Thunderstorm with slight hail', 'icon': 'fa-bolt'},
    99: {'description': 'Thunderstorm with heavy hail', 'icon': 'fa-bolt'}
}


def current_weather(weather_data):
    if 'current' in weather_data:
        #  "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation", "rain", "weather_code", "cloud_cover", "surface_pressure", "wind_speed_10m"],
        time = convert_hourly_to_datetime(weather_data['current']['time'])
        temperature = weather_data['current']['temperature_2m']
        humidity = weather_data['current']['relative_humidity_2m']
        apparent_temperature = weather_data['current']['apparent_temperature']
        precipitation = weather_data['current']['precipitation']
        rain = weather_data['current']['rain']
        weather_code = weather_data['current']['weather_code']
        weather_code_desc = weather_codes[weather_code]['description']
        weather_code_icon = weather_codes[weather_code]['icon']
        cloud_cover = weather_data['current']['cloud_cover']
        surface_pressure = weather_data['current']['surface_pressure']
        wind_speed = weather_data['current']['wind_speed_10m']

        return {
            "time": time,
            "temperature": temperature,
            "humidity": humidity,
            'apparent_temperature': apparent_temperature,
            "precipitation": precipitation,
            "rain": rain,
            "weather_code": weather_code,
            "cloud_cover": cloud_cover,
            "surface_pressure": surface_pressure,
            'wind_speed': wind_speed,
            'weather_code_desc': weather_code_desc,
            'weather_code_icon': weather_code_icon,
        }
    else:
        print("No current data available.")

# if __name__ == "__main__":
#     # get_weather(54.352050, 18.646370)
#     data = get_weather(54.352050, 18.646370)
#     # hourly_weather(data)
#     # daily_weather(data)
#     current_weather(data)
