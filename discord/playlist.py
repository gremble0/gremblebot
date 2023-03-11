"""Single purpose file for playlist class"""
import discord

class Playlist:
    """Class for keeping track of songs queued by !play command"""
    def __init__(self) -> None:
        self.queue = []

    def pop(self) -> None:
        """Removes song from start of queue"""
        self.queue.pop(0)

    def insert(self, yt_obj) -> None:
        """Append song to end of queue"""
        self.queue.append(yt_obj)

    def play(self):
        """Remove first song from queue and return it"""
        return self.queue.pop(0)
