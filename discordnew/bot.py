from nextcord import Interaction, Client, VoiceClient, Message
from nextcord.ext import commands
from dotenv import load_dotenv
from os import getenv
from media import Media, download_media


client: Client = commands.Bot()
voice_clients: dict[int, VoiceClient] = {}
playlists: dict[int, list[Media]] = {}


@client.event
async def on_ready():
    print("-------------------------------")
    print("gremblebot is now ready to use!")
    print("-------------------------------")


@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    print(f"@{message.guild}#{message.channel}, {message.author}: {message.content}")


@client.slash_command(guild_ids=[978053854878904340], description="pong!")
async def ping(interaction: Interaction) -> None:
    await interaction.response.send_message("pong!")


@client.slash_command(guild_ids=[978053854878904340], description="Play audio from a youtube video")
async def play(interaction: Interaction, query: str) -> None:
    if not interaction.guild_id:
        await interaction.response.send_message("Play command has to be used in a server")
        return

    if not interaction.guild_id in voice_clients.keys():
        try:
            voice_clients[interaction.guild_id] = await interaction.user.voice.channel.connect()
        except RuntimeError:
            await interaction.response.send_message("You're not connected to a voice channel")
            return

    # Using interaction more than 3 seconds after instantiation results in error
    # so we need to defer it in case media download takes more than that
    await interaction.response.defer()
    media = await download_media(query)
    await interaction.followup.send(f"Added `{media.title}` to the queue")

    if interaction.guild_id in playlists:
        playlists[interaction.guild_id].append(media)
    else:
        playlists[interaction.guild_id] = [media]

    if len(playlists[interaction.guild_id]) == 1:
        voice_clients[interaction.guild_id].play(
            media.audio_source,
            after=lambda x=interaction.guild_id: play_queue(x)
        )


def play_queue(guild_id: int) -> None:
    """
    Recursively continues the playlist in the given server until the playlist
    in that server is empty.
    """
    if not guild_id in playlists:
        return

    media = playlists[guild_id].pop(0)
    voice_clients[guild_id].play(media.audio_source, after=lambda x=guild_id: play_queue(x))


@client.slash_command(guild_ids=[978053854878904340], description="Skip the currently playing audio")
async def skip(interaction: Interaction) -> None:
    if not interaction.guild_id:
        await interaction.response.send_message("Skip command has to be used in a server")
        return

    if not interaction.guild_id in playlists or not playlists[interaction.guild_id]:
        await interaction.response.send_message("Queue is empty, nothing to skip")
        return

    voice_clients[interaction.guild_id].stop()
    play_queue(interaction.guild_id)
    await interaction.response.send_message("Skipped the currently playing audio") # TODO: get name of currently playing audio


@client.slash_command(guild_ids=[978053854878904340], description="Get the current queue of songs")
async def queue(interaction: Interaction) -> None:
    if not interaction.guild_id:
        await interaction.response.send_message("Queue command has to be used in a server")
        return

    if interaction.guild_id not in playlists:
        await interaction.response.send_message("Queue is empty")
        return

    outstr = ""
    i = 1
    for song in playlists[interaction.guild_id]:
        outstr += f"{i}: {song.title} \n"
        i = i + 1

    await interaction.response.send_message(outstr)
                        

def main() -> None:
    load_dotenv(dotenv_path=".env")
    DISCORD_TOKEN: str | None = getenv("DISCORD_TOKEN")

    if not DISCORD_TOKEN:
        print("Couldn't find discord token")
    else:
        client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
