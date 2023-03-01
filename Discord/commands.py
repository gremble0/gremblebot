import random
import discord
import secrets
from pytube import YouTube, Search
from googleapiclient.discovery import build

async def handle_command(client, message):
	#voice_client = discord.VoiceClient(client, message.channel)
	message_split = message.content.split()

	if message_split[0] == "!ping":
		return "pong!"
	
	if message_split[0] == "!play":
		if len(message_split) < 2:
			return "Please enter a video title"

		yt = Search(" ".join(message_split[1:])).results
		yt[0].streams.get_audio_only().download(output_path="media/")

		return "asd"
