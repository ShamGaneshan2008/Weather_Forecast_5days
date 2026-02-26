import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise EnvironmentError("OPENWEATHER_API_KEY not set. Add it to your .env file.")

BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"


def get_data(place: str, forecast_days: int = 5) -> list[dict]:
    """
    Fetch weather forecast data for a given place.

    Args:
        place: City name to fetch weather for
        forecast_days: Number of days to forecast (1-5)

    Returns:
        List of forecast entries (8 per day from OpenWeatherMap)

    Raises:
        ValueError: If the city is not found or API returns an error
        ConnectionError: If the API request fails
    """
    if not place or not place.strip():
        raise ValueError("City name cannot be empty.")

    forecast_days = max(1, min(5, forecast_days))

    try:
        response = requests.get(
            BASE_URL,
            params={"q": place, "appid": API_KEY, "units": "metric"},
            timeout=10,
        )
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to connect to weather service: {e}") from e

    if response.status_code == 404:
        raise ValueError(f'City "{place}" not found. Please check the spelling and try again.')
    elif response.status_code == 401:
        raise ValueError("Invalid API key. Please check your configuration.")
    elif response.status_code != 200:
        raise ValueError(f"Weather API error (status {response.status_code}). Please try again later.")

    data = response.json()
    entries = data.get("list", [])

    if not entries:
        raise ValueError("No forecast data available for this location.")

    return entries[: 8 * forecast_days]


if __name__ == "__main__":
    results = get_data("Amsterdam", forecast_days=2)
    for r in results[:3]:
        print(r["dt_txt"], r["main"]["temp"], r["weather"][0]["main"])
