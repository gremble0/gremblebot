"""File for handling user input/commands"""
import ctypes
from pytube import Search
import discord

async def handle_command(message, playlist):
    """Handles commands and returns string to be sent in text channel"""
    message_split = message.content.split()

    if message_split[0] == "!ping":
        return "pong!"

    if message_split[0] == "!play":
        discord.opus.load_opus(ctypes.util.find_library("opus"))
        if len(message_split) < 2:
            return "Please enter a video title"
        if len(playlist.queue) >= 10:
            return "Queue full"

        # yt_obj contains first YouTube object in SearchQuery object
        yt_obj = Search(" ".join(message_split[1:])).results[0]
        playlist.insert(yt_obj)
        stream = yt_obj.streams.get_lowest_resolution() # get_audio_only() doesnt work
        video_title = stream.download(output_path="media/")

        #source = discord.FFmpegAudio(j
        source = discord.PCMAudio(open(video_title, "rb"))
        #source = await discord.FFmpegOpusAudio.from_probe(video_title, method="fallback")
        voice_client = await message.author.voice.channel.connect()
        voice_client.play(source)

        return f"Added {yt_obj.title} to the queue."
