import os
import requests
from dotenv import load_dotenv
load_dotenv()

def get_noon_weather_summaries(city):
	api_key = str(os.getenv('OPEN_WEATHER_MAP_API_KEY'))
	url = "https://api.openweathermap.org/data/2.5/forecast"
	params = {"q": city, "appid": api_key, "units": "metric"}
	response = requests.get(url, params=params)

	if response.status_code != 200:
		print(f"Error {response.status_code}: {response.text}")
		return None

	data = response.json()
	summaries = []
	for entry in data["list"]:
		if "12:00:00" in entry["dt_txt"]:
			main = entry["weather"][0]["main"]
			has_rain_field = "rain" in entry
			description = entry["weather"][0]["description"]
			date = entry["dt_txt"].split(" ")[0]

			if main.lower() == "rain" or has_rain_field:
				summaries.append({ "Date": date, "Weather Description": description })
				
	# run github func here with summaries list as param (must be scope outside for loop)
	print("Summaries", summaries)
	return summaries
	
if __name__ == "__main__":
	get_noon_weather_summaries("London")