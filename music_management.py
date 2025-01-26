from pygame import mixer
from file_management import *
import webbrowser                        # https://docs.python.org/3/library/webbrowser.html 

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

def play_podcast(videoURL):
    """
    Abre o browser definido por defeito com um url
    """
    webbrowser.open(videoURL, new = 0, autoraise=True)

def get_authors(musicList):
    
    authorList=[]

    for music in musicList:
        if music[1] not in authorList:
            authorList.append(music[1])

    return authorList

def get_favorites(musicList, usernameFinal):
    favoriteList = []

    # Lê o arquivo de favoritos
    with open(f"{usersPath}{usernameFinal}{pathFormat}favorites.csv", "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        fields = line.strip().split(";")
        # Remove espaços desnecessários em cada campo
        fields = [field.strip() for field in fields]

        # Verifica se alguma música da musicList coincide com os dois primeiros campos de fields
        for music in musicList:
            if music[0] == fields[0] and music[1] == fields[1]:
                favoriteList.append(music)

    return favoriteList

def remove_favorite(name, author, usernameFinal):
    file_path = f"{usersPath}{usernameFinal}{pathFormat}favorites.csv"

    # Lê o conteúdo do arquivo
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Cria uma nova lista sem a música que será removida
    updated_lines = []
    for line in lines:
        fields = line.strip().split(";")
        # Remove espaços desnecessários nos campos
        fields = [field.strip() for field in fields]

        # Se o nome e autor não coincidem, mantém a linha
        if not (fields[0] == name and fields[1] == author):
            updated_lines.append(line)

    # Escreve as linhas atualizadas de volta no arquivo
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(updated_lines)

def remove_music_playlist(name, author, usernameFinal,playListName):
    file_path = f"{usersPath}{usernameFinal}{pathFormat}playlists{pathFormat}{playListName}.csv"

    # Lê o conteúdo do arquivo
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Cria uma nova lista sem a música que será removida
    updated_lines = []
    for line in lines:
        fields = line.strip().split(";")
        # Remove espaços desnecessários nos campos
        fields = [field.strip() for field in fields]

        # Se o nome e autor não coincidem, mantém a linha
        if not (fields[0] == name and fields[1] == author):
            updated_lines.append(line)

    # Escreve as linhas atualizadas de volta no arquivo
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(updated_lines)

def get_playlist_list(musicList, usernameFinal, playListName):
    playlistList = []

    # Lê o arquivo de favoritos
    with open(f"{usersPath}{usernameFinal}{pathFormat}playlists{pathFormat}{playListName}.csv", "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        fields = line.strip().split(";")
        # Remove espaços desnecessários em cada campo
        fields = [field.strip() for field in fields]

        # Verifica se alguma música da musicList coincide com os dois primeiros campos de fields
        for music in musicList:
            if music[0] == fields[0] and music[1] == fields[1]:
                playlistList.append(music)

    return playlistList

def add_favorites(musicName,musicAuthor,usernameFinal):
    if musicName == None:
        return
    else:
        file_path = f"{usersPath}{usernameFinal}{pathFormat}favorites.csv"

        # Lê o conteúdo atual do arquivo
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Verifica se a combinação já existe no arquivo
        for line in lines:
            fields = line.strip().split(";")
            # Remove espaços desnecessários nos campos
            fields = [field.strip() for field in fields]
            if fields[0] == musicName and fields[1] == musicAuthor:
                print(f"'{musicName}' by {musicAuthor} is already in favorites.")
                return

        # Se não encontrar, adiciona ao arquivo
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"{musicName};{musicAuthor}\n")

        print(f"'{musicName}' by {musicAuthor} has been added to favorites.")

def check_favorite(musicName,musicAuthor,usernameFinal):
    file_path = f"{usersPath}{usernameFinal}{pathFormat}favorites.csv"

     # Lê o conteúdo atual do arquivo
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Verifica se a combinação existe no arquivo
    for line in lines:
        fields = line.strip().split(";")
        # Remove espaços desnecessários nos campos
        fields = [field.strip() for field in fields]
        if fields[0] == musicName and fields[1] == musicAuthor:
            print(f"'{musicName}' by {musicAuthor} is in favorites.")
            return True

    return False

def get_podcast(podcastList):
    podcastMainList=[]
    
    for podcast in podcastList:
        if podcast[1] not in podcastMainList:
            podcastMainList.append(podcast[1])

    return podcastMainList

# Ensure you are extracting all unique categories
def get_categories_music(musicList):
    return list(set(music[2] for music in musicList))  # Extract unique categories from the music list