"""Single purpose file for playlist class"""
import discord
#import os

class Playlist:
    """Class for keeping track of songs queued by !play command"""
    def __init__(self, client) -> None:
        self.queue = []
        self.client = client

    def pop(self) -> None:
        """Removes song from start of queue"""
        self.queue.pop(0)

    def insert(self, yt_obj) -> None:
        """Append song to end of queue"""
        self.queue.append(yt_obj)

    async def play(self):
        """Download and return discord audio object of first song in queue"""
        yt_obj = self.queue[0]
        stream = yt_obj.streams.get_lowest_resolution() # get_audio_only() doesnt work
        video_title = stream.download(output_path="media/")
        #os.rename(video_title, video_title + ".mp3")
        source = await discord.FFmpegOpusAudio.from_probe(source=video_title)
        return source
        #return discord.File(open(video_title, "rb"))
        #return discord.FFmpegPCMAudio(video_title).read()
        #return discord.File(open(video_title, "rb"))
