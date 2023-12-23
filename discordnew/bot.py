from nextcord import Interaction, Intents, Client, VoiceClient, Message, FFmpegOpusAudio, AudioSource, Member
from nextcord.ext import commands
from dotenv import load_dotenv
from os import getenv, remove
from yt_dlp import YoutubeDL

class Bot:
    def __init__(self) -> None:
        intents = Intents.default()
        intents.message_content = True

        self.client: Client = commands.Bot()
        self.voice_client: VoiceClient | None = None
        self.playlists: dict[int, list[AudioSource]] = {}
        self.ydl: YoutubeDL = YoutubeDL({
            "format": "bestaudio",
            "noplaylist": "True",
            "outtmpl": "%(id)s.%(ext)s"
        })

        @self.client.event
        async def on_ready():
            print("-------------------------------")
            print("gremblebot is now ready to use!")
            print("-------------------------------")

        @self.client.event
        async def on_message(message: Message) -> None:
            if message.author == self.client.user: return

            print(f"@{message.guild}#{message.channel}, {message.author}: {message.content}")
            await self.handle_message(message)

        @self.client.slash_command(guild_ids=[978053854878904340], description="pong!")
        async def ping(interaction: Interaction) -> None:
            await interaction.response.send_message("pong!")

        @self.client.slash_command(guild_ids=[978053854878904340], description="Play audio from a youtube video")
        async def play(interaction: Interaction, query: str) -> None:
            if not self.voice_client:
                try:
                    self.voice_client = await self._connect(interaction)
                except RuntimeError:
                    await interaction.response.send_message("You're not connected to a voice channel")
                    return

            audio_source: AudioSource = await self._download_video(query)
            await interaction.response.send_message(f"Added `{audio_source}` to the queue")

            if interaction.guild_id in self.playlists:
                self.playlists[interaction.guild_id].append(audio_source)
            else:
                self.playlists[interaction.guild_id] = [audio_source]

            if len(self.playlists[interaction.guild_id]) == 1:
                self.voice_client.play(audio_source, after=lambda x=interaction: self._play_queue(x))

    def _play_queue(self, interaction: Interaction) -> None:
        if not self.playlists[interaction.guild_id] or not self.voice_client:
            return

        source = self.playlists[interaction.guild_id].pop(0)
        self.voice_client.play(source, after=lambda x=interaction: self._play_queue(x))

    async def _connect(self, interaction: Interaction) -> VoiceClient:
        """Wrapper function to connect to the voice channel of a users interaction"""
        if not isinstance(interaction.user, Member):
            raise TypeError(f"Expected type {Member.__class__} but got {interaction.__class__}")
        if not interaction.user.voice:
            raise RuntimeError(f"Member {interaction.user.name} is not connected to a voice channel")
        if not interaction.user.voice.channel:
            # TODO: find out what voice.channel being None really means
            raise RuntimeError(f"Member {interaction.user.name} is not connected to a voice channel")

        return await interaction.user.voice.channel.connect()

    async def _download_video(self, query: str) -> AudioSource:
        # TODO: regex search to either install directly from query as url or search first
        # re.match("https:\/\/www\.youtube\.com\/watch\?v=.*", query)
        results = self.ydl.extract_info(f"ytsearch:{query}")

        if not results:
            raise RuntimeError("YoutubeDL query failed")

        first_video = results["entries"][0]
        filename = f"{first_video['id']}.webm"

        return await FFmpegOpusAudio.from_probe(filename)
                            
    def run(self) -> None:
        load_dotenv(dotenv_path=".env")
        DISCORD_TOKEN: str | None = getenv("DISCORD_TOKEN")

        if not DISCORD_TOKEN:
            print("Couldn't find discord token")
        else:
            self.client.run(DISCORD_TOKEN)

    async def handle_message(self, message: Message):
        pass


if __name__ == "__main__":
    bot = Bot()
    bot.run()
