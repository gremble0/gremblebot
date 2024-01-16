from nextcord import AudioSource, FFmpegOpusAudio
from dataclasses import dataclass
from yt_dlp import YoutubeDL
from pathlib import Path


@dataclass
class Audio:
    source: AudioSource
    title: str
    url: str


async def download_audio(query: str, path: Path | str) -> Audio:
    """
    Download media from youtube based on query

    Parameters:
        - query: The query that will be searched for on YouTube. The first result for this query will be downloaded

    Returns:
        Media object containing an AudioSource of the downloaded media and the title of the youtube video
    """
    ydl = YoutubeDL({
        "format": "bestaudio",
        "noplaylist": "True",
        "outtmpl": f"{path}/%(id)s.%(ext)s"
    })

    # TODO: regex search to either install directly from query as url or search first
    # re.match("https:\/\/www\.youtube\.com\/watch\?v=.*", query)
    results = ydl.extract_info(f"ytsearch:{query}")

    if not results:
        raise RuntimeError("YoutubeDL query failed")

    first_video = results["entries"][0]
    filename = f"{path}/{first_video['id']}.webm"
    url = "https://www.youtube.com/watch?v=" + first_video["id"]

    return Audio(await FFmpegOpusAudio.from_probe(filename), first_video["title"], url)
