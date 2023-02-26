import random
import discord
import secrets
from pytube import YouTube
from googleapiclient.discovery import build

def handle_command(client, message):
	#voice_client = discord.VoiceClient(client, message.channel)

	if message.content == "!ping":
		return "pong!"
	
	if message.content == "!play":
		youtube_client = build("youtube", "v3", developerKey=secrets.YOUTUBE_API_KEY)
		request = youtube_client.search().list(
			part = "snippet",
			q = "eminem lose yourself"
		)
		response = request.execute()

		for video in response["items"]:
			video_id = video["id"]["videoId"]
			#print(video_id)
			yt = YouTube("https://youtu.be/9bZkp7q19f0")
			yt.streams.get_audio_only().download()
			#YouTube("https://youtu.be/"+video_id).streams.get_audio_only().download()

		return "asd"
