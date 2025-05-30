import os
from slack_sdk import WebClient
from dotenv import load_dotenv
load_dotenv()

def create_slack_message(items):
	SLACK_BOT_TOKEN = str(os.getenv('SLACK_BOT_USER_TOKEN'))
	client = WebClient(token=SLACK_BOT_TOKEN)
	channel = "C0211DW58JD"

	if isinstance(items, str):
		text_to_send = items
	else:
		message_lines = [f"- {item['Date']}: {item['Weather Description']}" for item in items]
		text_to_send = "New rain alert(s):\n" + "\n".join(message_lines)

	try:
		client.conversations_join(channel=channel)
	except Exception:
		pass

	client.chat_postMessage(channel=channel, text=text_to_send)
