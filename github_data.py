import os
import logging
import json
from github import Github
from slack import create_slack_message
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()
logger = logging.getLogger(__name__)

def load_github_json():
	GITHUB_PERSONAL_ACCESS_TOKEN = str(os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN'))
	github = Github(GITHUB_PERSONAL_ACCESS_TOKEN)	
	try:
		repo = github.get_user().get_repo('weather-data')
		file = repo.get_contents("json/data.json")
		db_data = json.loads(file.decoded_content.decode('utf-8'))	
		return repo, file, db_data
	except Exception as e:
		logger.exception("An error occurred")


def check_github_json(forecast):

	# forecast = [{"Date": "2025-06-04", "Weather Description": "heavy rain"}]

	if forecast is None:
		create_slack_message("No rain expected in the next 5 days.")
		return

	repo, file, db_data = load_github_json()
	new_items = []
	is_first_run = len(db_data) == 0

	for item in forecast:
		if item not in db_data:
			print("Make JSON DB entry")
			db_data.append(item)
			new_items.append(item)
		else:
			print("Skip, found in DB")

	if new_items:
		if is_first_run:
			update_github_json(repo, file, db_data, slack_items=new_items)
		else:
			update_github_json(repo, file, db_data, slack_items=[new_items[-1]])
	else:
		print("No new items to commit")



def update_github_json(repo, file, updated_data, slack_items):
	bytes_data = json.dumps(updated_data).encode('utf-8')
	commit_msg = datetime.now(timezone.utc).strftime("Update weather data - %Y-%m-%d %H:%M:%S UTC")
	try:
		repo.update_file(file.path, commit_msg, bytes_data, file.sha)
		print("Github data updated!")
		create_slack_message(slack_items)
	except Exception as e:
		logger.exception("An error occurred")
