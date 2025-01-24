from pygame import mixer
from file_management import *

def get_music_length(music):
    """Obtém a duração da música em segundos."""
    from mutagen.mp3 import MP3
    audio = MP3(musicAudioPath + music)
    return int(audio.info.length)

def get_recent_songs(activityPath):
    """Lê o arquivo activityPath e retorna uma lista de músicas recentemente tocadas."""
    recentMusic = []
    try:
        with open(activityPath, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                musicInfo = linha.strip().split(";")
                if len(musicInfo) == 2:
                    nome, autor = musicInfo
                    recentMusic.append((nome, autor))
    except FileNotFoundError:
        print(f"O arquivo {activityPath} não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
    return recentMusic

def filter_music(musicList, recentMusic):
    """Filtra musicList para incluir apenas músicas presentes em recentMusic."""
    activityList = []
    for musica in recentMusic:
        for music in musicList:
            if music[0] == musica[0] and music[1] == musica[1]:
                activityList.append(music)
                break
    return activityList