from fastmcp import FastMCP
import requests

# Create the MCP server instance.
# This server exposes weather-related tools to MCP-compatible clients.
mcp = FastMCP("Weather Server")

# Open-Meteo API endpoints.
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# Open-Meteo weather codes mapped to human-readable descriptions.
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Frost mist",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light and freezing rain",
    67: "Heavy and freezing rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Light and mixed rain",
    81: "Moderate and mixed rain",
    82: "Heavy and mixed rain",
    85: "Light and mixed snow",
    86: "Heavy and mixed snow",
    95: "Thunderstorm",
    96: "Thunderstorm with light hail",
    99: "Thunderstorm with heavy hail",
}


def geocode_city(city: str) -> dict:
    """
    Resolve a city name into geographic coordinates using the
    Open-Meteo geocoding API.

    Args:
        city: The name of the city to look up.

    Returns:
        A dictionary with the resolved name, country, latitude and
        longitude.

    Raises:
        ValueError: If no matching city is found.
    """

    # Send a request to the geocoding API to resolve the city name.
    response = requests.get(
        GEOCODING_URL,
        params={"name": city, "count": 1, "language": "en", "format": "json"},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    # The API returns a list of matching locations.
    results = data.get("results")
    if not results:
        raise ValueError(f"City not found: {city}")

    # Keep only the best matching result.
    match = results[0]
    return {
        "name": match["name"],
        "country": match.get("country", ""),
        "latitude": match["latitude"],
        "longitude": match["longitude"],
    }


def fetch_forecast(latitude: float, longitude: float) -> dict:
    """
    Fetch the current weather and today's forecast for a given
    location using the Open-Meteo forecast API.

    Args:
        latitude: Latitude of the location.
        longitude: Longitude of the location.

    Returns:
        The raw JSON payload returned by the Open-Meteo API.
    """

    # Request both the current weather and today's daily forecast.
    response = requests.get(
        FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
            "daily": "temperature_2m_max,temperature_2m_min,weather_code",
            "timezone": "auto",
            "forecast_days": 1,
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


@mcp.tool()
def get_current_weather(city: str) -> str:
    """
    Get the current weather for a given city.

    Args:
        city (str): The name of the city (e.g. "London", "New York").

    Returns:
        str: A human-readable summary of the current weather.
    """

    try:
        # Convert the city name into geographic coordinates,
        # then fetch the weather forecast.
        location = geocode_city(city)
        forecast = fetch_forecast(location["latitude"], location["longitude"])
    except ValueError as e:
        return str(e)
    except requests.RequestException as e:
        return f"Error connecting to weather API: {e}"

    # Extract the current weather information.
    current = forecast["current"]
    condition = WEATHER_CODES.get(current["weather_code"], "Unknown conditions")

    return (
        f"Current weather in {location['name']}, {location['country']} :\n"
        f"- Condition: {condition}\n"
        f"- Temperature: {current['temperature_2m']} °C\n"
        f"- Humidity: {current['relative_humidity_2m']} %\n"
        f"- Wind: {current['wind_speed_10m']} km/h"
    )


@mcp.tool()
def get_daily_forecast(city: str) -> str:
    """
    Get today's min/max temperature forecast for a given city.

    Args:
        city (str): The name of the city (e.g. "London", "New York").

    Returns:
        str: A human-readable summary of today's forecast.
    """

    try:
        # Resolve the city location before requesting the forecast.
        location = geocode_city(city)
        forecast = fetch_forecast(location["latitude"], location["longitude"])
    except ValueError as e:
        return str(e)
    except requests.RequestException as e:
        return f"Error connecting to weather API: {e}"

    # Extract today's forecast values.
    daily = forecast["daily"]
    condition = WEATHER_CODES.get(daily["weather_code"][0], "Unknown conditions")

    return (
        f"Daily forecast for {location['name']}, {location['country']} :\n"
        f"- Condition: {condition}\n"
        f"- Max Temp: {daily['temperature_2m_max'][0]} °C\n"
        f"- Min Temp: {daily['temperature_2m_min'][0]} °C"
    )


# Run the MCP server when this script is executed directly.
# The server listens for incoming MCP requests from compatible clients.
if __name__ == "__main__":
    mcp.run()