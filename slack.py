import os
from slack_sdk import WebClient
from dotenv import load_dotenv
load_dotenv()

SLACK_BOT_TOKEN = str(os.getenv('SLACK_BOT_USER_TOKEN'))
client = WebClient(token=SLACK_BOT_TOKEN)

channel = "C0211DW58JD"
text_to_send = f"Test hello"

client.conversations_join(channel=channel)
client.chat_postMessage(channel=channel, text=text_to_send)

