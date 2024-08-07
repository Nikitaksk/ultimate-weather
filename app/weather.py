import requests
from datetime import datetime

weather_codes = {
    0: {'description': 'Clear sky', 'icon': 'fa-sun has-text-warning'},
    1: {'description': 'Mainly clear', 'icon': 'fa-cloud-sun has-text-success '},
    2: {'description': 'Partly cloudy', 'icon': 'fa-cloud-sun has-text-success'},
    3: {'description': 'Overcast', 'icon': 'fa-cloud-meatball has-text-dark'},
    45: {'description': 'Fog and depositing rime fog', 'icon': 'fa-smog has-text-dark'},
    48: {'description': 'Fog and depositing rime fog', 'icon': 'fa-smog has-text-dark'},
    51: {'description': 'Drizzle: Light', 'icon': 'fa-cloud-drizzle has-text-link'},
    53: {'description': 'Drizzle: Moderate', 'icon': 'fa-cloud-drizzle has-text-link'},
    55: {'description': 'Drizzle: Dense intensity', 'icon': 'fa-cloud-showers-heavy has-text-info'},
    56: {'description': 'Freezing Drizzle: Light', 'icon': 'fa-cloud-showers-heavy has-text-info'},
    57: {'description': 'Freezing Drizzle: Dense intensity', 'icon': 'fa-cloud-showers-heavy has-text-info'},
    61: {'description': 'Rain: Slight', 'icon': 'fa-cloud-rain has-text-info'},
    63: {'description': 'Rain: Moderate', 'icon': 'fa-cloud-rain has-text-info'},
    65: {'description': 'Rain: Heavy intensity', 'icon': 'fa-cloud-showers-heavy has-text-danger'},
    66: {'description': 'Freezing Rain: Light', 'icon': 'fa-cloud-showers-heavy has-text-danger'},
    67: {'description': 'Freezing Rain: Heavy intensity', 'icon': 'fa-cloud-showers-heavy has-text-danger'},
    71: {'description': 'Snowfall: Slight', 'icon': 'fa-snowflake has-text-info'},
    73: {'description': 'Snowfall: Moderate', 'icon': 'fa-snowflake has-text-info'},
    75: {'description': 'Snowfall: Heavy intensity', 'icon': 'fa-snowflake has-text-info'},
    77: {'description': 'Snow grains', 'icon': 'fa-snowflakes has-text-info'},
    80: {'description': 'Rain showers: Slight', 'icon': 'fa-cloud-showers-heavy has-text-danger'},
    81: {'description': 'Rain showers: Moderate', 'icon': 'fa-cloud-showers-heavy has-text-danger'},
    82: {'description': 'Rain showers: Violent', 'icon': 'fa-cloud-showers-heavy has-text-danger'},
    85: {'description': 'Snow showers: Slight', 'icon': 'fa-snowflakes has-text-info'},
    86: {'description': 'Snow showers: Heavy', 'icon': 'fa-snowflakes has-text-info'},
    95: {'description': 'Thunderstorm: Slight or moderate', 'icon': 'fa-bolt has-text-danger'},
    96: {'description': 'Thunderstorm with slight hail', 'icon': 'fa-bolt has-text-danger'},
    99: {'description': 'Thunderstorm with heavy hail', 'icon': 'fa-bolt has-text-danger'}
}

past_days = 2


def get_weather(lat, lon):
    endpoint = "https://api.open-meteo.com/v1/forecast"
    parameters = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "precipitation_probability", "weather_code"],
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation", "rain",
                    "weather_code", "cloud_cover", "surface_pressure", "wind_speed_10m"],
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "precipitation_sum",
                  "precipitation_hours", "precipitation_probability_max"],
        "timezone": "auto",
        "past_days": past_days,
    }
    try:
        response = requests.get(endpoint, params=parameters)
        response.raise_for_status()
        response_data = response.json()
        return response_data
    except requests.RequestException as e:
        print(f"Error fetching hourly weather data: {e}")
        return None
    except ValueError as e:
        print(f"Error processing hourly weather data: {e}")
        return None


def convert_hourly_to_datetime_bulk(hourly_data):
    arr = []
    for hour in hourly_data:
        arr.append(convert_hourly_to_datetime(hour).strftime("%H"))
    return arr

def convert_daily_to_datetime_bulk(daily_data):
    arr = []
    for day in daily_data:
        arr.append(datetime.strptime(day, "%Y-%m-%d").strftime("%d %b"))
    return arr


def convert_hourly_to_datetime(time_string: str) -> datetime:
    try:
        date = datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        date = datetime.strptime(time_string, '%Y-%m-%dT%H:%M')
    return date


def hourly_weather(weather_data):
    amount_of_hours = 24
    if 'hourly' in weather_data:
        timestamp_start = past_days * 24
        timestamp_end = timestamp_start + amount_of_hours
        timestamps = convert_hourly_to_datetime_bulk(weather_data['hourly']['time'][timestamp_start: timestamp_end])
        temperatures = weather_data['hourly']['temperature_2m'][timestamp_start: timestamp_end]
        precipitations = weather_data['hourly']['precipitation_probability'][timestamp_start: timestamp_end]
        weather_codes_info = weather_data['hourly']['weather_code'][timestamp_start: timestamp_end]
        weather_codes_desc = [weather_codes[i]['description'] for i in weather_codes_info]
        weather_codes_icon = [weather_codes[i]['icon'] for i in weather_codes_info]
        return {
            "hourly_data": zip(timestamps, temperatures, precipitations, weather_codes_desc, weather_codes_icon),
        }
    else:
        return None


def daily_weather(weather_data):
    if 'daily' in weather_data:
        timestamps = convert_daily_to_datetime_bulk(weather_data['daily']['time'])
        weather_codes_info = weather_data['daily']['weather_code']
        weather_codes_desc = []
        weather_codes_icon = []
        min_of_the_day = []
        max_of_the_day = []
        precipitation_hours = []
        sunrise = []
        sunset = []
        for i in range(len(timestamps)):
            weather_codes_desc.append(weather_codes[weather_codes_info[i]]['description'])
            weather_codes_icon.append(weather_codes[weather_codes_info[i]]['icon'])
            min_of_the_day.append(int(weather_data['daily']['temperature_2m_min'][i]))
            max_of_the_day.append(int(weather_data['daily']['temperature_2m_max'][i]))
            precipitation_hours.append(int(weather_data['daily']['precipitation_hours'][i]))
            sunrise.append(datetime.strptime(weather_data['daily']['sunrise'][i], "%Y-%m-%dT%H:%M").strftime("%H:%M"))
            sunset.append(datetime.strptime(weather_data['daily']['sunset'][i], "%Y-%m-%dT%H:%M").strftime("%H:%M"))


        precipitation_sum = weather_data['daily']['precipitation_sum']
        precipitation_probability = weather_data['daily']['precipitation_probability_max']
        return {
            "daily_data" : zip(timestamps[past_days:], weather_codes_icon[past_days:], weather_codes_desc[past_days:], min_of_the_day[past_days:], max_of_the_day[past_days:], sunrise[past_days:], sunset[past_days:], precipitation_sum[past_days:], precipitation_hours[past_days:], precipitation_probability[past_days:])
        }
    else:
        return None
        # print("  No hourly data available.")


def current_weather(weather_data):
    if 'current' in weather_data:
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
            "current_time": time,
            "current_temperature": temperature,
            "current_humidity": humidity,
            'current_apparent_temperature': apparent_temperature,
            "current_precipitation": precipitation,
            "current_rain": rain,
            "current_weather_code": weather_code,
            "current_cloud_cover": cloud_cover,
            "current_surface_pressure": surface_pressure,
            'current_wind_speed': wind_speed,
            'current_weather_code_desc': weather_code_desc,
            'current_weather_code_icon': weather_code_icon,
        }
    else:
        print("No current data available.")
