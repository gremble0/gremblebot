"""File for handling user input/commands"""
import ctypes
import yt_dlp
import discord
import os


class CommandHandler:
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
    """

    def __init__(self, bot):
        self.message = None
        self.bot = bot
        self.playlists = {} 

    async def handle_command(self):
        """
        Starts coroutine for private method based on the
        content of the message variable
        """

        message_split = self.message.content.split()
        if message_split[0] == "%ping":
            await self._ping()
        elif message_split[0] == "%stop":
            await self._stop()
        elif message_split[0] == "%play":
            await self._play()

    async def _ping(self):
        """Sends pong to channel message was sent from"""
        await self.message.channel.send("pong!")

    async def _stop(self):
        """Stops bot from running"""
        await self.message.channel.send("Shutting down...")
        await self.bot.client.close()

    async def _play(self):
        """
        Downloads mp3 file from youtube based on message content
        Plays mp3 file through discord voice client
        """
        discord.opus.load_opus(ctypes.util.find_library("opus"))
        if len(self.message.content.split()) < 2:
            self.message.channel.send("Please enter a video title")
        # if len(self.playlists[self.message.guild.id]) >= 10:
        #    self.message.channel.send("Queue is full :(")
        #    return

        search_term = " ".join(self.message.content.split()[1:])
        ydl_options = {
            "format": "bestaudio",
            "noplaylist": "True",
        }
        ydl = yt_dlp.YoutubeDL(ydl_options)
        video_info = ydl.extract_info(f"ytsearch:{search_term}")["entries"][0]
        filename = f"{video_info['title']} [{video_info['id']}].webm"

        source = await discord.FFmpegOpusAudio.from_probe(filename)
        if self.message.guild.id in self.playlists:
            self.playlists[self.message.guild.id].append(source)
        else:
            self.playlists[self.message.guild.id] = [source]
        # maybe errors if method is slow or if multiple coroutines run
        # the same function at once
        await self._connect()
        await self.message.channel.send(f"Added `{filename.rstrip('.webm')}` \
            to the queue")

        if self.bot.voice_client.is_playing():
            self.playlists[self.message.guild.id].append(source)
        else:
            self.bot.voice_client.play(self.playlists[self.message.guild.id].pop(0),
                after = lambda x = None: self._play_queue())
            os.remove(filename)

    def _play_queue(self):
        """Plays songs that are in queue after previous song is done"""
        if not self.playlists[self.message.guild.id]:
            return

        source = self.playlists[self.message.guild.id].pop(0)
        self.bot.voice_client.play(source, after=lambda x=None: self._play_queue())

    async def _connect(self):
        """Connects to voice client if not already connected"""
        if self.bot.voice_client is None:
            self.bot.voice_client = await self.message.author.voice.channel.connect()
