from nextcord import Interaction, Client, VoiceClient
from nextcord.ext import commands
from dotenv import load_dotenv
from os import getenv
from audio import Audio, download_audio


client: Client = commands.Bot()
voice_clients: dict[int, VoiceClient] = {}
playlists: dict[int, list[Audio]] = {}


@client.event
async def on_ready():
    print("-------------------------------")
    print("gremblebot is now ready to use!")
    print("-------------------------------")


@client.slash_command(guild_ids=[978053854878904340], description="pong!")
async def ping(interaction: Interaction) -> None:
    """
    Check if the bot is active
    """
    await interaction.response.send_message("pong!")


@client.slash_command(guild_ids=[978053854878904340], description="Play audio from a youtube video")
async def play(interaction: Interaction, query: str) -> None:
    """
    Download media from youtube based on query and add it to the queue
    of songs for the server.
    """
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
    audio = await download_audio(query)
    await interaction.followup.send(f"Added `{audio.title}` - {audio.url} to the queue")

    if interaction.guild_id in playlists:
        playlists[interaction.guild_id].append(audio)
    else:
        playlists[interaction.guild_id] = [audio]

    if not voice_clients[interaction.guild_id].is_playing():
        await play_queue(interaction)


async def play_queue(interaction: Interaction) -> None:
    """
    Recursively continues the playlist in the given server until the playlist
    in that server is empty.
    """
    if not interaction.guild_id in playlists:
        return

    if len(playlists[interaction.guild_id]) > 0:
        media = playlists[interaction.guild_id].pop(0)
        voice_clients[interaction.guild_id].play(media.source,
                                                 after=lambda _: play_queue(interaction))
        await interaction.followup.send(f"Now playing `{media.title}`")


@client.slash_command(guild_ids=[978053854878904340], description="Skip the currently playing audio")
async def skip(interaction: Interaction) -> None:
    """
    Skips the currently playing song and plays the next one in queue if the
    queue is not empty
    """
    if not interaction.guild_id:
        await interaction.response.send_message("Skip command has to be used in a server")
        return

    if interaction.guild_id not in playlists:
        await interaction.response.send_message("Nothing to skip")
        return

    if not (voice_clients[interaction.guild_id].is_paused() or voice_clients[interaction.guild_id].is_playing()):
        await interaction.response.send_message("Not playing any audio")
        return

    voice_clients[interaction.guild_id].stop()
    await interaction.response.send_message(f"Skipped currently playing audio")


@client.slash_command(guild_ids=[978053854878904340], description="Pause the currently playing audio")
async def pause(interaction: Interaction) -> None:
    """
    Pause the currently playing audio
    """
    if not interaction.guild_id:
        await interaction.response.send_message("Pause command has to be used in a server")
        return

    if interaction.guild_id not in playlists:
        await interaction.response.send_message("Nothing to pause")
        return

    if voice_clients[interaction.guild_id].is_paused():
        await interaction.response.send_message("Already paused")
        return

    voice_clients[interaction.guild_id].pause()
    await interaction.response.send_message(f"Paused currently playing audio")


@client.slash_command(guild_ids=[978053854878904340], description="Resume playing paused audio")
async def resume(interaction: Interaction) -> None:
    """
    Resume playing paused audio
    """
    if not interaction.guild_id:
        await interaction.response.send_message("Pause command has to be used in a server")
        return

    if interaction.guild_id not in playlists:
        await interaction.response.send_message("Nothing to resume")
        return

    if voice_clients[interaction.guild_id].is_playing():
        await interaction.response.send_message("Already playing audio")
        return

    voice_clients[interaction.guild_id].resume()
    await interaction.response.send_message(f"Resumed currently playing audio")


@client.slash_command(guild_ids=[978053854878904340], description="Get the current queue of songs")
async def queue(interaction: Interaction) -> None:
    """
    Gets the current queue of media
    """
    if not interaction.guild_id:
        await interaction.response.send_message("Queue command has to be used in a server")
        return

    if interaction.guild_id not in playlists or len(playlists[interaction.guild_id]) == 0:
        await interaction.response.send_message("Queue is empty")
        return

    outstr = ""
    i = 1
    for song in playlists[interaction.guild_id]:
        outstr += f"{i}: {song.title}\n"
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
