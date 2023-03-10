"""File for handling user input/commands"""
import ctypes
import yt_dlp as youtube_dl
import discord

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

    Methods
    -------
    handle_command():
        redirects to appropriate command based on user input
    """


    def __init__(self, bot):
        self.message = None
        self.bot = bot


    async def handle_command(self):
        """
        Starts coroutine for private method based on the
        content of the message variable
        """

        message_split = self.message.content.split()
        if message_split[0] == "!ping":
            await self._ping()
        elif message_split[0] == "!stop":
            await self._stop()
        elif message_split[0] == "!play":
            await self._play()


    async def _ping(self):
        await self.message.channel.send("pong!")


    async def _stop(self):
        await self.message.channel.send("Shutting down...")
        await self.bot.client.close()


    async def _play(self):
        discord.opus.load_opus(ctypes.util.find_library("opus"))
        if len(self.message.content.split()) < 2:
            self.message.channel.send("Please enter a video title")
        if len(self.bot.playlist.queue) >= 10:
            self.message.channel.send("Queue is full :(")

        video_url = self.search(" ".join(self.message.split()[1:]))
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
        voice_client = await self.message.author.voice.channel.connect()
        # try except ClientException for queueing??
        voice_client.play(source)

        return f"Added {filename} to the queue."


    def search(self, search_term) -> str:
        """
        Searches youtube for video based on search_term. Returns string of video url
            Parameters:
                search_term (str): Video title
            Returns:
                video (str): Youtube URL to first search result
        """
        ydl_options = {"format": "bestaudio", "noplaylist": "True"}
        ydl = youtube_dl.YoutubeDL(ydl_options)
        video = ydl.extract_info(f"ytsearch:{search_term}", download=False)["entries"][0]

        return "youtube.com/watch?v=" + video["id"]
