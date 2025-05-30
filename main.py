import os
import requests
from github_data import check_github_json
from dotenv import load_dotenv
load_dotenv()

def get_noon_weather_summaries(city):
	api_key = str(os.getenv('OPEN_WEATHER_MAP_API_KEY'))
	url = "https://api.openweathermap.org/data/2.5/forecast"
	params = {"q": city, "appid": api_key, "units": "metric"}
	response = requests.get(url, params=params)

	if response.status_code != 200:
		print(f"Error {response.status_code}: {response.text}")
		return

	data = response.json()
	summaries = []

	for entry in data["list"]:
		if "12:00:00" in entry["dt_txt"]:
			main = entry["weather"][0]["main"]
			description = entry["weather"][0]["description"]

			if "rain" in description.lower() or "rain" in main.lower() or "rain" in entry:
				date = entry["dt_txt"].split(" ")[0]
				summaries.append({
					"Date": date,
					"Weather Description": description
				})

	if summaries:
		check_github_json(summaries)
	else:
		check_github_json(None)

	
if __name__ == "__main__":
	get_noon_weather_summaries("London")