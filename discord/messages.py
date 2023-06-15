"""File for handling user input/commands"""
import ctypes
import yt_dlp
import discord
import os

class MessageHandler:
    """
    Class for handling user input containing all the bots commands

    Attributes
    ----------
    bot : Bot()
        pointer to Bot object running the program
        necessary for some commands
    message : discord.Message
        pointer to discord.Message variable containing
        information necessary for processing the current command
    playlists : { Int : [discord.FFmpegOpusAudio] }
        the int is the servers guild id (id unique for each server)
        dictionary of each servers queue of songs

    Methods
    -------
    handle_command():
        redirects to appropriate private method based on user input
    ping():
        sends ping to current chat channel
    stop():
        stops bot from running
    play():
        downloads and plays audio through voice client
    join():
        joins current audio channel
    leave():
        leaves current audio channel
    skip():
        skips song currently playing
    """

    def __init__(self, voice_client):
        self.voice_client = voice_client
        self.playlists = {}

    async def handle_message(self, message):
        """
        Starts coroutine for private method based on the
        content of the message variable
        """

        message_split = message.content.split()
        if message_split[0] == "%ping":
            return await self.ping(message)
        elif message_split[0] == "%stop":
            return await self.stop(message)
        elif message_split[0] == "%play":
            return await self.play(message)
        elif message_split[0] == "%join" or message_split[0] == "%connect":
            return await self.connect(message)
        elif message_split[0] == "%leave":
            return await self.leave(message)
        elif message_split[0] == "%skip":
            return await self.skip(message)
        elif message_split[0] == "%help":
            return await self.help(message)

    async def ping(self, message):
        """Sends pong to channel message was sent from"""
        await message.channel.send("pong!")
        return 0

    async def stop(self, message):
        """Stops bot from running"""
        await message.channel.send("Shutting down...")
        return -1

    async def play(self, message):
        """
        Downloads audio file from youtube based on message content
        Plays audio through discord voice client
        Calls on self._play_queue() after audio is done playing
        """
        discord.opus.load_opus(ctypes.util.find_library("opus"))
        if len(message.content.split()) < 2:
            message.channel.send("Please enter a video title")

        search_term = " ".join(message.content.split()[1:])
        ydl_options = {
            "format": "bestaudio",
            "noplaylist": "True",
            "outtmpl": "%(id)s.%(ext)s"
        }
        ydl = yt_dlp.YoutubeDL(ydl_options)
        video_info = ydl.extract_info(f"ytsearch:{search_term}")["entries"][0]
        filename = f"{video_info['id']}.webm"

        source = await discord.FFmpegOpusAudio.from_probe(filename)
        if message.guild.id in self.playlists:
            self.playlists[message.guild.id].append(source)
        else:
            self.playlists[message.guild.id] = [source]
        # maybe errors if method is slow or if multiple coroutines run
        # the same function at once
        await self.connect(message)
        await message.channel.send(f"Added `{video_info['title']} [{video_info['id']}]` to the queue")

        if not self.voice_client:
            await self.connect(message)
        elif self.voice_client.is_playing():
            self.playlists[message.guild.id].append(source)
        else:
            self.voice_client.play(self.playlists[message.guild.id].pop(0),
                                   after=lambda: self._play_queue(message))
            os.remove(filename)

        return 0

    async def _play_queue(self, message):
        """Plays songs that are in queue after previous song is done"""
        if not self.playlists[message.guild.id]:
            await message.channel.send("No more songs queued. Leaving voice...")
            await self.leave(message)
            return

        source = self.playlists[message.guild.id].pop(0)
        self.voice_client.play(source, after=lambda: self._play_queue(message))

    async def connect(self, message):
        """Connects to voice client if not already connected"""
        if not self.voice_client:
            self.voice_client = await message.author.voice.channel.connect()

        return 0

    async def leave(self, message):
        """Leaves if currently connected to a voice channel"""
        if self.voice_client is None:
            await message.channel.send("Not connected to voice you silly goose🤪")
            return 1

        await message.channel.send("Leaving voice channel...")
        await self.voice_client.disconnect(force=True)
        self.voice_client = None

        return 0

    async def skip(self, message):
        """Skips current song"""
        if self.voice_client is None:
            await message.channel.send("Not currently playing a song...")
            return 1

        if self.voice_client.is_playing():
            self.voice_client.stop()
            await self._play_queue(message)
            return 0


    async def help(self, message):
        """Instructs user with supported commands"""
        await message.channel.send("""
`%play 'video title'` plays audio through discord voice client\n
`%skip` skips currently playing audio\n
`%connect` or `%join` connects to discord voice client\n
`%leave` leaves discord voice client\n
        """)

        return 0
