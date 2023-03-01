from pytube import YouTube
import discord
import os

class Playlist:
	def __init__(self, client):
		self.queue = []
		self.client = client

	def pop(self):
		self.queue.pop(0)
	
	def insert(self, yt):
		self.queue.append(yt)

	def play(self):
		yt_obj = self.queue[0]
		stream = yt_obj.streams.get_lowest_resolution()
		video_title = stream.download(output_path="media/")
		#os.rename(video_title, video_title + ".mp3")
		
		return discord.file(open(video_title, "rb"))
