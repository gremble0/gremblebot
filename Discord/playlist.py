"""Single purpose file for playlist class"""
import discord
#import os

class Playlist:
    """Class for keeping track of songs queued by !play command"""
    def __init__(self, client):
        self.queue = []
        self.client = client

    def pop(self):
        """Removes song from start of queue"""
        self.queue.pop(0)

    def insert(self, yt_obj):
        """Append song to end of queue"""
        self.queue.append(yt_obj)

    def play(self):
        """Download and return discord file object of first song in queue"""
        yt_obj = self.queue[0]
        stream = yt_obj.streams.get_lowest_resolution()
        video_title = stream.download(output_path="media/")
        #os.rename(video_title, video_title + ".mp3")

        return discord.File(open(video_title, "rb"))
