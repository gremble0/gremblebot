import random
import discord
import secrets
from pytube import YouTube
from googleapiclient.discovery import build

async def handle_command(client, message):
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

		#YouTube("https://youtu.be/"+response["items"][0]["id"]["videoId"], use_oauth=True).streams.get_highest_resolution().download() # download first video in http response
		for video in response["items"]: # !! very slow !!
			video_id = video["id"]["videoId"]
			YouTube("https://youtu.be/"+video_id, use_oauth=True).streams.get_highest_resolution().download()

		return "asd"
