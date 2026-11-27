import httpx
from fastapi import HTTPException, status


async def get_weather_summary(city: str):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    weather_url = "https://api.open-meteo.com/v1/forecast"

    async with httpx.AsyncClient(timeout=10.0) as client:
        # Get cords by name
        geo_params = {"name": city, "count": 1, "format":"json"}

        geo_res = await client.get(geo_url,params=geo_params)
        geo_res.raise_for_status()
        geo_data = geo_res.json()

        if not geo_data.get("results"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="City not found")

        location = geo_data["results"][0]
        lat,long = location["latitude"], location["longitude"]

        # Get info I actually need - average temp, rain probability (can change as need)
        weather_params = {
            "latitude": lat,
            "longitude": long,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "timezone": "auto",
            "forecast_days": 1,
        }
        weather_res = await client.get(weather_url, params=weather_params)
        weather_res.raise_for_status()

        daily = weather_res.json()["daily"]

        rain_chance = daily["precipitation_probability_max"][0]
        rain_chance = rain_chance if rain_chance is not None else 0

        return {
            "city": f"{location['name']}, {location.get('country', '')}",
            "temp_max_c": daily["temperature_2m_max"][0],
            "temp_min_c": daily["temperature_2m_min"][0],
            "rain_chance_percent": rain_chance ,
            "will_it_rain": rain_chance >= 40,
        }
        
# Response should look like this
# {
#   "city": "Berlin, Germany",
#   "temp_max_c": -0.9,
#   "temp_min_c": -1.9,
#   "rain_chance_percent": 0,
#   "will_it_rain": false
# }
