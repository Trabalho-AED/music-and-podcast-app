from pygame import mixer
from file_management import *

def get_music_length(music):
    """Obtém a duração da música em segundos."""
    from mutagen.mp3 import MP3
    audio = MP3(musicAudioPath + music)
    return int(audio.info.length)