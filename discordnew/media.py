from nextcord import AudioSource, FFmpegOpusAudio
from dataclasses import dataclass
from yt_dlp import YoutubeDL


ydl: YoutubeDL = YoutubeDL({
    "format": "bestaudio",
    "noplaylist": "True",
    "outtmpl": "%(id)s.%(ext)s"
})


@dataclass
class Media:
    audio_source: AudioSource
    title: str


async def download_media(query: str) -> Media:
    """
    Download media from youtube based on query

    Parameters:
        - query: The query that will be searched for on YouTube. The first result for this query will be downloaded and added to the queue

    Returns:
        Media object containing an AudioSource of the downloaded media and the title of the youtube video
    """
    # TODO: regex search to either install directly from query as url or search first
    # re.match("https:\/\/www\.youtube\.com\/watch\?v=.*", query)
    results = ydl.extract_info(f"ytsearch:{query}")

    if not results:
        raise RuntimeError("YoutubeDL query failed")

    first_video = results["entries"][0]
    filename = f"{first_video['id']}.webm"

    return Media(await FFmpegOpusAudio.from_probe(filename), first_video["title"])
