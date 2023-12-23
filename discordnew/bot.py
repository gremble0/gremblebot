from nextcord import Interaction, Intents, Client, VoiceClient, Message, FFmpegOpusAudio, AudioSource
from nextcord.ext import commands
from dotenv import load_dotenv
from os import getenv
from yt_dlp import YoutubeDL

intents = Intents.default()
intents.message_content = True

client: Client = commands.Bot()
voice_clients: VoiceClient | None = None # TODO: voice_client: dict[int, VoiceClient] = {}
playlists: dict[int, list[AudioSource]] = {}
ydl: YoutubeDL = YoutubeDL({
    "format": "bestaudio",
    "noplaylist": "True",
    "outtmpl": "%(id)s.%(ext)s"
})

@client.event
async def on_ready():
    print("-------------------------------")
    print("gremblebot is now ready to use!")
    print("-------------------------------")

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user: return

    print(f"@{message.guild}#{message.channel}, {message.author}: {message.content}")

@client.slash_command(guild_ids=[978053854878904340], description="pong!")
async def ping(interaction: Interaction) -> None:
    await interaction.response.send_message("pong!")

@client.slash_command(guild_ids=[978053854878904340], description="Play audio from a youtube video")
async def play(interaction: Interaction, query: str) -> None:
    if not voice_clients:
        try:
            # voice_channel = interaction.user.voice.channel
            voice_client = await interaction.user.voice.channel.connect()
        except RuntimeError:
            await interaction.response.send_message("You're not connected to a voice channel")
            return

    audio_source: AudioSource = await _download_video(query)
    # await interaction.response.send_message(f"Added `{audio_source}` to the queue")

    if interaction.guild_id in playlists:
        playlists[interaction.guild_id].append(audio_source)
    else:
        playlists[interaction.guild_id] = [audio_source]

    if len(playlists[interaction.guild_id]) == 1:
        voice_client.play(audio_source, after=lambda x=interaction: _play_queue(x))

def _play_queue(interaction: Interaction) -> None:
    if not playlists[interaction.guild_id] or not voice_client:
        return

    source = playlists[interaction.guild_id].pop(0)
    voice_client.play(source, after=lambda x=interaction: _play_queue(x))

async def _download_video(query: str) -> AudioSource:
    # TODO: regex search to either install directly from query as url or search first
    # re.match("https:\/\/www\.youtube\.com\/watch\?v=.*", query)
    results = ydl.extract_info(f"ytsearch:{query}")

    if not results:
        raise RuntimeError("YoutubeDL query failed")

    first_video = results["entries"][0]
    filename = f"{first_video['id']}.webm"

    return await FFmpegOpusAudio.from_probe(filename)
                        
def main() -> None:
    load_dotenv(dotenv_path=".env")
    DISCORD_TOKEN: str | None = getenv("DISCORD_TOKEN")

    if not DISCORD_TOKEN:
        print("Couldn't find discord token")
    else:
        client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
