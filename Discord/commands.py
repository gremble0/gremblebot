import random
import discord
from pytube import YouTube, Search

async def handle_command(client, message, playlist):
	message_split = message.content.split()

	if message_split[0] == "!ping":
		return "pong!"
	
	if message_split[0] == "!play":
		if len(message_split) < 2:
			return "Please enter a video title"
		if len(playlist.queue) >= 10:
			return "Queue full"

		yt = Search(" ".join(message_split[1:])).results[0] # returns first YouTube object in SearchQuery object
		playlist.insert(yt)

		await message.author.voice.channel.connect()
		message.channel.send(playlist.play())

		return f"Added {yt.title} to the queue."
