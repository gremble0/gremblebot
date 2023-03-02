"""Single purpose file for handling commands"""
from pytube import Search

async def handle_command(message, playlist):
    """Handles commands and returns string to be sent in text channel"""
    message_split = message.content.split()

    if message_split[0] == "!ping":
        return "pong!"

    if message_split[0] == "!play":
        if len(message_split) < 2:
            return "Please enter a video title"
        if len(playlist.queue) >= 10:
            return "Queue full"

        # yt_obj contains first YouTube object in SearchQuery object
        yt_obj = Search(" ".join(message_split[1:])).results[0]
        playlist.insert(yt_obj)

        await message.author.voice.channel.connect()
        message.channel.send(playlist.play())

        return f"Added {yt_obj.title} to the queue."
