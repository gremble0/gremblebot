"""Discord bot written by gremble"""
import ctypes
import datetime
import secrets
import yt_dlp as youtube_dl
import discord
from playlist import Playlist
from commands import CommandHandler

class Bot:
    """
    Main class for running bot
    
    Attributes
    ----------
    commands : str[]
        list of supported commands
    client : discord.Client()
        client for connecting to discord server
    voice_client : None
        client for connecting to discord voice servers
        starts uninstantiated, but becomes type : discord.VoiceClient
        once connected to a voice channel
    """

    def __init__(self):
        self.commands = [
            "!ping",
            "!play",
            "!stop"
        ]
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents = intents)
        self.voice_client = None
        self.playlist = Playlist(self.client) # for !play command
        self.command_handler = CommandHandler(self)

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            now = datetime.datetime.today().strftime("%Y/%m/%d %H:%M")
            print(f"{now} #{message.channel}, {message.author}: {message.content}")

            self.command_handler.message = message
            message_split = message.content.split()
            if message_split[0] in self.commands:
                await self.command_handler.handle_command()


    def run(self) -> None:
        """Runs bot"""
        self.client.run(secrets.DISCORD_TOKEN)


    def _search(self, search_term) -> str:
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


    async def handle_command(self, message):
        """
        Handles commands and returns string to be sent in text channel
            Parameters:
                message (str): message sent by user
        """
        message_split = message.content.split()


        if message_split[0] == "!ping":
            await message.channel.send("pong!")
            return

        if message_split[0] == "!stop":
            await message.channel.send("shutting down...")
            await self.client.close()
            return

        if message_split[0] == "!play":
            discord.opus.load_opus(ctypes.util.find_library("opus"))
            if len(message_split) < 2:
                await message.channel.send("Please enter a video title")
            if len(self.playlist.queue) >= 10:
                await message.channel.send("Queue is full :(")

            video_url = self._search(" ".join(message_split[1:]))
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
            # try except ClientException for queueing?? probably bad
            voice_client.play(source)

            return f"Added {filename} to the queue."


    # todo - migrate commands to bot class,
    #      - add dict for calling commands,
    #      - fix queueing songs in !play
    #      - add command for stopping bot remotely,
    #           - easier with commands in bot class
    #      - remove songs after played
    #      - remove _search()


if __name__ == "__main__":
    bot = Bot()
    bot.run()
