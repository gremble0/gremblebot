"""File for handling user input/commands"""
import ctypes
import yt_dlp as youtube_dl
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

        video_url = search(" ".join(message_split[1:]))
        video_info = youtube_dl.YoutubeDL().extract_info(url = video_url, download= False)
        filename = f"{video_info['title']}.mp3"
        options = {
            "format": "bestaudio/best",
            "keepvideo": False,
            "outtmpl": filename
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info["webpage_url"]])

        source = await discord.FFmpegOpusAudio.from_probe(filename)
        voice_client = await message.author.voice.channel.connect()
        # try except ClientException for queueing??
        voice_client.play(source)

        return f"Added {filename} to the queue."

def search(arg) -> str:
    """Searches youtube for video based on arg. Returns string of video url"""
    ydl_options = {"format": "bestaudio", "noplaylist": "True"}
    ydl = youtube_dl.YoutubeDL(ydl_options)
    video = ydl.extract_info(f"ytsearch:{arg}", download=False)["entries"][0]
    return "youtube.com/watch?v=" + video["id"]
