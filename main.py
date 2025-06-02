import os
import requests
from celery import Celery
from celery.schedules import crontab
from github_data import check_github_json
from dotenv import load_dotenv
load_dotenv()

app = Celery('main', broker='amqp://localhost')
app.conf.timezone = 'Europe/London'
app.conf.broker_pool_limit = 1
app.conf.beat_schedule = {
    'check-weather-every-30-seconds': {
        'task': 'main.weather_task',
        'schedule': crontab(hour=12, minute=0),
        'args': ('London',)
    },
}

@app.task(name='main.weather_task')
def weather_task(city):
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

# Commented-out code kept if you want to test code instantly without scheduler
# if __name__ == "__main__":
# 	weather_task("London")