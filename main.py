import customtkinter
from PIL import Image
from tkinter import filedialog
import shutil #Copy images shutil.copy() https://docs.python.org/3/library/shutil.html
import re #Regex for expression check(username and password)
import os
from pygame import mixer #https://www.pygame.org/docs/ref/mixer.html
#from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#from comtypes import CLSCTX_ALL
import tkinter as tk
from io import StringIO
from tkinter import ttk#from tkVideoPlayer import TkinterVideo   #https://pypi.org/project/tkvideoplayer/ 
import time #Sleep
from file_management import *
from users import *
from music_management import *
from admin_management import *
import random
import CTkMessagebox

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light" Alterar entre tema escuro e claro

pathFormat = path_format()

###########################################################
currentFrame = None # Guarda o frame que o utilizador se encontra
isAdmin = False # Booleano que diz se o utilizador é ou não admin
tempCoverName = None # Para salvar o nome da imagem da música
tempAudioName = None # Para salvar o nome do aúdio da música
nameFull = None  # Para salvar o nome do utilizador
currentLevel = 50 # Para Salvar o volume antes de mute
isPaused = True # Para salvar estado da música
usernameFinal = None # Para salvar o username no login
musicNameCurrent = None # Para salvar a musica a ser tocada
musicAuthorCurrent = None # Para salvar o artista da musica a ser tocada
isFavorite = False
passwordFinal = None
currentPlaylist = []  # Lista com todas as músicas sendo exibidas
currentIndex = 0  # Índice da música atual
###########################################################

# Inicializar app
app = customtkinter.CTk(fg_color= "#000000")

# Titulo da app
app.title("Music App")

# Define a dimensão da app
appWidth = 1500
appHeight = 800

# App não resizable em x
app.resizable(width=False, height=False)

# Obtém a dimensão do ecrã
screenWidth = app.winfo_screenwidth()
screenHeight = app.winfo_screenheight()

app.iconbitmap(f"{imagePath}favicon.ico")

# Calcula a posição para centralizar a janela
x = (screenWidth / 2) - (appWidth / 2)
y = (screenHeight / 2) - (appHeight / 2)

# Define o tamanho da app e começa no centro da tela
app.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")

##################[ALGORITMOS DA APP]################################

def check_format(value, typeVal):
    """Verifica se o username e password estão no formato pedido"""

    fullPasswordRegex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,16}$" # Expressão regular que verifica que a password cumpre todos os pârametros
    onlyLowerNumberRegex = r"(.*[a-z].*)$" # Expressão regular que verifica que a password tem letras minúsculas
    onlyUpperNumberRegex = r"(.*[A-Z].*)$" # Expressão regular que verifica que a password tem letras maiúsculas
    onlyNumberRegex = r"(.*[0-9].*)$" # Expressão regular que verifica que a password tem números

    #Se o campo não estiver preenchido estiver vazio, retornar
    if value == "":
        return
    
    #Caso seja nome
    if typeVal=="name":
        if value.count(";") > 0:
            return "Name cannot have "";"" character" # Texto a apresentar
        else:
            return None
    #Caso seja username
    elif typeVal=="user":
        #Caso o username não tenha entre 8 e 16 caracteres
        if len(value)<8 or len(value)>16:
            return "Username must be between 8 and 16 characters long." # Texto a apresentar
        elif value.count(";") > 0:
            return "Username cannot have "";"" character" # Texto a apresentar
        else:
            return None 
    #Caso seja password
    else:
        if not re.findall(onlyNumberRegex, value):
            return "Password doesn't meet the requirements.\nMust have at least one number." # Texto a apresentar
        elif not re.findall(onlyLowerNumberRegex, value):
            return "Password doesn't meet the requirements.\nMust have at least one lowercase character." # Texto a apresentar
        elif not re.findall(onlyUpperNumberRegex, value):
            return "Password doesn't meet the requirements.\nMust have at least one uppercase character." # Texto a apresentar
        elif not re.findall(fullPasswordRegex, value):
            return "Password doesn't meet the requirements.\nMust be between 8 and 16 characters long." # Texto a apresentar
        elif value.count(";") > 0:
            return "Password cannot have "";"" character" # Texto a apresentar
        else:
            return None

def check_admin(username):
    """Verifica se o utilizador é admin.
    Retorna um booleano"""

    global isAdmin

    lines = read_file(adminListfile) # Abrir os dados do ficheiro admin

    #Para cada linha de dados
    for line in lines:
        if line.strip() == username:
            isAdmin = True
            return True # Se o utilizador na linha for igual ao username
        
    return False # Se o utilizador não estiver na lista de admin


def create_account(username, password, name):
    """Cria uma conta"""

    accountAdd = username+";"+password+";"+name+"\n" # String com o Formato dos dados
    create_sub_folders(f"db{pathFormat}users{pathFormat}{username}")
    create_sub_folders(f"db{pathFormat}users{pathFormat}{username}{pathFormat}playlists")
    create_main_files(f"db{pathFormat}users{pathFormat}{username}{pathFormat}favorites.csv")
    create_main_files(f"db{pathFormat}users{pathFormat}{username}{pathFormat}music_activity.csv")
    create_main_files(f"db{pathFormat}users{pathFormat}{username}{pathFormat}podcast_activity.csv")
    create_main_files(f"db{pathFormat}users{pathFormat}{username}{pathFormat}notification.csv")
    with open(accountsPath, "a", encoding="utf-8") as file:
        file.write(accountAdd) # Escreve os dados no ficheiro

    return

def get_accounts(username,password):
    """Verifica se existe o username ou a combinação username - password.
    Retorna os dados encontrados"""

    lines = read_file(accountsPath) # Recebe o conteúdo do ficheiro
    
    #Para cada linha
    for line in lines:
        fields = line.strip().split(";")
        if fields[0] == username and fields[1] == password:
            return fields[0], fields[1], fields[2] # Se a combinação username e password existir, retorna todos os dados
    
    return "not_found", "not_found", "" # Caso a combinação não exista, retorna as strings

def register_action(usernameEntry, passwordEntry,nameEntry, resultLabel, frameRegister):
    """Gere o algoritmo de registo"""

    name = nameEntry.get() # Recebe o valor que está na entry do nome
    username = usernameEntry.get() # Recebe o valor que está na entry do username
    password = passwordEntry.get() # Recebe o valor que está na entry da password

    nameFormat = check_format(name, "name") # Verifica se o nome está dentro dos parâmentos
    userFormat = check_format(username, "user") # Verifica se o username está dentro dos parâmentos
    passwordFormat = check_format(password, "password") # Verifica se a password está dentro dos parâmentos

    if username == "" or password == "" or name == "": 
        resultLabel.configure(text="Fill all fields.") # Texto a apresentar
        return
    elif nameFormat:
        resultLabel.configure(text=userFormat)
        return
    elif userFormat:
        resultLabel.configure(text=userFormat)
        return
    elif passwordFormat:
        resultLabel.configure(text=passwordFormat)
        return
    
    print(f"Username: {username}, Password: {password}")  # Substituir por lógica real de autenticação

    isUser = user_check(username) # Booleano - Verifica se o utilizador já existe

    # Caso o utilizador já exista
    if isUser:
        resultLabel.configure(text="Utilizador já existe!.") # Texto a apresentar
    #Caso o utilizador não exista
    else:
        create_account(username, password, name) # Criar a conta
        resultLabel.configure(text=f"Bem vindo {name}, Conta criada com com sucesso!") # Texto a apresentar
        time.sleep(2)
        login_render(frameRegister)



def login_action(usernameEntry, passwordEntry, resultLabel,loginFrame):
    """Gere o algoritmo de login"""

    global nameFull, usernameFinal, passwordFinal

    username = usernameEntry.get() # Recebe o valor que está na entry do username
    password = passwordEntry.get() # Recebe o valor que está na entry da password

    # Se algum campo estiver vazio
    if username == "" or password == "": 
        resultLabel.configure(text="Preencha todos os campos.") # Texto a apresentar
        return 
    
    print(f"Username: {username}, Password: {password}")  # Mensagem de confirmação na consola

    username, password, name = get_accounts(username, password) # Verifica se a combinação utilizador/password existe
    
    isAdmin = check_admin(username) # Booleano - Verifica se o utilizador é admin
    if isAdmin: # Se for admin, atribui a flag admin ao utilizador
        adminflag = "Admin"
    else: # Se não for admin, atribui a flag não admin ao utilizador
        adminflag = "Não Admin"

    if username == "not_found" and password == "not_found": # Se o utilizador e a password não existirem ou a password estiver errada
        resultLabel.configure(text="Utilizador Inexistente ou password errada.") # Texto a apresentar

    else: # Se a combinação utilizador password estiver correta 
        resultLabel.configure(text=f"Bem vindo {name}, Login realizado com sucesso!\nTipo de Utilizador: {adminflag}") # Texto a apresentar
        print(username, password, adminflag) # Confirmação
        nameFull = name
        usernameFinal = username
        passwordFinal = password
        mainwindow_render(loginFrame) # Passa para a janela principal
##########################################################

#############################[RENDER SCREENS]##########################################
def register_render(oldFrame):
    """Renderiza a frame do formulário de registo"""

    print("Register") # Mensagem de confirmação na consola

    oldFrame.destroy() # Apagar o estilo do frame anterior

    #Frame
    frameRegister = customtkinter.CTkFrame(app, width=800, height=500, fg_color= "#0D0D0D")
    frameRegister.pack_propagate(False)
    frameRegister.pack(expand=True)

    # Labels Register
    RegisterLabel = customtkinter.CTkLabel(frameRegister, text="Register",font=("Roboto", 28))
    RegisterLabel.pack(padx=0, pady=60)

    # Labels e campos de entrada
    nameLabel = customtkinter.CTkLabel(frameRegister, text="Nome:", font=("Roboto", 18))
    nameLabel.place(x=230, y=120,anchor='w')

    nameEntry = customtkinter.CTkEntry(frameRegister, placeholder_text="Nome...",width=310)
    nameEntry.place(x=230,y=150, anchor='w')

    usernameLabel = customtkinter.CTkLabel(frameRegister, text="Username:",font=("Roboto", 18))
    usernameLabel.place(x=230, y=210, anchor='w')

    usernameEntry = customtkinter.CTkEntry(frameRegister, placeholder_text="Username...",width=310)
    usernameEntry.place(x=230, y=240, anchor='w')

    passwordLabel = customtkinter.CTkLabel(frameRegister, text="Password:", font=("Roboto", 18))
    passwordLabel.place(x=230, y=280)

    passwordEntry = customtkinter.CTkEntry(frameRegister, placeholder_text="Password...", show="*",width=310)
    passwordEntry.place(x=230, y=310)

    # Botão de login
    loginButton = customtkinter.CTkButton(frameRegister,width=60, text="Login", command=lambda:login_render(frameRegister))
    loginButton.place(x=420, y=415)

    #label Existent User
    existentUserLabel = customtkinter.CTkLabel(frameRegister, text="Existing User? Login!",font=("Roboto", 12))
    existentUserLabel.place(x=290, y=415)

    # Botão de criar conta
    CreateButton = customtkinter.CTkButton(frameRegister,height=40,width=200,text="Create User", command=lambda:register_action(usernameEntry, passwordEntry,nameEntry, resultLabel, frameRegister))
    CreateButton.place(x=290, y=360)

    # Label para exibir resultados ou mensagens de erro
    resultLabel = customtkinter.CTkLabel(frameRegister, text="")
    resultLabel.pack(padx=20, pady=20)


def login_render(oldFrame):
    """Renderiza a frame do formulário de login"""

    #Caso não exista frame anterior (ex: Ao executar a app)
    if oldFrame == "":
        pass
    else:
        oldFrame.pack_forget() # Apagar o estilo do frame anterior

    #Frame
    frameLogin = customtkinter.CTkFrame(app, width=800, height=500, fg_color= "#0D0D0D")
    frameLogin.pack_propagate(False)
    frameLogin.pack(expand=True )

    # Labels Login
    LoginLabel = customtkinter.CTkLabel(frameLogin, text="Login",font=("Roboto", 28))
    LoginLabel.pack(padx=0, pady=60)

    # Labels e campos de entrada
    usernameLabel = customtkinter.CTkLabel(frameLogin, text="Username:", font=("Roboto", 18))
    usernameLabel.place(x=230, y=150,anchor='w')

    usernameEntry = customtkinter.CTkEntry(frameLogin, placeholder_text="Username...", width=310)
    usernameEntry.place(x=230,y=180, anchor='w')

    passwordLabel = customtkinter.CTkLabel(frameLogin, text="Password:",font=("Roboto", 18))
    passwordLabel.place(x=230, y=240, anchor='w')

    passwordEntry = customtkinter.CTkEntry(frameLogin, placeholder_text="Password...", show="*", width=310)
    passwordEntry.place(x=230, y=270, anchor='w')

    # Botão de login
    loginButton = customtkinter.CTkButton(frameLogin,height=40,width=200,text="Login",font=("Roboto", 18), command=lambda:login_action(usernameEntry, passwordEntry, resultLabel, frameLogin))
    loginButton.place(x=300, y=330, anchor='w')

    # Botão de criar conta
    createaccButton = customtkinter.CTkButton(frameLogin,width=50,text="Create User", command=lambda:register_render(frameLogin))
    createaccButton.place(x=440, y=380, anchor='w')

    # Label New User
    NewUserLabel = customtkinter.CTkLabel(frameLogin, text="New User? Create an account!",font=("Roboto", 12))
    NewUserLabel.place(x=265,y=368)

    # Label para exibir resultados ou mensagens de erro
    resultLabel = customtkinter.CTkLabel(frameLogin, text="")
    resultLabel.place(x=280,y=430)

def confirm_music(musicNameEntry, musicAuthorEntry,musicCoverImg,musicAudioPathLabel, erroradd_musicLabel,strCategories):
    """Guarda os dados da música a adicionar"""
    
    global tempCoverName, tempAudioName  # Indicar as variáveis globais

    if musicNameEntry.get() and musicAuthorEntry.get() and tempAudioName and tempCoverName:
        #Variável com a estrutura de dados
        musicData = f"{musicNameEntry.get()};{musicAuthorEntry.get()};{strCategories.get()};0;{tempCoverName};{tempAudioName}\n"

        #Abre o caminho da música no formato "append" para adicionar a linha sem apagar o conteúdo existente
        with open(musicPath, "a", encoding="utf-8") as file:
            file.writelines(musicData) # escreve os dados com a estrutura anteriormente definida
            file.close
        
        write_notifications(musicNameEntry.get(), musicAuthorEntry.get(),"music")

        #Apagar conteúdo
        musicNameEntry.delete(0,"end")
        musicAuthorEntry.delete(0,"end")
        musicCoverImg.configure(image=None)
        musicAudioPathLabel.configure(text="")
        erroradd_musicLabel.configure(text="Music added with success!")

        tempCoverName = None
        tempAudioName = None

        return

    else:
        erroradd_musicLabel.configure(text="Fill all fields!")
        return

def select_file(musicCoverImg, musicAudioPathLabel):
    """Seleciona um ficheiro"""

    global tempCoverName, tempAudioName  # Indicar as variáveis globais

    if musicCoverImg == "" and musicAudioPathLabel != "":
        filePath = filedialog.askopenfilename(title="Select File", initialdir=".", filetypes=(("mp3 files", "*.mp3"), ("wav files", ".wav"))) # Escolher ficheiro, 

        shutil.copy(filePath, musicAudioPath) # Copia o aúdio escolhido para a pasta do aúdio da app

        tempAudioName = os.path.basename(filePath) # Guarda o nome do ficheiro de aúdio numa variável temporária

        musicAudioPathLabel.configure(text=f"{tempAudioName}") # Muda o texto da label para apresentar o aúdio

        print(musicAudioPath+tempAudioName) # Print para confirmação
    
    else:
        filePath = filedialog.askopenfilename(title="Select File", initialdir=".", filetypes=(("png files", "*.png"), ("jpg files", "*.jpg"))) #Escolher ficheiro, png ou jpg

        shutil.copy(filePath, coverArtPath) # Copia a imagem escolhido para a pasta de cover art da app

        coverImage = customtkinter.CTkImage(Image.open(filePath), size=(150,150)) # Abre a imagem escolhida

        tempCoverName = os.path.basename(filePath) # Guarda o nome do ficheiro da imagem numa variável temporária

        musicCoverImg.configure(image=coverImage) # Muda a imagem da label para a imagem escolhida

        print(coverArtPath+tempCoverName) # Print para confirmação
    
    return

def refresh_playlists(playlistScrollFrame):
    playLists = get_playlists()

    playlistScrollFrame.destroy()

    # Cria um scrollable frame dentro do frame principal
    playlistScrollFrame = customtkinter.CTkScrollableFrame(
        playlistMenuFrame,
        orientation="vertical",
        width=150,
        height=150,
        fg_color="transparent"
    )
    playlistScrollFrame.place(x=0, y=30)

    #Botão com Icone de playlist
    btnaddPlaylist1 = customtkinter.CTkButton(playlistScrollFrame, image=addIcon, width=31, height=31, fg_color="transparent", text="Add Playlist", command=new_playlist)
    btnaddPlaylist1.grid(row=0, column=0,sticky="w")

    for i in range(len(playLists)):
        #Botão com Icone de playlist
        btnPlaylist1 = customtkinter.CTkButton(playlistScrollFrame,
                                               image=playlistIcon,
                                               width=31, height=31,
                                               fg_color="transparent",
                                               text=f"{playLists[i]}",
                                               command=lambda playlistName=playLists[i]:playlist_page_render(mainContentFrame,currentFrame,playlistName))
        btnPlaylist1.grid(row=i+1, column=0,sticky="w")

def get_playlists():
    """Gets the playlists from files by username and returns them in a list"""

    playlistPath = f"{usersPath}{usernameFinal}{pathFormat}playlists" # Caminho para o diretório onde são armazenadas as playlists

    playlists = []
    try:
        # Para cada ficheiro no diretório
        for fileName in os.listdir(playlistPath):
            # Verificar se é ficheiro 
            if os.path.isfile(os.path.join(playlistPath, fileName)):
                # Remove a extensão (últimos 4 caracteres)
                playlists.append(fileName[:-4])
        return playlists
    except Exception as e:
        print(f"Error reading directory: {e}")
        return []

def update_music_info(musicNameNew, musicAuthorNew,coverArtNew):
    """Atualiza as informações da música na interface."""
    musicName.configure(text=musicNameNew)
    artistName.configure(text=musicAuthorNew)
    musicCover.configure(image=coverArtNew,fg_color="transparent")

def update_slider():
    """Atualiza o slider de progresso da música."""
    if mixer.music.get_busy():
        current_time = mixer.music.get_pos() // 1000  # Em segundos
        musicLenSlider.set(current_time)
    app.after(100, update_slider)  # Atualiza a cada 200ms

def adjust_volume(event=None):
    """Ajusta o volume da música baseado no slider."""
    volume = volumeSlider.get() / 100  # Converte para intervalo de 0 a 1
    mixer.music.set_volume(volume)

def play_music(index, playlist):
    """Inicia a reprodução da música com base no índice e na playlist selecionados."""
    global currentIndex, currentPlaylist, isPaused

    # Atualiza a playlist e o índice
    currentPlaylist = playlist
    currentIndex = index

    # Acessa a música correspondente ao índice na playlist
    music = currentPlaylist[currentIndex]
    musicName = music[0]
    musicAuthor = music[1]
    musicCover = coverArtPath + music[4]
    musicURL = music[5]

    # Atualiza a interface e inicia a música
    coverArt = customtkinter.CTkImage(Image.open(musicCover), size=(52, 52))
    play_music_audio(musicURL, musicName, musicAuthor, coverArt)

    # Atualiza as informações da interface
    update_music_info(musicName, musicAuthor, coverArt)
    update_slider()
    increment_music_views(musicName, musicAuthor)
    update_recent_songs_file(musicName, musicAuthor)

    # Altera o botão de play para pause
    btnPlay.configure(image=pauseIcon)
    isPaused = False

def play_music_audio(musicURL, musicName, musicAuthor, coverArt):
    """Inicia a reprodução da música, usando mixer para tocar o áudio."""
    global isPaused, isFavorite, musicNameCurrent, musicAuthorCurrent

    mixer.init()
    mixer.music.load(musicAudioPath+musicURL)  # Carrega a música
    mixer.music.play(loops=0)   # Toca a música uma vez

    musicNameCurrent = musicName
    musicAuthorCurrent = musicAuthor

    isFavorite = check_favorite(musicName,musicAuthor,usernameFinal)

    if isFavorite:
        likeBtn.configure(image=favoriteIcon)
    else:
        likeBtn.configure(image=noFavoriteIcon)

    # Atualiza as informações de música no GUI
    update_music_info(musicName, musicAuthor, coverArt)
    musicLenSlider.configure(to=get_music_length(musicURL))  # Configura o slider de progresso
    isPaused = False  # Assume que a música começa não pausada


def update_music_info_safe(name, author, cover_art):
    currentFrame.after(0, update_music_info, name, author, cover_art)

def play_next():
    """Toca a próxima música da playlist."""
    global currentIndex, currentPlaylist

    # Incrementa o índice para a próxima música
    currentIndex += 1

    # Verifica se o índice não ultrapassa o tamanho da playlist
    if currentIndex >= len(currentPlaylist):
        currentIndex = 0  # Volta para a primeira música se atingir o final

    # Chama a função play_music, passando o índice e a playlist
    play_music(currentIndex, currentPlaylist)

def play_previous():
    """Toca a música anterior da playlist."""
    global currentIndex, currentPlaylist

    # Decrementa o índice para a música anterior
    currentIndex -= 1

    # Verifica se o índice é menor que 0 (primeira música), caso em que vai para a última música
    if currentIndex < 0:
        currentIndex = len(currentPlaylist) - 1  # Vai para a última música da playlist

    # Chama a função play_music, passando o índice e a playlist
    play_music(currentIndex, currentPlaylist)


def update_recent_songs_file(musicName, musicAuthor):
    """Updates the recent songs file to ensure uniqueness and maintain order."""
    songInfo = f"{musicName};{musicAuthor}\n"
    activityPath = f"{usersPath}{usernameFinal}{pathFormat}music_activity.csv"

    # Read all lines from the file
    try:
        with open(activityPath, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    # Remove the song if it already exists
    lines = [line for line in lines if line != songInfo]

    # Insert the new song at the beginning
    lines.insert(0, songInfo)

    # Ensure only the last 8 songs are kept
    lines = lines[:8]

    # Write back the updated list to the file
    with open(activityPath, "w", encoding="utf-8") as file:
        file.writelines(lines)

def increment_music_views(musicName, musicAuthor):
    """Incrementa o número de visualizações para a música tocada."""
    global musicPath  # Caminho para o arquivo de músicas

    # Lê o conteúdo atual do arquivo
    with open(musicPath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Atualiza a linha correspondente
    updatedLines = []
    for line in lines:
        fields = line.strip().split(";")  # Divide os campos da linha
        if fields[0] == musicName and fields[1] == musicAuthor:
            fields[3] = str(int(fields[3]) + 1)  # Incrementa visualizações

        # Reconstrói a linha manualmente
        updatedLine = fields[0] + ";" + fields[1] + ";" + fields[2] + ";" + fields[3] + ";" + fields[4] + ";" + fields[5]
        updatedLines.append(updatedLine)

    # Escreve o conteúdo atualizado de volta no arquivo
    with open(musicPath, "w", encoding="utf-8") as file:
        for updatedLine in updatedLines:
            file.write(updatedLine + "\n")

def new_playlist():
    """Abre um frame para adicionar playlists"""

    # Frame para adicionar playlist
    playlistCreateFrame = customtkinter.CTkFrame(app, width=appWidth-246, height=916,fg_color="#0A090C")
    playlistCreateFrame.place(x=215, y=430)  # Abre o frame no canto superior direito

    # ----------------------------[Nome da Playlist]--------------------------------#

    # Label para mostrar o texto "Nome da Playlist:"
    playListNameLabel = customtkinter.CTkLabel(playlistCreateFrame, text="Playlist Name:")
    playListNameLabel.pack(expand=True, padx=20)

    # Entry para o nome da música
    playListNameEntry = customtkinter.CTkEntry(playlistCreateFrame)
    playListNameEntry.pack(expand=True, padx=20)

    # ----------------------------------------------------------------------------#

    # Botão para salvar os dados
    confirmBtn = customtkinter.CTkButton(
        playlistCreateFrame,
        width=100,
        height=50,
        text="Create",
        command=lambda: create_playlist(playListNameEntry.get(), playlistCreateFrame, errorLabel)  # Retrieve value when clicked
    )
    confirmBtn.pack(expand=True, pady=20)

    # Botão para cancelar
    cancBtn = customtkinter.CTkButton(
        playlistCreateFrame,
        width=100,
        height=50,
        text="Cancel",
        command=lambda: playlistCreateFrame.destroy()  # Retrieve value when clicked
    )
    cancBtn.pack(expand=True, pady=5)

    errorLabel = customtkinter.CTkLabel(playlistCreateFrame, text="")
    errorLabel.pack(expand=True, pady=5)

def edit_music_render(tree):
    """Abre um frame para editar música"""

    rowId = tree.focus()

    line = tree.item(rowId)

    if not rowId:
        print("No row selected!")
        return

    oldMusicName = line["values"][0]
    oldArtistName = line["values"][1]
    oldCategory = line["values"][2]

    #Frame para adicionar música
    editFrame = customtkinter.CTkFrame(app, width=appWidth-246, height=916, border_width=2, border_color="white", fg_color="#0A090C")
    editFrame.place(x=1180,y=180) #Abre o frame no canto superior direito
    
    #----------------------------[Nome da Música]--------------------------------#

    #Label para mostar o texto "Music Name:"
    musicNameLabel = customtkinter.CTkLabel(editFrame, text="Music Name:")
    musicNameLabel.grid(row=0,column=0, pady=20, padx=10)
    
    musicNameNew = customtkinter.StringVar()
    musicNameNew.set(oldMusicName)

    #Entry para o nome da música
    musicNameEntry = customtkinter.CTkEntry(editFrame, textvariable=musicNameNew)
    musicNameEntry.grid(row=0,column=1, padx=10)

    #----------------------------------------------------------------------------#

    #----------------------------[Autor da Música]-------------------------------#
    
    #Label para mostrar o texto "Author:"
    musicAuthorLabel = customtkinter.CTkLabel(editFrame, text="Author:")
    musicAuthorLabel.grid(row=1,column=0)

    musicAuthorNew = customtkinter.StringVar()
    musicAuthorNew.set(oldArtistName)

    #Entry para o nome do autor
    musicAuthorEntry = customtkinter.CTkEntry(editFrame, textvariable=musicAuthorNew)
    musicAuthorEntry.grid(row=1,column=1)

    #----------------------------------------------------------------------------#

    #----------------------------[Categoria Música]------------------------------#

    categoriesList = get_categories()

    strCategories = customtkinter.StringVar()
    strCategories.set(oldCategory)

    #Label para mostrar o texto "Category:"
    categoriesLabel = customtkinter.CTkLabel(editFrame, text="Category:")
    categoriesLabel.grid(row=2,column=0, pady=20)

    categoriesCombo = customtkinter.CTkComboBox(editFrame,variable=strCategories,values=categoriesList, width=100, command="")
    categoriesCombo.grid(row=2, column=1)

    #----------------------------------------------------------------------------#

    #--------------------------------------------------------------------------#


    #Botão para salvar a os dados
    confirmBtn = customtkinter.CTkButton(editFrame, width=160, height=30, text="Confirm", command=lambda:edit_music_refresh(musicNameNew, musicAuthorNew, strCategories, tree))
    confirmBtn.grid(row=3,column=0, columnspan=2)

    #Botão para salvar a os dados
    cancelBtn = customtkinter.CTkButton(editFrame, width=160, height=30, text="Cancel", command=lambda:editFrame.destroy())
    cancelBtn.grid(row=4,column=0, columnspan=2)

    #Label para mostrar erros
    erroradd_musicLabel = customtkinter.CTkLabel(editFrame, text="")
    erroradd_musicLabel.grid(row=5,column=0, columnspan=2)

def edit_music_refresh(oldMusicName, oldArtistName, oldCategory, tree):
    edit_music(oldMusicName, oldArtistName, oldCategory,tree)
    refresh_tree(tree,"music")

def add_music():
    """Abre um frame para adicionar músicas"""

    #Frame para adicionar música
    musicFrame = customtkinter.CTkFrame(app, width=appWidth-246, height=916, border_width=2, border_color="white", fg_color="#0A090C")
    musicFrame.place(x=1180,y=100) #Abre o frame no canto superior direito
    
    #----------------------------[Nome da Música]--------------------------------#

    #Label para mostar o texto "Music Name:"
    musicNameLabel = customtkinter.CTkLabel(musicFrame, text="Music Name:")
    musicNameLabel.grid(row=0,column=0, pady=20, padx=10)

    #Entry para o nome da música
    musicNameEntry = customtkinter.CTkEntry(musicFrame)
    musicNameEntry.grid(row=0,column=1, padx=10)

    #----------------------------------------------------------------------------#


    #----------------------------[Autor da Música]-------------------------------#
    
    #Label para mostrar o texto "Author:"
    musicAuthorLabel = customtkinter.CTkLabel(musicFrame, text="Author:")
    musicAuthorLabel.grid(row=1,column=0)

    #Entry para o nome do autor
    musicAuthorEntry = customtkinter.CTkEntry(musicFrame)
    musicAuthorEntry.grid(row=1,column=1)

    #----------------------------------------------------------------------------#

    #----------------------------[Categoria Música]------------------------------#

    categoriesList = get_categories()

    strCategories = customtkinter.StringVar()
    strCategories.set(categoriesList[0])

    #Label para mostrar o texto "Category:"
    categoriesLabel = customtkinter.CTkLabel(musicFrame, text="Category:")
    categoriesLabel.grid(row=2,column=0)

    categoriesCombo = customtkinter.CTkComboBox(musicFrame,variable=strCategories,values=categoriesList, width=100, command="")
    categoriesCombo.grid(row=2, column=1)

    #----------------------------------------------------------------------------#

    #----------------------------[Imagem da Música]------------------------------#
    
    #Label para mostrar o texto "Cover Art:"
    musicCoverLabel = customtkinter.CTkLabel(musicFrame, text="Cover Art:")
    musicCoverLabel.grid(row=3,column=0, columnspan=2)

    #Label para mostrar a imagem escolhida
    musicCoverImg = customtkinter.CTkLabel(musicFrame, text="")
    musicCoverImg.grid(row=4,column=0, columnspan=2)

    #Botão para escolher a imagem da música
    musicCoverBtn = customtkinter.CTkButton(musicFrame, width=200, height=50, text="Add cover art", command=lambda:select_file(musicCoverImg, ""))
    musicCoverBtn.grid(row=5,column=0, columnspan=2)

    #--------------------------------------------------------------------------#


    #----------------------------[Aúdio da Música]-----------------------------#
    
    #Label para mostrar a o texto "Audio:"
    musicAudioLabel = customtkinter.CTkLabel(musicFrame, text="Audio:")
    musicAudioLabel.grid(row=6,column=0, columnspan=2)

    #Label para mostrar o aúdio a ser adicionado
    musicAudioPathLabel = customtkinter.CTkLabel(musicFrame, text="")
    musicAudioPathLabel.grid(row=7,column=0, columnspan=2)

    #Botão para escolher o aúdio
    musicAudioBtn = customtkinter.CTkButton(musicFrame, width=200, height=50, text="Add audio", command=lambda:select_file("", musicAudioPathLabel))
    musicAudioBtn.grid(row=8,column=0, columnspan=2, pady=10)

    #--------------------------------------------------------------------------#


    #Botão para salvar a os dados
    confirmBtn = customtkinter.CTkButton(musicFrame, width=160, height=30, text="Confirm", command=lambda:confirm_music(musicNameEntry, musicAuthorEntry,musicCoverImg,musicAudioPathLabel, erroradd_musicLabel,strCategories))
    confirmBtn.grid(row=9,column=0, columnspan=2)

    #Botão para salvar a os dados
    cancelBtn = customtkinter.CTkButton(musicFrame, width=160, height=30, text="Cancel", command=lambda:musicFrame.destroy())
    cancelBtn.grid(row=10,column=0, columnspan=2)

    #Label para mostrar erros
    erroradd_musicLabel = customtkinter.CTkLabel(musicFrame, text="")
    erroradd_musicLabel.grid(row=11,column=0, columnspan=2)

def confirm_episode_refresh(episodeNameEntry, strPodcast,episodeUrlEntry, erroradd_episodeLabel,tree):
    confirm_episode(episodeNameEntry, strPodcast,episodeUrlEntry, erroradd_episodeLabel)
    refresh_tree(tree,"episodes")

def add_episode(tree):
    """Abre um frame para adicionar músicas"""

    #Frame para adicionar música
    episodeFrame = customtkinter.CTkFrame(app, width=appWidth-246, height=916, border_width=2, border_color="white", fg_color="#0A090C")
    episodeFrame.place(x=1180,y=120) #Abre o frame no canto superior direito
    
    #----------------------------[Nome da Música]--------------------------------#

    #Label para mostar o texto "episode Name:"
    episodeNameLabel = customtkinter.CTkLabel(episodeFrame, text="Episode Name:")
    episodeNameLabel.grid(row=0,column=0, pady=20, padx=10)

    #Entry para o nome da música
    episodeNameEntry = customtkinter.CTkEntry(episodeFrame)
    episodeNameEntry.grid(row=0,column=1, padx=10)

    #----------------------------------------------------------------------------#


    #----------------------------[Autor da Música]-------------------------------#
    
    podcastList = get_podcast_combo()

    #Label para mostrar o texto "Author:"
    episodeAuthorLabel = customtkinter.CTkLabel(episodeFrame, text="episode:")
    episodeAuthorLabel.grid(row=1,column=0)

    strPodcast = customtkinter.StringVar()
    strPodcast.set(podcastList[0])
    #Entry para o nome do autor
    episodeCombo = customtkinter.CTkComboBox(episodeFrame, variable=strPodcast,values=podcastList,width=130)
    episodeCombo.grid(row=1,column=1,pady=20)

    #--------------------------------------------------------------------------#

    #----------------------------[Autor da Música]-------------------------------#
    
    #Label para mostrar o texto "Author:"
    episodeUrlLabel = customtkinter.CTkLabel(episodeFrame, text="URL:")
    episodeUrlLabel.grid(row=2,column=0)

    #Entry para o nome do autor
    episodeUrlEntry = customtkinter.CTkEntry(episodeFrame)
    episodeUrlEntry.grid(row=2,column=1)

    #--------------------------------------------------------------------------#

    #Botão para salvar a os dados
    confirmBtn = customtkinter.CTkButton(episodeFrame, width=160, height=30, text="Confirm", command=lambda:confirm_episode_refresh(episodeNameEntry, strPodcast,episodeUrlEntry, erroradd_episodeLabel,tree))
    confirmBtn.grid(row=3,column=0, columnspan=2,pady=20)

    #Botão para salvar a os dados
    cancelBtn = customtkinter.CTkButton(episodeFrame, width=160, height=30, text="Cancel", command=lambda:episodeFrame.destroy())
    cancelBtn.grid(row=4,column=0, columnspan=2)

    #Label para mostrar erros
    erroradd_episodeLabel = customtkinter.CTkLabel(episodeFrame, text="")
    erroradd_episodeLabel.grid(row=11,column=0, columnspan=2)

def add_podcast(tree):
    """Abre um frame para adicionar músicas"""

    #Frame para adicionar música
    podcastFrame = customtkinter.CTkFrame(app, width=appWidth-246, height=916, border_width=2, border_color="white", fg_color="#0A090C")
    podcastFrame.place(x=1180,y=100) #Abre o frame no canto superior direito
    
    #----------------------------[Nome da Música]--------------------------------#

    #Label para mostar o texto "podcast Name:"
    podcastNameLabel = customtkinter.CTkLabel(podcastFrame, text="podcast Name:")
    podcastNameLabel.grid(row=0,column=0, pady=20, padx=10)

    #Entry para o nome da música
    podcastNameEntry = customtkinter.CTkEntry(podcastFrame)
    podcastNameEntry.grid(row=0,column=1, padx=10)

    #----------------------------------------------------------------------------#


    #----------------------------[Autor da Música]-------------------------------#
    
    #Label para mostrar o texto "Author:"
    podcastAuthorLabel = customtkinter.CTkLabel(podcastFrame, text="Author:")
    podcastAuthorLabel.grid(row=1,column=0)

    #Entry para o nome do autor
    podcastAuthorEntry = customtkinter.CTkEntry(podcastFrame)
    podcastAuthorEntry.grid(row=1,column=1)

    #----------------------------------------------------------------------------#

    #----------------------------[Imagem do Podcast]------------------------------#
    
    #Label para mostrar o texto "Cover Art:"
    podcastCoverLabel = customtkinter.CTkLabel(podcastFrame, text="Cover Art:")
    podcastCoverLabel.grid(row=3,column=0, columnspan=2)

    #Label para mostrar a imagem escolhida
    podcastCoverImg = customtkinter.CTkLabel(podcastFrame, text="")
    podcastCoverImg.grid(row=4,column=0, columnspan=2)

    #Botão para escolher a imagem do podcast
    podcastCoverBtn = customtkinter.CTkButton(podcastFrame, width=200, height=50, text="Add cover art", command=lambda:select_file(podcastCoverImg, ""))
    podcastCoverBtn.grid(row=5,column=0, columnspan=2)


    #--------------------------------------------------------------------------#


    #Botão para salvar a os dados
    confirmBtn = customtkinter.CTkButton(podcastFrame, width=160, height=30, text="Confirm", command=lambda:confirm_podcast(podcastNameEntry, podcastAuthorEntry,podcastCoverImg, erroradd_podcastLabel,tree))
    confirmBtn.grid(row=9,column=0, columnspan=2,pady=15)

    #Botão para salvar a os dados
    cancelBtn = customtkinter.CTkButton(podcastFrame, width=160, height=30, text="Cancel", command=lambda:podcastFrame.destroy())
    cancelBtn.grid(row=10,column=0, columnspan=2)

    #Label para mostrar erros
    erroradd_podcastLabel = customtkinter.CTkLabel(podcastFrame, text="")
    erroradd_podcastLabel.grid(row=11,column=0, columnspan=2)

def confirm_podcast(podcastNameEntry, podcastAuthorEntry,podcastCoverImg, erroradd_podcastLabel,tree):
    """Guarda os dados da música a adicionar"""
    
    global tempCoverName, tempAudioName  # Indicar as variáveis globais

    if podcastNameEntry.get() and podcastAuthorEntry.get() and tempCoverName:
        #Variável com a estrutura de dados
        podcastData = f"{podcastNameEntry.get()};{podcastAuthorEntry.get()};{tempCoverName}\n"

        #Abre o caminho da música no formato "append" para adicionar a linha sem apagar o conteúdo existente
        with open(podcastPath, "a", encoding="utf-8") as file:
            file.writelines(podcastData) # escreve os dados com a estrutura anteriormente definida
            file.close

        write_notifications(podcastNameEntry.get(), podcastAuthorEntry.get(),"podcast")

        #Apagar conteúdo
        podcastNameEntry.delete(0,"end")
        podcastAuthorEntry.delete(0,"end")
        podcastCoverImg.configure(image=None)
        erroradd_podcastLabel.configure(text="podcast added with success!")

        tempCoverName = None
        tempAudioName = None
        refresh_tree(tree, "podcast")
        return

    else:
        erroradd_podcastLabel.configure(text="Fill all fields!")
        return

def toggle_favorites(musicNameCurrent,musicAuthorCurrent,usernameFinal):
    global isFavorite

    if not isFavorite:
        isFavorite=True
        likeBtn.configure(image=favoriteIcon)
        add_favorites(musicNameCurrent,musicAuthorCurrent,usernameFinal)
    else:
        isFavorite=False
        likeBtn.configure(image=noFavoriteIcon)
        remove_favorite(musicNameCurrent, musicAuthorCurrent, usernameFinal)

def get_notification(type):
    if type == "custom":
        with open(customNotificationFile, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines:
            returnString = line.strip()

        return returnString
    else:
        notificationList = []

        with open(autoNotificationFile, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines:
            fields = line.strip().split(";")
            if fields[0] == type:
                notificationList.append(fields[1])
                notificationList.append(fields[2])

        return notificationList

def get_type_notification(usernameFinal):
    acceptedNotifications=[]
    with open(f"{usersPath}{usernameFinal}{pathFormat}notification.csv", "r", encoding="utf-8") as file:
        lines=file.readlines()

    for line in lines:
        acceptedNotifications.append(line.strip())
    
    return acceptedNotifications

def open_notifications():
    musicNotifications = get_notification("music")
    podcastNotifications=get_notification("podcast")
    customNotification = get_notification("custom")
    notificationType = get_type_notification(usernameFinal)

    messageString=""

    if "music" in notificationType:
        messageString+=f"New Music:{musicNotifications[0]} by {musicNotifications[1]}\n\n"
    if "podcast" in notificationType:
        messageString+=f"New Podcast:{podcastNotifications[0]} by {podcastNotifications[1]}\n\n"
    if "custom" in notificationType:
        messageString+=f"Message:{customNotification[0]} by {customNotification[1]}\n\n"
    if messageString=="":
        messageString="No Notifications to Show"

    close = CTkMessagebox.CTkMessagebox(app, width=700, height=500, title="Notifications", message=f"{messageString}",font=("Arial", 15),icon="", option_1="Close")

    response = close.get()

def mainwindow_render(oldFrame):
    """Rendriza a frame da janela principal"""

    global btnUser,playlistScrollFrame,favoriteIcon,noFavoriteIcon,likeBtn,mainContentFrame,currentFrame,nameFull,addIcon,playlistMenuFrame, musicName, artistName, musicLenSlider, volumeSlider, musicCover, playIcon, pauseIcon, btnPlay, playlistScrollFrame,playlistIcon # Variável global do frame em uso

    oldFrame.destroy() # Apagar o estilo do frame anterior

    #Frame menu lateral
    menuFrame = customtkinter.CTkFrame(app, width=246, height=916, fg_color="#0E0D11",corner_radius=0)  
    menuFrame.place(relx=0, rely=0,anchor="nw")
    
    #Frame de cima com a função de procurar e, para admin, entrar no dashboard
    upperSearchFrame = customtkinter.CTkFrame(app, width=appWidth, height=90, fg_color="#020202",corner_radius=0)  
    upperSearchFrame.place(x=246,y=0)

    #Frame para o conteúdo principal
    mainContentFrame = customtkinter.CTkFrame(app, width=appWidth-246, height=appHeight-221, fg_color="#000000",corner_radius=0)  
    mainContentFrame.place(x=246,y=90)

    #Search Bar na Upper Search Frame
    searchEntry = customtkinter.CTkEntry(
    upperSearchFrame,
    width=300,
    height=30,
    placeholder_text="Search...",
    justify="center",
    font=("Arial", 14),
    corner_radius=10,  
    border_width=0,
    fg_color="#333333",  
    text_color="#ffffff",  
    placeholder_text_color="#888888",
    )
    searchEntry.place(x=531, y=39, anchor="center")

    #Se o utilizador for admin, mostrar botão
    if isAdmin:
        #addBtn = customtkinter.CTkButton(upperSearchFrame, width=100, height=10, fg_color="transparent", text="Add Music", command=add_music)
        #addBtn.place(x=100, y=30)
        adminDashBtn = customtkinter.CTkButton(upperSearchFrame, width=100, height=10, fg_color="transparent", text="Admin dashboard", command=lambda:adminpage_render(mainContentFrame, currentFrame))
        adminDashBtn.place(x=100, y=30)

    #Frame barra inferior com os comandos da música
    playFrame = customtkinter.CTkFrame(app, width=1920, height=131, fg_color="#0A090C",corner_radius=0) 
    playFrame.place(relx=0, rely=1, anchor="sw")

    #Frame separador user e home
    upperMenuFrame = customtkinter.CTkFrame(menuFrame, width=162, height=110, fg_color="transparent") 
    upperMenuFrame.place(x=42,y=44)

    #Frame separador collection
    collectionMenuFrame = customtkinter.CTkFrame(menuFrame, width=162, height=165, fg_color="transparent") 
    collectionMenuFrame.place(x=42,y=191)

    #Frame separador playlists
    playlistMenuFrame = customtkinter.CTkFrame(menuFrame, width=170, height=659, fg_color="transparent")  
    playlistMenuFrame.place(x=42,y=395)

    ##################################IMAGENS PARA OS BUTTONS#############################################################
    ####################################### UpperMenuFrame ###############################################

    # Icon user
    userIcon = customtkinter.CTkImage(Image.open(f"{imagePath}user_icon.png"), size=(31, 31))

    # Icon home
    homeIcon = customtkinter.CTkImage(Image.open(f"{imagePath}home_icon.png"), size=(31, 31))

    # Icon música
    musicIcon = customtkinter.CTkImage(Image.open(f"{imagePath}music_icon.png"), size=(31, 31))

    # Icon artista
    artistIcon = customtkinter.CTkImage(Image.open(f"{imagePath}singer_icon.png"), size=(31, 31))

    # Icon Notificações
    notificationIcon = customtkinter.CTkImage(Image.open(f"{imagePath}bell_icon.png"), size=(31, 31))

    # Icon playlist
    playlistIcon = customtkinter.CTkImage(Image.open(f"{imagePath}playlist_icon.png"), size=(31, 31))

    # Icon add 
    addIcon = customtkinter.CTkImage(Image.open(f"{imagePath}add_icon.png"), size=(31, 31))

    noFavoriteIcon = customtkinter.CTkImage(Image.open(f"{imagePath}nofavorite_icon.png"), size=(31, 31))

    favoriteIcon = customtkinter.CTkImage(Image.open(f"{imagePath}favorite_icon.png"), size=(31, 31))

    ############################## APLICAÇAO DAS IMAGENS NOS BUTTONS E LAYERS PARA CADA BUTTON######################
    ############################################### UpperMenuFrame ###############################################

    notificationBtn = customtkinter.CTkButton(upperSearchFrame, width=35, height=35,text="",image=notificationIcon,fg_color="transparent",command=open_notifications)
    notificationBtn.place(x=1000, y=40, anchor="center")

    #Botão com Icon e texto de user
    btnUser = customtkinter.CTkButton(upperMenuFrame, image=userIcon, width=31, height=31, fg_color="transparent", text=f"{nameFull}",command=lambda:userpage_render(mainContentFrame, currentFrame))
    btnUser.place(x=0, y=0)

    #Botão com Icon e texto de home
    btnHome = customtkinter.CTkButton(upperMenuFrame, image= homeIcon , width = 31, height = 31, fg_color="transparent", text="Home Page", command=lambda:homepage_render(mainContentFrame, currentFrame))
    btnHome.place(x=0, y=65)

    #---------------------------------------------------------------------------------------------------------------------

    #Label para o separador collection
    labelCollection = customtkinter.CTkLabel(collectionMenuFrame, text="Collection")
    labelCollection.place(x=0, y=0) # Inicio do frame

    #Botão com Icon e texto de musica
    btnMusic = customtkinter.CTkButton(collectionMenuFrame, image=musicIcon, width=31, height=31, fg_color="transparent", text="Music",command=lambda:musicpage_render(mainContentFrame, currentFrame))
    btnMusic.place(x=0, y=30)

    #Botão com Icon e texto de podcast
    btnPodcast = customtkinter.CTkButton(collectionMenuFrame, image=artistIcon, width=31, height=31, fg_color="transparent", text="Podcast",command=lambda:podcastpage_render(mainContentFrame, currentFrame))
    btnPodcast.place(x=0, y=76)

    #Botão com Icon e texto de Favoritos
    btnFavorites = customtkinter.CTkButton(collectionMenuFrame, image=favoriteIcon, width=31, height=31, fg_color="transparent", text="Favorites",command=lambda:favoritepage_render(mainContentFrame,currentFrame))
    btnFavorites.place(x=0, y=122)

    #---------------------------------------------------------------------------------------------------------------------
    
    #Label para o separador playlists
    labelPlaylists = customtkinter.CTkLabel(playlistMenuFrame, text="Playlists")
    labelPlaylists.place(x=0, y=0) # Inicio do frame

    ####[PLAYLISTS, mudar para criar as playlists mais tarde]####

    # Cria um scrollable frame dentro do frame principal
    playlistScrollFrame = customtkinter.CTkScrollableFrame(
        playlistMenuFrame,
        orientation="vertical",
        width=150,
        height=150,
        fg_color="transparent"
    )
    playlistScrollFrame.place(x=0, y=30)

    refresh_playlists(playlistScrollFrame)

    #---------------------------------------------------------------------------------------------------------------------

    ##################################IMAGENS PARA OS BUTTONS#############################################################
    ####################################### PLAYFRAME ###############################################

    # Icon de play
    playIcon = customtkinter.CTkImage(Image.open(f"{imagePath}play_icon.png"), size=(34, 34))

    # Icon de pausa
    pauseIcon = customtkinter.CTkImage(Image.open(f"{imagePath}pause_icon.png"), size=(34, 34))

    # Icon de avançar música
    forwardIcon = customtkinter.CTkImage(Image.open(f"{imagePath}forward_icon.png"), size=(20, 20))

    # Icon de recuar música
    backIcon = customtkinter.CTkImage(Image.open(f"{imagePath}back_icon.png"), size=(20, 20))

    # Icon de áudio
    audioIcon = customtkinter.CTkImage(Image.open(f"{imagePath}audio_icon.png"), size=(20, 20)) 

    # Icon de pesquisa
    searchIcon = customtkinter.CTkImage(Image.open(f"{imagePath}search_icon.png"), size=(25, 25)) 

    ############################## APLICAÇAO DAS IMAGENS NOS BUTTONS E LAYERS PARA CADA BUTTON######################

    searchBtn = customtkinter.CTkButton(upperSearchFrame, width=31, height=31,image=searchIcon,text="",fg_color="transparent", command=lambda:search_frame(searchEntry,currentFrame))
    searchBtn.place(x=700, y=23)

    ############################################### FRAMES BARRA MUSICA ###############################################
    #Frame com conteúdo
    # Frame com conteúdo
    musicContentFrame = customtkinter.CTkFrame(playFrame, width=2000, height=70, fg_color="#0A090C")
    musicContentFrame.place(x=107, y=35)

    # Configurar o layout em grid com proporções
    musicContentFrame.columnconfigure(0, weight=1)  # Coluna para `showMusicFrame`
    musicContentFrame.columnconfigure(1, weight=1)  # Coluna para `musicActionFrame`
    musicContentFrame.columnconfigure(2, weight=1)  # Coluna para `audioSliderFrame`

    # Frame para mostrar música e info na barra inferior
    showMusicFrame = customtkinter.CTkFrame(musicContentFrame, fg_color="#0A090C", width=210)
    showMusicFrame.grid(row=0, column=0, sticky="nsew", padx=50, pady=5)  # Alinhado e espaçado

    # Frame dos botões para controlar música
    musicActionFrame = customtkinter.CTkFrame(musicContentFrame, fg_color="#0A090C",width=626, height=58)
    musicActionFrame.grid(row=0, column=1, sticky="nsew", padx=50, pady=5)  # Alinhado e espaçado

    # Frame slider de áudio
    audioSliderFrame = customtkinter.CTkFrame(musicContentFrame, fg_color="#0A090C",width=170, height=20)
    audioSliderFrame.grid(row=0, column=2, sticky="nsew", padx=50, pady=10)  # Alinhado e espaçado

    #-------------------------------------------------------------------------------------------------------

    #-------------------------------------[FRAME INFO]-------------------------------------------------------------

    likeBtn = customtkinter.CTkButton(playFrame,text="", width=35, height=35,image=noFavoriteIcon ,fg_color="transparent", command=lambda:toggle_favorites(musicNameCurrent,musicAuthorCurrent,usernameFinal))
    likeBtn.place(x=45,y=50)

    playListAddBtn = customtkinter.CTkButton(playFrame,text="", width=35, height=35,image=addIcon ,fg_color="transparent", command=add_playlist_render)
    playListAddBtn.place(x=95,y=50)

    #Frame para mostrar info: Nome da música e artista
    musicInfoFrame = customtkinter.CTkFrame(showMusicFrame, width=300, height=50, fg_color="#0A090C")
    musicInfoFrame.place(x=72, y=7)

    #Capa da Música (substituir por imagem)
    musicCover = customtkinter.CTkButton(showMusicFrame, width=53, height=53, text="",image="", fg_color="transparent")
    musicCover.place(x=0,y=0)

    #Nome da música
    musicName = customtkinter.CTkLabel(musicInfoFrame, text="No Music Playing", font=("Arial", 17))
    musicName.place(x=0, y=0)

    #Nome do artista
    artistName = customtkinter.CTkLabel(musicInfoFrame, text="", font=("Arial", 12) )
    artistName.place(x=0, y=24)

    #------------------------------------[FRAME CONTROLOS MÚSICA]---------------------------------------------------------------------------

    #Frame botões de controlo
    controlBtnFrame = customtkinter.CTkFrame(musicActionFrame, width=130, height=44, fg_color="#0A090C")
    controlBtnFrame.place(x=256, y=1)

    #Botão com Icone de recuar
    btnBack = customtkinter.CTkButton(controlBtnFrame, image=backIcon, width=20, height=20, fg_color="transparent", text="", command=play_previous)
    btnBack.place(x=0, y=7)

    #Botão com Icone de play
    btnPlay = customtkinter.CTkButton(controlBtnFrame, image=playIcon, width=34, height=34, fg_color="transparent", text="", command=toggle_play)
    btnPlay.place(x=40, y=0)

    #Botão com Icone de avançar
    btnForward = customtkinter.CTkButton(controlBtnFrame, image=forwardIcon, width=20, height=20, fg_color="transparent", text="", command=play_next)
    btnForward.place(x=94, y=7)

    #Slider da música
    musicLenSlider = customtkinter.CTkSlider(musicActionFrame,width=626, from_=0, to=100, number_of_steps=100)
    musicLenSlider.place(x=0, y=54)

    #-------------------------------------[FRAME SLIDER ÁUDIO]-------------------------------------------------------------------------

    #Botão com Icone do áudio
    btnAudio = customtkinter.CTkButton(audioSliderFrame, image=audioIcon, width=20, height=20, fg_color="transparent", text="",
    command=toggle_mute)
    btnAudio.place(x=0, y=0)

    #Slider de audio
    volumeSlider = customtkinter.CTkSlider(audioSliderFrame,width=100, from_=0, to=100, number_of_steps=100)
    volumeSlider.set(50)
    volumeSlider.place(x=40, y=8)

    # Associar o controlo de volume ao slider
    volumeSlider.bind("<B1-Motion>", adjust_volume)  # <B1-Motion>: Movimento com o botão do mouse pressionado
    volumeSlider.bind("<ButtonRelease-1>", adjust_volume)  # Para garantir ajuste no final

    homepage_render(mainContentFrame, currentFrame) # Mostra a homepage por defeito

def search_frame(searchEntry, oldFrame):
    """Search and display filtered results based on search input"""
    
    global currentFrame  # Global variable for the frame to be used

    if oldFrame != None:
        oldFrame.destroy()  # Destroy the previous frame's content

    search_query = searchEntry.get().lower()  # Get the text from the search entry and make it lowercase for case-insensitive search
    
    # Create a new frame for the playlist page
    playlistPageFrame = customtkinter.CTkFrame(
        mainContentFrame,
        width=1238,
        height=appHeight - (90 + 131),
        fg_color="black",
        corner_radius=0
    )
    playlistPageFrame.place(x=0, y=0)

    currentFrame = playlistPageFrame  # The current frame to be used is the playlistPageFrame

    # Frame for displaying music
    MusicFrame = customtkinter.CTkFrame(playlistPageFrame, width=1300, height=800, fg_color="transparent", corner_radius=0)
    MusicFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Scrollable frame for music items
    MusicScrollFrame = customtkinter.CTkScrollableFrame(
        MusicFrame,
        orientation="vertical",
        width=1200,
        height=500,
        fg_color="transparent"
    )
    MusicScrollFrame.place(x=100, y=50)

    MusicLabel = customtkinter.CTkLabel(MusicFrame, text=f"'{searchEntry.get()}' Results", font=("Roboto", 25))
    MusicLabel.place(x=20, y=10)

    # Get the music list and filter it based on the search query
    musicList = read_content("music")  # Get music data

    # Filter playlist items based on the search query
    filteredPlaylist = []
    for music in musicList:
        musicName = music[0].lower()  # Convert to lowercase for case-insensitive comparison
        musicAuthor = music[1].lower()
        musicCategory = music[2].lower()
        
        # Check if search query matches any field (name, author, or category)
        if search_query in musicName or search_query in musicAuthor or search_query in musicCategory:
            filteredPlaylist.append(music)

    # Loop to create buttons for filtered music items
    index = 0
    for music in filteredPlaylist:
        musicName = music[0]
        musicAuthor = music[1]
        musicCategory = music[2]
        musicViews = music[3]
        musicCover = coverArtPath + music[4]
        musicURL = music[5]

        coverArt = customtkinter.CTkImage(Image.open(musicCover), size=(150, 150))
        coverArt2 = customtkinter.CTkImage(Image.open(musicCover), size=(52, 52))

        button = customtkinter.CTkButton(
            MusicScrollFrame,
            width=150,
            height=150,
            text="",
            image=coverArt,
            fg_color="transparent",
            compound="top",
            command=lambda idx=index, playlist=filteredPlaylist: play_music(idx, playlist)
        )

        button.grid(row=index, column=0, padx=40, pady=20)

        nameLabel = customtkinter.CTkLabel(MusicScrollFrame, text=f"{musicName}")
        nameLabel.grid(row=index, column=1, padx=40, pady=20)

        authorLabel = customtkinter.CTkLabel(MusicScrollFrame, text=f"{musicAuthor}")
        authorLabel.grid(row=index, column=2, padx=40, pady=20)

        categoryLabel = customtkinter.CTkLabel(MusicScrollFrame, text=f"{musicCategory}")
        categoryLabel.grid(row=index, column=3, padx=40, pady=20)

        viewsLabel = customtkinter.CTkLabel(MusicScrollFrame, text=f"{musicViews} Views")
        viewsLabel.grid(row=index, column=4, padx=40, pady=20)

        index += 1  # Increment index for the next music


def userpage_render(mainContentFrame, oldFrame):
    """Mostra o frame da página de utilizador"""

    global currentFrame # Variável global para frame a ser usado

    oldFrame.destroy() # Apagar o estilo do frame anterior

    #Frame User Menu
    userFrame = customtkinter.CTkFrame(mainContentFrame, width=1674, height=890, fg_color="#000000",corner_radius=0)  
    userFrame.place(x=0,y=0)

    currentFrame = userFrame # O frame a ser usado passa a ser o userFrame

    #Frame Credentials
    credentialsFrame = customtkinter.CTkFrame(userFrame, width=542, height=250, corner_radius=10,fg_color="#000000")
    credentialsFrame.grid(row=0, column=0, padx=350)

    #Titulo
    title = customtkinter.CTkLabel(credentialsFrame, text="User Page", font=("Arial", 30),text_color="white")
    title.grid(row=0, column=0, columnspan=2,pady=20)

    # Label Nome
    labelName = customtkinter.CTkLabel(credentialsFrame, text=f"Name: {nameFull}", font=("Arial", 20),text_color="white")
    labelName.grid(row=1,column=0, columnspan=2,pady=10)
    
    # Label Username
    labelUsername = customtkinter.CTkLabel(credentialsFrame, text=f"Username: {usernameFinal}", font=("Arial", 20),text_color="white")
    labelUsername.grid(row=2,column=0, columnspan=2, pady=20)

    # Label Password
    labelPass = customtkinter.CTkLabel(credentialsFrame, text=f"Password: {'*' * len(passwordFinal)}", font=("Arial", 20),text_color="white")
    labelPass.grid(row=3,column=0, columnspan=2,pady=10)
    
    # Butao mudar 
    btnchgCred = customtkinter.CTkButton(credentialsFrame, width=150, height=30,text="Edit Profile",command=lambda:change_credentials(mainContentFrame, currentFrame))
    btnchgCred.grid(row=4,column=0, padx=20)

    btnLogout = customtkinter.CTkButton(credentialsFrame, width=100, height=30,text="Logout",command=logout,fg_color="red")
    btnLogout.grid(row=4, column=1,pady=20)

    #Frame Notificações
    notificationsFrame = customtkinter.CTkFrame(userFrame, width=542, height=250, corner_radius=10,fg_color="#000000")
    notificationsFrame.grid(row=1, column=0, padx=350, pady=50)

    notificationsLabel = customtkinter.CTkLabel(notificationsFrame,text="Notfications:", font=("Arial", 30))
    notificationsLabel.grid(row=0, column=0, padx=20, rowspan=3)

    #Variáveis checkbox
    checkVarMusic = customtkinter.StringVar(value="off")
    checkVarPodcast = customtkinter.StringVar(value="off")
    checkVarOthers = customtkinter.StringVar(value="off")

    set_check_var(usernameFinal, checkVarMusic, checkVarPodcast, checkVarOthers)

    #Checkboxes 
    checkboxMusic = customtkinter.CTkCheckBox(notificationsFrame, text="Musics", variable=checkVarMusic, onvalue="on", offvalue="off")
    checkboxPodcast = customtkinter.CTkCheckBox(notificationsFrame, text="Podcasts", variable=checkVarPodcast, onvalue="on", offvalue="off")
    checkboxOthers = customtkinter.CTkCheckBox(notificationsFrame, text="Others", variable=checkVarOthers, onvalue="on", offvalue="off")

    checkboxMusic.grid(row=0, column=1, pady=10)
    checkboxPodcast.grid(row=1, column=1, pady=10)
    checkboxOthers.grid(row=2, column=1, pady=10)

    #Botão preferências
    savePreferencesBtn = customtkinter.CTkButton(notificationsFrame, text="Save Preferences", command=lambda:save_preferences(usernameFinal, checkVarMusic, checkVarPodcast, checkVarOthers))
    savePreferencesBtn.grid(row=0,column=2, rowspan=3)

def logout():
    for widget in app.winfo_children():
        widget.destroy()
    login_render(currentFrame)

def change_credentials(mainContentFrame, oldFrame):
    """Mostra a pagina de mudar credenciais"""

    global currentFrame # Variável global para frame a ser usado

    oldFrame.destroy() # Apagar o estilo do frame anterior

    #Frame Home Page
    changeInfosFrame =customtkinter.CTkFrame(mainContentFrame, width=1674, height=890, fg_color="#000000",corner_radius=0)
    changeInfosFrame.place(x=0,y=0)

    currentFrame = changeInfosFrame # O frame a ser usado passa a ser o changeInfosFrame

    Title = customtkinter.CTkLabel(changeInfosFrame, text="Change Your Credentials", font=("Arial", 30))
    Title.place(x=400,y=30)

    nameEntry = customtkinter.CTkEntry(changeInfosFrame, placeholder_text="Name...",width=310)
    nameEntry.place(x=400,y=200)

    usernameEntry = customtkinter.CTkEntry(changeInfosFrame, placeholder_text="Username...",width=310)
    usernameEntry.place(x=400,y=300)

    confirmBtn = customtkinter.CTkButton(changeInfosFrame, width=100, height=30,text="Confirm", command=lambda:save_changes(usernameEntry,nameEntry,usernameFinal,nameFull))
    confirmBtn.place(x=400, y=500)

    cancelBtn = customtkinter.CTkButton(changeInfosFrame, width=100, height=30,text="Cancel",command=lambda:userpage_render(mainContentFrame, oldFrame))
    cancelBtn.place(x=600, y=500)


def save_changes(usernameEntry,nameEntry,oldUsername,oldName):
    global usernameFinal,nameFull,btnUser,isAdmin
    usernameFinal, nameFull = confirm_change(usernameEntry,nameEntry,usernameFinal,nameFull)
    btnUser.configure(text=f"{nameFull}")
    isAdmin = check_admin(usernameFinal)

def select_image():
    filename =filedialog.askopenfilename(title='select file',initialdir = 'images',filetypes=(('png files','*.png'),('gif files','*.gif'),('all files','*.*')))

def read_content(contentType):
    if contentType == "podcast":
        with open(podcastPath, "r", encoding="utf-8") as file:
            podcastList = file.readlines()
        return podcastList
    elif contentType == "music":
        with open(musicPath, "r", encoding="utf-8") as file:
            lines = file.readlines()

def create_playlist(playListName, playlistCreateFrame, errorLabel):
    """Cria uma playlist com o nome pedido pelo utilizador"""
    playlistPath = f"{usersPath}{usernameFinal}{pathFormat}playlists{pathFormat}{playListName}.csv" # Caminho para o diretório onde são armazenadas as playlists

    if playListName == " " or playListName == "":
        errorLabel.configure(text="Playlist name can't be empty!")
        return
    
    elif playListName+".csv" in os.listdir(f"{usersPath}{usernameFinal}{pathFormat}playlists"):
        errorLabel.configure(text="Playlist already exists!")
        return

    else:
        with open(playlistPath, "w", encoding="utf-8") as file:
            pass

        refresh_playlists(playlistScrollFrame)

        playlistCreateFrame.destroy()

def manage_music_render(mainContentFrame, oldFrame):
    """Mostra a pagina de gerir musicas"""

    global currentFrame # Variável global para frame a ser usado

    if oldFrame != None:
        oldFrame.destroy() # Apagar o estilo do frame anterior

    #Frame Home Page
    musicManageFrame = customtkinter.CTkScrollableFrame(mainContentFrame,
	orientation="vertical",
	width=1238,
	height=appHeight-(90+131),
	fg_color="black",
	corner_radius = 0
	)
    musicManageFrame.place(x=0,y=0)

    currentFrame = musicManageFrame # O frame a ser usado passa a ser o userFrame

    #Label para mostrar o texto "Admin Dashboard"
    trendingLabel = customtkinter.CTkLabel(musicManageFrame, text="Manage Musics", font=("Roboto", 30))
    trendingLabel.grid(row=0, column=0,padx=20, pady=20, sticky="nsew")

    #Botão para gerir músicas
    manageMusicsbtn = customtkinter.CTkButton(musicManageFrame, width=200, height=50, text="Add Music", command=add_music)
    manageMusicsbtn.grid(row=1, column=1, padx=0, pady=10, sticky="w")

    #Botão para gerir músicas
    editMusicBtn = customtkinter.CTkButton(musicManageFrame, width=200, height=50, text="Edit Music", command=lambda:edit_music_render(tree))
    editMusicBtn.grid(row=2, column=1, padx=0, pady=10, sticky="w")

    #Botão para gerir músicas
    deleteMusicBtn = customtkinter.CTkButton(musicManageFrame, width=200, height=50, text="Delete Music", command=lambda:delete_type(tree, "music"))
    deleteMusicBtn.grid(row=3, column=1, padx=0, pady=10, sticky="w")

    # define columns
    columns = ('music_name', 'artist_name','category', 'views')

    tree = ttk.Treeview(musicManageFrame, columns=columns, show='headings')

    # define headings
    tree.heading('music_name', text='Music Name')
    tree.heading('artist_name', text='Artist')
    tree.heading('category', text='Category')
    tree.heading('views', text='Views')

    tree.grid(row=1,rowspan=3, column=0,padx=70, pady=20,  sticky='nsew')

    refresh_tree(tree,"music")

def manage_podcast_render(mainContentFrame, oldFrame):
    """Mostra a pagina de gerir podcasts"""

    global currentFrame # Variável global para frame a ser usado

    if oldFrame != None:
        oldFrame.destroy() # Apagar o estilo do frame anterior

    #Frame Home Page
    podcastManageFrame = customtkinter.CTkScrollableFrame(mainContentFrame,
	orientation="vertical",
	width=1238,
	height=appHeight-(90+131),
	fg_color="black",
	corner_radius = 0
	)
    podcastManageFrame.place(x=0,y=0)

    currentFrame = podcastManageFrame # O frame a ser usado passa a ser o userFrame

    #Label para mostrar o texto "Admin Dashboard"
    trendingLabel = customtkinter.CTkLabel(podcastManageFrame, text="Manage Podcasts", font=("Roboto", 30))
    trendingLabel.grid(row=0, column=0,padx=20, pady=20, sticky="nsew")

    #Botão para gerir músicas
    managepodcastsbtn = customtkinter.CTkButton(podcastManageFrame, width=200, height=50, text="Add Podcast", command=lambda:add_podcast(tree))
    managepodcastsbtn.grid(row=1, column=1, padx=0, pady=10, sticky="w")

    #Botão para gerir músicas
    deletepodcastBtn = customtkinter.CTkButton(podcastManageFrame, width=200, height=50, text="Delete Podcast", command=lambda:delete_type(tree,"podcast"))
    deletepodcastBtn.grid(row=3, column=1, padx=0, pady=10, sticky="w")

    # define columns
    columns = ('podcast_name', 'host_name')

    tree = ttk.Treeview(podcastManageFrame, columns=columns, show='headings')

    # define headings
    tree.heading('podcast_name', text='Podcast Name')
    tree.heading('host_name', text='Host')

    tree.grid(row=1,rowspan=3, column=0,padx=70, pady=20,  sticky='nsew')

    refresh_tree(tree, "podcast")

def manage_episodes_render(mainContentFrame, oldFrame):
    """Mostra a pagina de gerir episódios de podcasts"""

    global currentFrame # Variável global para frame a ser usado

    if oldFrame != None:
        oldFrame.destroy() # Apagar o estilo do frame anterior

    #Frame Home Page
    podcastManageFrame = customtkinter.CTkScrollableFrame(mainContentFrame,
	orientation="vertical",
	width=1238,
	height=appHeight-(90+131),
	fg_color="black",
	corner_radius = 0
	)
    podcastManageFrame.place(x=0,y=0)

    currentFrame = podcastManageFrame # O frame a ser usado passa a ser o userFrame

    #Label para mostrar o texto "Admin Dashboard"
    trendingLabel = customtkinter.CTkLabel(podcastManageFrame, text="Manage Podcasts Episodes", font=("Roboto", 30))
    trendingLabel.grid(row=0, column=0,padx=20, pady=20, sticky="nsew")

    #Botão para gerir músicas
    managepodcastsbtn = customtkinter.CTkButton(podcastManageFrame, width=200, height=50, text="Add Episode", command=lambda:add_episode(tree))
    managepodcastsbtn.grid(row=1, column=1, padx=0, pady=10, sticky="w")

    #Botão para gerir músicas
    deletepodcastBtn = customtkinter.CTkButton(podcastManageFrame, width=200, height=50, text="Delete Episode", command=lambda:delete_type(tree,"episodes"))
    deletepodcastBtn.grid(row=3, column=1, padx=0, pady=10, sticky="w")

    # define columns
    columns = ('episode_name', 'podcast_name', 'views', 'url')

    tree = ttk.Treeview(podcastManageFrame, columns=columns, show='headings')

    # define headings
    tree.heading('episode_name', text='Episode Name')
    tree.heading('podcast_name', text='Podcast Name')
    tree.heading('views', text='Views')
    tree.heading('url', text='URL')

    tree.grid(row=1,rowspan=3, column=0,padx=70, pady=20,  sticky='nsew')

    refresh_tree(tree, "episodes")

def manage_users_render(mainContentFrame, oldFrame):
    """Mostra a pagina de gerir podcasts"""

    global currentFrame # Variável global para frame a ser usado

    if oldFrame != None:
        oldFrame.destroy() # Apagar o estilo do frame anterior

    #Frame Home Page
    usersManageFrame = customtkinter.CTkScrollableFrame(mainContentFrame,
	orientation="vertical",
	width=1238,
	height=appHeight-(90+131),
	fg_color="black",
	corner_radius = 0
	)
    usersManageFrame.place(x=0,y=0)

    currentFrame = usersManageFrame # O frame a ser usado passa a ser o userFrame

    #Label para mostrar o texto "Admin Dashboard"
    trendingLabel = customtkinter.CTkLabel(usersManageFrame, text="Manage userss", font=("Roboto", 30))
    trendingLabel.grid(row=0, column=0,padx=20, pady=20, sticky="nsew")

    #Botão para gerir músicas
    deleteusersBtn = customtkinter.CTkButton(usersManageFrame, width=200, height=50, text="Delete users", command=lambda:delete_type(tree,"users"))
    deleteusersBtn.grid(row=3, column=1, padx=0, pady=10, sticky="w")

    # define columns
    columns = ('users_name', 'users_username', 'users_password')

    tree = ttk.Treeview(usersManageFrame, columns=columns, show='headings')

    # define headings
    tree.heading('users_name', text='Name')
    tree.heading('users_username', text='Username')
    tree.heading('users_password', text='Password')

    tree.grid(row=1,rowspan=3, column=0,padx=70, pady=20,  sticky='nsew')

    refresh_tree(tree, "users")

def manage_admins_render(mainContentFrame, oldFrame):
    """Mostra a pagina de gerir podcasts"""

    global currentFrame # Variável global para frame a ser usado

    if oldFrame != None:
        oldFrame.destroy() # Apagar o estilo do frame anterior

    #Frame Home Page
    usersManageFrame = customtkinter.CTkScrollableFrame(mainContentFrame,
	orientation="vertical",
	width=1238,
	height=appHeight-(90+131),
	fg_color="black",
	corner_radius = 0
	)
    usersManageFrame.place(x=0,y=0)

    currentFrame = usersManageFrame # O frame a ser usado passa a ser o userFrame

    #Label para mostrar o texto "Admin Dashboard"
    trendingLabel = customtkinter.CTkLabel(usersManageFrame, text="Manage Admins", font=("Roboto", 30))
    trendingLabel.grid(row=0, column=0,padx=20, pady=20, sticky="nsew")

    #Botão para gerir músicas
    manageusersBtn = customtkinter.CTkButton(usersManageFrame, width=200, height=50, text="Add admin", command=lambda:add_admin_render(tree))
    manageusersBtn.grid(row=1, column=1, padx=0, pady=10, sticky="w")

    #Botão para gerir músicas
    deleteusersBtn = customtkinter.CTkButton(usersManageFrame, width=200, height=50, text="Undo admin", command=lambda:delete_type(tree,"admin"))
    deleteusersBtn.grid(row=3, column=1, padx=0, pady=10, sticky="w")

    # define columns
    columns = ('username')

    tree = ttk.Treeview(usersManageFrame, columns=columns, show='headings')

    # define headings
    tree.heading('username', text='Username')

    tree.grid(row=1,rowspan=3, column=0,padx=70, pady=20,  sticky='nsew')

    notificationsText = customtkinter.CTkTextbox(usersManageFrame,width=200,height=200)
    notificationsText.grid(row=4, column=0, rowspan=2)

    saveNotBtn = customtkinter.CTkButton(usersManageFrame, width=200, height=50,text="Add Notification", command=lambda:save_notifications(notificationsText))
    deleteNotBtn = customtkinter.CTkButton(usersManageFrame, width=200, height=50,text="Delete Notifications", command=delete_notifications)
    saveNotBtn.grid(row=4, column=1)
    deleteNotBtn.grid(row=5, column=1)
    refresh_tree(tree, "admin")

def add_admin_render(tree):
    """Abre um frame para adicionar músicas"""

    #Frame para adicionar música
    adminFrame = customtkinter.CTkFrame(app, width=appWidth-246, height=916, border_width=2, border_color="white", fg_color="#0A090C")
    adminFrame.place(x=1180,y=120) #Abre o frame no canto superior direito
    
    #----------------------------[Nome da Música]--------------------------------#

    #Label para mostar o texto "episode Name:"
    adminLabel = customtkinter.CTkLabel(adminFrame, text="Enter username:")
    adminLabel.grid(row=0,column=0, pady=20, padx=10)

    #Entry para o nome da música
    adminEntry = customtkinter.CTkEntry(adminFrame)
    adminEntry.grid(row=0,column=1, padx=10)

    #---------------------------------------------------------------------------#

    #Botão para salvar a os dados
    confirmBtn = customtkinter.CTkButton(adminFrame, width=160, height=30, text="Confirm", command=lambda:confirm_admin_refresh(adminEntry, erroradd_adminLabel,tree))
    confirmBtn.grid(row=3,column=0, columnspan=2,pady=20)

    #Botão para salvar a os dados
    cancelBtn = customtkinter.CTkButton(adminFrame, width=160, height=30, text="Cancel", command=lambda:adminFrame.destroy())
    cancelBtn.grid(row=4,column=0, columnspan=2)

    #Label para mostrar erros
    erroradd_adminLabel = customtkinter.CTkLabel(adminFrame, text="")
    erroradd_adminLabel.grid(row=11,column=0, columnspan=2)

def confirm_admin_refresh(adminEntry, erroradd_adminLabel,tree):
    confirm_admin(adminEntry, erroradd_adminLabel)
    refresh_tree(tree, "admin")

def confirm_admin(adminEntry, erroradd_adminLabel):
    userCheck=[]

    with open(adminListfile, "r", encoding="utf-8") as file:
        lines=file.readlines()

    for line in lines:
        userCheck.append(line.strip())

    if adminEntry.get() in userCheck:
        erroradd_adminLabel.configure(text="User already admin")
        return
    
    with open(adminListfile, "a", encoding="utf-8") as file:
        file.write(adminEntry.get()+"\n")

    adminEntry.delete(0,"end")

    erroradd_adminLabel.configure(text=f"{adminEntry.get()} is now admin")


def add_playlist_render():
    playlistFrame=customtkinter.CTkFrame(app, height=170, width=170,fg_color="#0A090C")
    playlistFrame.place(x=150, y=500)

    # Cria um scrollable frame dentro do frame principal
    playlistScrollFrame = customtkinter.CTkScrollableFrame(
        playlistFrame,
        orientation="vertical",
        width=150,
        height=150,
        fg_color="transparent"
    )
    playlistScrollFrame.place(x=0, y=10)

    playLists = get_playlists()
    
    for i in range(len(playLists)):
        #Botão com Icone de playlist
        btnPlaylist1 = customtkinter.CTkButton(playlistScrollFrame,
                                               image=playlistIcon,
                                               width=31, height=31,
                                               fg_color="transparent",
                                               text=f"{playLists[i]}",
                                               command=lambda playlistName=playLists[i]:add_to_playlist(playlistName, playlistFrame))
        btnPlaylist1.grid(row=i, column=0,sticky="w")

def add_to_playlist(playlistName, playlistFrame):

    with open(f"{usersPath}{usernameFinal}{pathFormat}playlists{pathFormat}{playlistName}.csv", "r", encoding="utf-8") as file:
        lines=file.readlines()
    
    for line in lines:
        fields=line.strip().split(";")
        if fields[0] == musicNameCurrent and fields[1] == musicAuthorCurrent:
            return

    with open(f"{usersPath}{usernameFinal}{pathFormat}playlists{pathFormat}{playlistName}.csv", "a", encoding="utf-8") as file:
        file.write(f"{musicNameCurrent};{musicAuthorCurrent}\n")

    playlistFrame.destroy()

def manage_categories_render(mainContentFrame, oldFrame):
    """Mostra a pagina de gerir podcasts"""

    global currentFrame # Variável global para frame a ser usado

    if oldFrame != None:
        oldFrame.destroy() # Apagar o estilo do frame anterior

    #Frame Home Page
    categoriesManageFrame = customtkinter.CTkScrollableFrame(mainContentFrame,
	orientation="vertical",
	width=1238,
	height=appHeight-(90+131),
	fg_color="black",
	corner_radius = 0
	)
    categoriesManageFrame.place(x=0,y=0)

    currentFrame = categoriesManageFrame # O frame a ser usado passa a ser o userFrame

    #Label para mostrar o texto "Admin Dashboard"
    trendingLabel = customtkinter.CTkLabel(categoriesManageFrame, text="Manage Categories", font=("Roboto", 30))
    trendingLabel.grid(row=0, column=0,padx=20, pady=20, sticky="nsew")

    #Botão para gerir músicas
    managecategoriesBtn = customtkinter.CTkButton(categoriesManageFrame, width=200, height=50, text="Add Category", command=lambda:add_categories_render(tree))
    managecategoriesBtn.grid(row=1, column=1, padx=0, pady=10, sticky="w")

    #Botão para gerir músicas
    deletecategoriesBtn = customtkinter.CTkButton(categoriesManageFrame, width=200, height=50, text="Delete Category", command=lambda:delete_category(tree))
    deletecategoriesBtn.grid(row=3, column=1, padx=0, pady=10, sticky="w")

    # define columns
    columns = ('categories_name')

    tree = ttk.Treeview(categoriesManageFrame, columns=columns, show='headings')

    # define headings
    tree.heading('categories_name', text='Name')

    tree.grid(row=1,rowspan=3, column=0,padx=70, pady=20,  sticky='nsew')

    refresh_tree(tree, "categories")

def add_categories_render(tree):
    """Abre um frame para adicionar músicas"""

    #Frame para adicionar música
    categoriesFrame = customtkinter.CTkFrame(app, width=appWidth-246, height=916, border_width=2, border_color="white", fg_color="#0A090C")
    categoriesFrame.place(x=830,y=200) #Abre o frame no canto superior direito
    
    #----------------------------[Nome da Música]--------------------------------#

    #Label para mostar o texto "categories Name:"
    categoriesNameLabel = customtkinter.CTkLabel(categoriesFrame, text="Category Name:")
    categoriesNameLabel.grid(row=0,column=0, pady=20, padx=10)

    #Entry para o nome da música
    categoriesNameEntry = customtkinter.CTkEntry(categoriesFrame)
    categoriesNameEntry.grid(row=0,column=1, padx=10)

    #----------------------------------------------------------------------------#

    #Botão para salvar a os dados
    confirmBtn = customtkinter.CTkButton(categoriesFrame, width=160, height=30, text="Confirm", command=lambda:add_categories_refresh(categoriesNameEntry, erroradd_categoriesLabel,tree))
    confirmBtn.grid(row=9,column=0, columnspan=2,pady=15)

    #Botão para cancelar os dados
    cancelBtn = customtkinter.CTkButton(categoriesFrame, width=160, height=30, text="Cancel", command=lambda:categoriesFrame.destroy())
    cancelBtn.grid(row=10,column=0, columnspan=2)

    #Label para mostrar erros
    erroradd_categoriesLabel = customtkinter.CTkLabel(categoriesFrame, text="")
    erroradd_categoriesLabel.grid(row=11,column=0, columnspan=2)

def add_categories_refresh(categoriesNameEntry, erroradd_categoriesLabel,tree):
    confirm_categories(categoriesNameEntry, erroradd_categoriesLabel)
    refresh_tree(tree, "categories")

def adminpage_render(mainContentFrame, oldFrame):
    """Mostra a homepage"""

    global currentFrame # Variável global para frame a ser usado

    if oldFrame != None:
        oldFrame.destroy() # Apagar o estilo do frame anterior

    #Frame Home Page
    homepageFrame = customtkinter.CTkScrollableFrame(mainContentFrame,
	orientation="vertical",
	width=1238,
	height=appHeight-(90+131),
	fg_color="#000000",
	corner_radius = 0
	)
    homepageFrame.place(x=0,y=0)

    currentFrame = homepageFrame # O frame a ser usado passa a ser o userFrame
    
    #Configure the grid to center the elements
    homepageFrame.grid_rowconfigure(0, weight=1)
    homepageFrame.grid_rowconfigure(1, weight=1)
    homepageFrame.grid_rowconfigure(2, weight=1)
    homepageFrame.grid_rowconfigure(3, weight=1)
    homepageFrame.grid_rowconfigure(4, weight=1)
    homepageFrame.grid_rowconfigure(5, weight=1)
    homepageFrame.grid_rowconfigure(6, weight=1)
    homepageFrame.grid_columnconfigure(0, weight=1)
    homepageFrame.grid_columnconfigure(1, weight=1)
    homepageFrame.grid_columnconfigure(2, weight=1)
    homepageFrame.grid_columnconfigure(3, weight=1)


    #Label para mostrar o texto "Admin Dashboard"
    trendingLabel = customtkinter.CTkLabel(homepageFrame, text="Admin Dashboard", font=("Roboto", 40))
    trendingLabel.grid(row=1, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")

    #Label para mostrar Music"
    labelMusics = customtkinter.CTkLabel(homepageFrame, text="Music", font=("Roboto", 25))
    labelMusics.grid(row=3, column=1, padx=20, pady=10, sticky="e")

    #Botão para gerir músicas
    manageMusicsbtn = customtkinter.CTkButton(homepageFrame, width=200, height=50, text="Manage Musics", command=lambda:manage_music_render(mainContentFrame,currentFrame))
    manageMusicsbtn.grid(row=3, column=2, padx=20, pady=10, sticky="w")

    #Label para mostrar Categorias
    labelManageCategories = customtkinter.CTkLabel(homepageFrame, text="Categories", font=("Roboto", 25))
    labelManageCategories.grid(row=4, column=1, padx=20, pady=10, sticky="e")
    
    #Botão para gerir Categorias
    manageCategoriesbtn = customtkinter.CTkButton(homepageFrame, width=200, height=50, text="Manage Categories", command=lambda:manage_categories_render(mainContentFrame,currentFrame))
    manageCategoriesbtn.grid(row=4, column=2, padx=20, pady=10, sticky="w")

    #Label para mostrar Podcasts"
    labelPodcasts = customtkinter.CTkLabel(homepageFrame, text="Podcasts", font=("Roboto", 25))
    labelPodcasts.grid(row=5, column=1, padx=20, pady=10, sticky="e")

    #Botão para gerir episódios
    manageEpisodesbtn = customtkinter.CTkButton(homepageFrame, width=200, height=50, text="Manage Podcasts", command=lambda:manage_podcast_render(mainContentFrame,currentFrame))
    manageEpisodesbtn.grid(row=5, column=2, padx=20, pady=10, sticky="w")

    #Label para mostrar Episódios
    labelManageEpisodes = customtkinter.CTkLabel(homepageFrame, text="Episodes", font=("Roboto", 25))
    labelManageEpisodes.grid(row=6, column=1, padx=20, pady=10, sticky="e")
    
    #Botão para gerir utilizadores
    manageEpisodesbtn = customtkinter.CTkButton(homepageFrame, width=200, height=50, text="Manage Episodes", command=lambda:manage_episodes_render(mainContentFrame, oldFrame))
    manageEpisodesbtn.grid(row=6, column=2, padx=20, pady=10, sticky="w")

    #Label para mostrar Users
    labelManageUsers = customtkinter.CTkLabel(homepageFrame, text="Users", font=("Roboto", 25))
    labelManageUsers.grid(row=7, column=1, padx=20, pady=10, sticky="e")
    
    #Botão para gerir utilizadores
    manageUsersbtn = customtkinter.CTkButton(homepageFrame, width=200, height=50, text="Manage Users", command=lambda:manage_users_render(mainContentFrame,currentFrame))
    manageUsersbtn.grid(row=7, column=2, padx=20, pady=10, sticky="w")

    #Label para mostrar Admins
    labelManageAdmins = customtkinter.CTkLabel(homepageFrame, text="Admins", font=("Roboto", 25))
    labelManageAdmins.grid(row=8, column=1, padx=20, pady=10, sticky="e")
    
    #Botão para gerir Admins
    manageAdminsbtn = customtkinter.CTkButton(homepageFrame, width=200, height=50, text="Manage Admins", command=lambda:manage_admins_render(mainContentFrame, oldFrame))
    manageAdminsbtn.grid(row=8, column=2, padx=20, pady=10, sticky="w")


def homepage_render(mainContentFrame, oldFrame):
    """Mostra a homepage"""

    global currentFrame # Variável global para frame a ser usado

    if oldFrame != None:
        oldFrame.destroy() # Apagar o estilo do frame anterior
    #Frame Home Page
    homepageFrame = customtkinter.CTkScrollableFrame(mainContentFrame,
	orientation="vertical",
	width=1238,
	height=appHeight-(90+131),
	fg_color="black",
	corner_radius = 0
	)
    homepageFrame.place(x=0,y=0)

    currentFrame = homepageFrame # O frame a ser usado passa a ser o userFrame
    
    #------------------------------------------------[Música em Alta]----------------------------------------------------------------------#

    # Frame menu trending Music
    trendingFrame = customtkinter.CTkFrame(homepageFrame, width=1300, height=300, fg_color="transparent", corner_radius=0)
    trendingFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Cria um scrollable frame dentro do frame principal
    trendingScrollFrame = customtkinter.CTkScrollableFrame(
        trendingFrame,
        orientation="horizontal",
        width=1200,
        height=250,
        fg_color="transparent"
    )
    trendingScrollFrame.place(x=0, y=20)
    
    trendingLabel = customtkinter.CTkLabel(trendingFrame,text="Trending Music",font=("Roboto", 25))
    trendingLabel.place(x=20,y=10)

    # Criar botões num ciclo for, na horizontal
    musicList = read_content("music")  # receber dados da lista (lista com sublistas)

    # Converter as visualizações para inteiro e ordenar manualmente
    for music in musicList:
        music[3] = int(music[3])  # Converter o campo de visualizações (índice 3) para inteiro

    # Ordenar a lista de músicas pelo número de visualizações em ordem decrescente
    for i in range(len(musicList)):
        for j in range(i + 1, len(musicList)):
            if musicList[i][3] < musicList[j][3]:  # Comparar pelo campo de visualizações
                musicList[i], musicList[j] = musicList[j], musicList[i]  # Trocar as posições

    # Limitar a exibição às 5 músicas com mais visualizações
    topTrendingMusic = musicList[:10]

    # Loop para criar os botões sem usar enumerate
    index = 0
    for music in topTrendingMusic:
        musicName = music[0]
        musicAuthor = music[1]
        musicCategory = music[2]
        musicViews = music[3]
        musicCover = coverArtPath + music[4]
        musicURL = music[5]

        coverArt = customtkinter.CTkImage(Image.open(musicCover), size=(150, 150))
        coverArt2 = customtkinter.CTkImage(Image.open(musicCover), size=(52, 52))

        button = customtkinter.CTkButton(
            trendingScrollFrame,
            width=150,
            height=150,
            text=f"{musicName}\n{musicAuthor}",
            image=coverArt,
            fg_color="transparent",
            compound="top",
            command=lambda idx=index, playlist=topTrendingMusic: play_music(idx, playlist) 
        )

        button.grid(row=0, column=index, padx=10, pady=40)
        index += 1  # Incrementar manualmente o índice

    #---------------------------------------------------------------------------------------------------------------------------------------#


    #------------------------------------------------[Podcast em Alta]----------------------------------------------------------------------#
    # Frame menu trending Podcasts
    trendingPodcastsFrame = customtkinter.CTkFrame(homepageFrame, width=1300, height=300, fg_color="transparent", corner_radius=0)
    trendingPodcastsFrame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

    # Cria um scrollable frame dentro do frame principal
    trendingPodcastsScrollFrame = customtkinter.CTkScrollableFrame(
        trendingPodcastsFrame,
        orientation="horizontal",
        width=1200,
        height=250,
        fg_color="transparent"
    )
    trendingPodcastsScrollFrame.place(x=0, y=20)
    
    trendingPodcastsLabel = customtkinter.CTkLabel(trendingPodcastsFrame,text="Trending Podcasts",font=("Roboto", 25))
    trendingPodcastsLabel.place(x=20,y=10)

    # Abrir lista de podcasts disponiveis
    podcastList = read_content("podcast") # receber dados da lista (lista com sublistas)

    # Converter as visualizações para inteiro e ordenar manualmente
    for podcast in podcastList:
        podcast[2] = int(podcast[2])  # Converter o campo de visualizações (índice 3) para inteiro

    # Ordenar a lista de músicas pelo número de visualizações em ordem decrescente
    for i in range(len(podcastList)):
        for j in range(i + 1, len(podcastList)):
            if podcastList[i][2] < podcastList[j][2]:  # Comparar pelo campo de visualizações
                podcastList[i], podcastList[j] = podcastList[j], podcastList[i]  # Trocar as posições

    # Limitar a exibição às 5 músicas com mais visualizações
    topTrendingpodcast = podcastList[:5]

    # Loop para criar os botões sem usar enumerate
    index = 0
    for podcast in topTrendingpodcast:
        podcastEpisode = podcast[0]
        podcastName = podcast[1]
        podcastViews = podcast[2]
        podcastCover = coverArtPath+get_cover_art(podcastName)
        podcastURL = podcast[3]

        if len(podcastEpisode) > 20:
            podcastEpisode = podcastEpisode[:17]+"..."
        
        if len(podcastName) > 20:
            podcastName = podcastName[:17]+"..."

        coverArt = customtkinter.CTkImage(Image.open(podcastCover), size=(150, 150))

        button = customtkinter.CTkButton(
            trendingPodcastsScrollFrame,
            width=150,
            height=150,
            text=f"{podcastEpisode}\n{podcastName}",
            image=coverArt,
            fg_color="transparent",
            compound="top",
            command=lambda url=podcastURL: play_podcast(url)
        )

        button.grid(row=0, column=index, padx=10, pady=40)
        index += 1  # Incrementar manualmente o índice

    # Frame menu Your Activity
    MusicYourActivityFrame = customtkinter.CTkFrame(homepageFrame, width=1300, height=300, fg_color="transparent", corner_radius=0)
    MusicYourActivityFrame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

    # Cria um scrollable frame dentro do frame principal
    MusicScrollFrame = customtkinter.CTkScrollableFrame(
        MusicYourActivityFrame,
        orientation="horizontal",
        width=1200,
        height=250,
        fg_color="transparent"
    )
    MusicScrollFrame.place(x=0, y=0)

    #Label para mostrar "Your Activity"
    MusicLabel = customtkinter.CTkLabel(MusicYourActivityFrame,text="Your Activity",font=("Roboto", 25))
    MusicLabel.place(x=10,y=0)

    activityPath = f"{usersPath}{usernameFinal}{pathFormat}music_activity.csv"

    recentMusic = get_recent_songs(activityPath)
    activityList = filter_music(musicList, recentMusic)

    index = 0
    for music in activityList:
        musicName = music[0]
        musicAuthor = music[1]
        musicCategory = music[2]
        musicViews = music[3]
        musicCover = coverArtPath + music[4]
        musicURL = music[5]

        coverArt = customtkinter.CTkImage(Image.open(musicCover), size=(150, 150))
        coverArt2 = customtkinter.CTkImage(Image.open(musicCover), size=(52, 52))

        button = customtkinter.CTkButton(
            MusicScrollFrame,
            width=150,
            height=150,
            text=f"{musicName}\n{musicAuthor}",
            image=coverArt,
            fg_color="transparent",
            compound="top",
            command=lambda idx=index, playlist=activityList: play_music(idx, playlist) 
        )

        button.grid(row=0, column=index, padx=10, pady=40)
        index += 1  # Incrementar manualmente o índice

    # Frame menu Discover
    MusicDiscoverFrame = customtkinter.CTkFrame(homepageFrame, width=1300, height=300, fg_color="transparent", corner_radius=0)
    MusicDiscoverFrame.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")

    # Cria um scrollable frame dentro do frame principal
    MusicScrollFrame = customtkinter.CTkScrollableFrame(
        MusicDiscoverFrame,
        orientation="horizontal",
        width=1200,
        height=250,
        fg_color="transparent"
    )
    MusicScrollFrame.place(x=0, y=0)

    #Label para mostrar "Your Activity"
    MusicLabel = customtkinter.CTkLabel(MusicDiscoverFrame,text="Discover",font=("Roboto", 25))
    MusicLabel.place(x=10,y=0)

    # Limitar a exibição a 8 músicas random
    randomMusic = random.sample(musicList, 4)

    index = 0
    for music in randomMusic:
        musicName = music[0]
        musicAuthor = music[1]
        musicCategory = music[2]
        musicViews = music[3]
        musicCover = coverArtPath + music[4]
        musicURL = music[5]

        coverArt = customtkinter.CTkImage(Image.open(musicCover), size=(150, 150))
        coverArt2 = customtkinter.CTkImage(Image.open(musicCover), size=(52, 52))

        button = customtkinter.CTkButton(
            MusicScrollFrame,
            width=150,
            height=150,
            text=f"{musicName}\n{musicAuthor}",
            image=coverArt,
            fg_color="transparent",
            compound="top",
            command=lambda idx=index, playlist=randomMusic: play_music(idx, playlist) 
        )

        button.grid(row=0, column=index, padx=10, pady=40)
        index += 1  # Incrementar manualmente o índice

    #---------------------------------------------------------------------------------------------------------------------------------------#

def musicpage_render(mainContentFrame, oldFrame):
    """Mostra a homepage"""

    global currentFrame,currentPlaylist # Variável global para frame a ser usado

    if oldFrame != None:
        oldFrame.destroy() # Apagar o estilo do frame anterior
    
    #Frame Music Page
    MusicpageFrame = customtkinter.CTkScrollableFrame(mainContentFrame,
	orientation="vertical",
	width=1238,
	height=appHeight-(90+131),
	fg_color="black",
	corner_radius = 0
	)
    MusicpageFrame.place(x=0,y=0)

    currentFrame = MusicpageFrame # O frame a ser usado passa a ser o userFrame

    # Frame menu Musicas
    MusicFrame = customtkinter.CTkFrame(MusicpageFrame, width=1300, height=300, fg_color="transparent", corner_radius=0)
    MusicFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Cria um scrollable frame dentro do frame principal
    MusicScrollFrame = customtkinter.CTkScrollableFrame(
        MusicFrame,
        orientation="horizontal",
        width=1200,
        height=250,
        fg_color="transparent"
    )
    MusicScrollFrame.place(x=0, y=0)

    MusicLabel = customtkinter.CTkLabel(MusicFrame,text="Music",font=("Roboto", 25))
    MusicLabel.place(x=20,y=10)

    # Criar botões num ciclo for, na horizontal
    musicList = read_content("music")  # receber dados da lista (lista com sublistas)

    index = 0
    for music in musicList:
        musicName = music[0]
        musicAuthor = music[1]
        musicCategory = music[2]
        musicViews = music[3]
        musicCover = coverArtPath + music[4]
        musicURL = music[5]

        coverArt = customtkinter.CTkImage(Image.open(musicCover), size=(150, 150))

        button = customtkinter.CTkButton(
            MusicScrollFrame,
            width=150,
            height=150,
            text=f"{musicName}\n{musicAuthor}",
            image=coverArt,
            fg_color="transparent",
            compound="top",
            command=lambda idx=index: play_music(idx,musicList)  # Passa o índice para a função
        )

        button.grid(row=0, column=index, padx=10, pady=40)
        index += 1

    # Frame menu Your Activity
    MusicYourActivityFrame = customtkinter.CTkFrame(MusicpageFrame, width=1300, height=300, fg_color="transparent", corner_radius=0)
    MusicYourActivityFrame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

    # Cria um scrollable frame dentro do frame principal
    MusicScrollFrame = customtkinter.CTkScrollableFrame(
        MusicYourActivityFrame,
        orientation="horizontal",
        width=1200,
        height=250,
        fg_color="transparent"
    )
    MusicScrollFrame.place(x=0, y=0)

    #Label para mostrar "Your Activity"
    MusicLabel = customtkinter.CTkLabel(MusicYourActivityFrame,text="Your Activity",font=("Roboto", 25))
    MusicLabel.place(x=10,y=0)

    activityPath = f"{usersPath}{usernameFinal}{pathFormat}music_activity.csv"

    recentMusic = get_recent_songs(activityPath)
    activityList = filter_music(musicList, recentMusic)

    index = 0
    for music in activityList:
        musicName = music[0]
        musicAuthor = music[1]
        musicCategory = music[2]
        musicViews = music[3]
        musicCover = coverArtPath + music[4]
        musicURL = music[5]

        coverArt = customtkinter.CTkImage(Image.open(musicCover), size=(150, 150))

        button = customtkinter.CTkButton(
            MusicScrollFrame,
            width=150,
            height=150,
            text=f"{musicName}\n{musicAuthor}",
            image=coverArt,
            fg_color="transparent",
            compound="top",
            command=lambda idx=index: play_music(idx,activityList)  # Passa o índice para a função
        )

        button.grid(row=0, column=index, padx=10, pady=40)
        index += 1

    # Frame menu Discover
    MusicDiscoverFrame = customtkinter.CTkFrame(MusicpageFrame, width=1300, height=300, fg_color="transparent", corner_radius=0)
    MusicDiscoverFrame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

    # Cria um scrollable frame dentro do frame principal
    MusicScrollFrame = customtkinter.CTkScrollableFrame(
        MusicDiscoverFrame,
        orientation="horizontal",
        width=1200,
        height=250,
        fg_color="transparent"
    )
    MusicScrollFrame.place(x=0, y=0)

    #Label para mostrar "Your Activity"
    MusicLabel = customtkinter.CTkLabel(MusicDiscoverFrame,text="Discover",font=("Roboto", 25))
    MusicLabel.place(x=10,y=0)

    # Limitar a exibição a 8 músicas random
    randomMusic = random.sample(musicList, 4)

    index = 0
    for music in randomMusic:
        musicName = music[0]
        musicAuthor = music[1]
        musicCategory = music[2]
        musicViews = music[3]
        musicCover = coverArtPath + music[4]
        musicURL = music[5]

        coverArt = customtkinter.CTkImage(Image.open(musicCover), size=(150, 150))

        button = customtkinter.CTkButton(
            MusicScrollFrame,
            width=150,
            height=150,
            text=f"{musicName}\n{musicAuthor}",
            image=coverArt,
            fg_color="transparent",
            compound="top",
            command=lambda idx=index: play_music(idx,randomMusic)  # Passa o índice para a função
        )

        button.grid(row=0, column=index, padx=10, pady=40)
        index += 1
    
    #--------------------------------------------------------------------------------------------------------------------------------------#

    # Main loop to display music by category
    categoryList = get_categories_music(musicList)  # Get all unique categories
    index = 2  # Start after Music, Your Activity, and Discover sections

    # Loop through each category
    for category in categoryList:
        # Print the category being processed for debugging
        print(f"Processing category: {category}")  # Debugging statement

        # Create frame for each category
        musicCategoryFrame = customtkinter.CTkFrame(MusicpageFrame, width=1300, height=300, fg_color="transparent", corner_radius=0)
        musicCategoryFrame.grid(row=index, column=0, padx=20, pady=20, sticky="nsew")

        # Create scrollable frame for the songs of the current category
        MusicCategoryScrollFrame = customtkinter.CTkScrollableFrame(
            musicCategoryFrame,
            orientation="horizontal",
            width=1200,
            height=250,
            fg_color="transparent"
        )
        MusicCategoryScrollFrame.place(x=0, y=0)

        # Label with the category name
        MusicLabel = customtkinter.CTkLabel(musicCategoryFrame, text=f"{category}", font=("Roboto", 25))
        MusicLabel.place(x=10, y=0)

        # Filter songs for the current category
        categoryMusicList = [music for music in musicList if music[2] == category]  # Filter songs based on category

        # Debugging: Check how many songs are being filtered for the category
        print(f"Songs in category '{category}': {len(categoryMusicList)}")  # Debugging statement

        if categoryMusicList:  # If there are songs for this category
            # Add songs to the scrollable frame
            col_index = 0
            for music in categoryMusicList:
                musicName = music[0]
                musicAuthor = music[1]
                musicCategory = music[2]
                musicViews = music[3]
                musicCover = coverArtPath + music[4]
                musicURL = music[5]

                coverArt = customtkinter.CTkImage(Image.open(musicCover), size=(150, 150))
                coverArt2 = customtkinter.CTkImage(Image.open(musicCover), size=(52, 52))

                # Create a button for each music, passing the category music list to play_music
                button = customtkinter.CTkButton(
                    MusicCategoryScrollFrame,
                    width=150,
                    height=150,
                    text=f"{musicName}\n{musicAuthor}",
                    image=coverArt,
                    fg_color="transparent",
                    compound="top",
                    command=lambda idx=col_index, playlist=categoryMusicList: play_music(idx, playlist)  # Passing the category music list
                )

                button.grid(row=0, column=col_index, padx=10, pady=40)
                col_index += 1  # Increment index for the next button
        else:
            # If no songs are available for the category, display a message
            MusicLabel = customtkinter.CTkLabel(musicCategoryFrame, text="No songs available for this category.", font=("Roboto", 20))
            MusicLabel.place(x=10, y=0)

        index += 1  # Increment index for the next category
        lastIndex=index
    
    # Obter lista de autores únicos
    authorList = get_authors(musicList)

    index = lastIndex+1  # Começar após as seções Music, Your Activity e Discover
    for author in authorList:
        # Criar frame para cada autor
        musicAuthorFrame = customtkinter.CTkFrame(MusicpageFrame, width=1300, height=300, fg_color="transparent", corner_radius=0)
        musicAuthorFrame.grid(row=index, column=0, padx=20, pady=20, sticky="nsew")

        # Criar scrollable frame para as músicas do autor
        MusicAuthorScrollFrame = customtkinter.CTkScrollableFrame(
            musicAuthorFrame,
            orientation="horizontal",
            width=1200,
            height=250,
            fg_color="transparent"
        )
        MusicAuthorScrollFrame.place(x=0, y=0)

        # Label com o nome do autor
        MusicLabel = customtkinter.CTkLabel(musicAuthorFrame, text=f"{author}", font=("Roboto", 25))
        MusicLabel.place(x=10, y=0)

        # Filtrar músicas do autor atual
        authorMusicList = [music for music in musicList if music[1] == author]

        # Adicionar músicas ao scrollable frame
        col_index = 0
        for music in authorMusicList:
            musicName = music[0]
            musicAuthor = music[1]
            musicCategory = music[2]
            musicViews = music[3]
            musicCover = coverArtPath + music[4]
            musicURL = music[5]

            coverArt = customtkinter.CTkImage(Image.open(musicCover), size=(150, 150))
            coverArt2 = customtkinter.CTkImage(Image.open(musicCover), size=(52, 52))

            # Criar botão para a música, passando a lista de músicas do autor para o play_music
            button = customtkinter.CTkButton(
                MusicAuthorScrollFrame,
                width=150,
                height=150,
                text=f"{musicName}\n{musicAuthor}",
                image=coverArt,
                fg_color="transparent",
                compound="top",
                command=lambda idx=col_index, playlist=authorMusicList: play_music(idx, playlist)  # Passando a música e a lista do autor
            )

            button.grid(row=0, column=col_index, padx=10, pady=40)
            col_index += 1  # Incrementar índice para o próximo botão

        index += 1  # Incrementar índice para o próximo autor
    
    #--------------------------------------------------------------------------------------------------------------------------------------#

def podcastpage_render(mainContentFrame, oldFrame):
    """Mostra a homepage"""

    global currentFrame # Variável global para frame a ser usado

    if oldFrame != None:
        oldFrame.destroy() # Apagar o estilo do frame anterior
    
    #Frame podcast Page
    podcastPageFrame = customtkinter.CTkScrollableFrame(mainContentFrame,
	orientation="vertical",
	width=1238,
	height=appHeight-(90+131),
	fg_color="black",
	corner_radius = 0
	)
    podcastPageFrame.place(x=0,y=0)

    currentFrame = podcastPageFrame # O frame a ser usado passa a ser o userFrame

    # Frame menu podcastas
    podcastFrame = customtkinter.CTkFrame(podcastPageFrame, width=1300, height=300, fg_color="transparent", corner_radius=0)
    podcastFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Cria um scrollable frame dentro do frame principal
    podcastScrollFrame = customtkinter.CTkScrollableFrame(
        podcastFrame,
        orientation="horizontal",
        width=1200,
        height=250,
        fg_color="transparent"
    )
    podcastScrollFrame.place(x=0, y=0)

    podcastLabel = customtkinter.CTkLabel(podcastFrame,text="Podcasts",font=("Roboto", 25))
    podcastLabel.place(x=20,y=10)

    # Criar botões num ciclo for, na horizontal
    podcastList = read_content("podcast")  # receber dados da lista (lista com sublistas)

    # Loop para criar os botões sem usar enumerate
    index = 0
    for podcast in podcastList:
        podcastEpisode = podcast[0]
        podcastName = podcast[1]
        podcastViews = podcast[2]
        podcastCover = coverArtPath+get_cover_art(podcastName)
        podcastURL = podcast[3]

        coverArt = customtkinter.CTkImage(Image.open(podcastCover), size=(150, 150))

        if len(podcastEpisode) > 20:
            podcastEpisode = podcastEpisode[:17]+"..."
        
        if len(podcastName) > 20:
            podcastName = podcastName[:17]+"..."

        button = customtkinter.CTkButton(
            podcastScrollFrame,
            width=150,
            height=150,
            text=f"{podcastEpisode}\n{podcastName}",
            image=coverArt,
            fg_color="transparent",
            compound="top",
            command=lambda url=podcastURL: play_podcast(url)
        )

        button.grid(row=0, column=index, padx=10, pady=40)
        index += 1  # Incrementar manualmente o índice


    # Obter lista de podcasts únicos
    podcastMainList = get_podcast(podcastList)

    index = 1  # Começar após as seções podcast
    for podcastTitle in podcastMainList:
        # Criar frame para cada autor
        podcastAuthorFrame = customtkinter.CTkFrame(podcastPageFrame, width=1300, height=300, fg_color="transparent", corner_radius=0)
        podcastAuthorFrame.grid(row=index, column=0, padx=20, pady=20, sticky="nsew")

        # Criar scrollable frame para as músicas do autor
        podcastAuthorScrollFrame = customtkinter.CTkScrollableFrame(
            podcastAuthorFrame,
            orientation="horizontal",
            width=1200,
            height=250,
            fg_color="transparent"
        )
        podcastAuthorScrollFrame.place(x=0, y=0)

        # Label com o nome do autor
        podcastLabel = customtkinter.CTkLabel(podcastAuthorFrame, text=f"{podcastTitle}", font=("Roboto", 25))
        podcastLabel.place(x=10, y=0)

        # Filtrar músicas do autor atual
        authorpodcastList = [podcast for podcast in podcastList if podcast[1] == podcastTitle]

        # Adicionar músicas ao scrollable frame
        col_index = 0
        for podcast in authorpodcastList:
            podcastEpisode = podcast[0]
            podcastName = podcast[1]
            podcastViews = podcast[2]
            podcastCover = coverArtPath+get_cover_art(podcastName)
            podcastURL = podcast[3]

            coverArt = customtkinter.CTkImage(Image.open(podcastCover), size=(150, 150))

            if len(podcastEpisode) > 20:
                podcastEpisode = podcastEpisode[:17]+"..."
        
            if len(podcastName) > 20:
                podcastName = podcastName[:17]+"..."
            
            button = customtkinter.CTkButton(
                podcastAuthorScrollFrame,
                width=150,
                height=150,
                text=f"{podcastEpisode}\n{podcastName}",
                image=coverArt,
                fg_color="transparent",
                compound="top",
                command=lambda url=podcastURL: play_podcast(url)
            )

            button.grid(row=0, column=col_index, padx=10, pady=40)
            col_index += 1  # Incrementar índice para o próximo botão

        index += 1  # Incrementar índice para o próximo autor

def delete_playlist(playListName, playlistPageFrame):
    """Deletes the playlist"""

    os.remove(f"{usersPath}{usernameFinal}{pathFormat}playlists{pathFormat}{playListName}.csv")
    print(f"Removed {usersPath}{usernameFinal}{pathFormat}playlists{pathFormat}{playListName}.csv.")

    homepage_render(mainContentFrame, currentFrame)
    refresh_playlists(playlistScrollFrame)

def playlist_page_render(mainContentFrame, oldFrame, playListName):
    """Mostra a homepage"""

    global currentFrame # Variável global para frame a ser usado

    if oldFrame != None:
        oldFrame.destroy() # Apagar o estilo do frame anterior
    
    
    #Frame Music Page
    playlistPageFrame = customtkinter.CTkFrame(mainContentFrame,
	width=1238,
	height=appHeight-(90+131),
	fg_color="black",
	corner_radius = 0
	)
    playlistPageFrame.place(x=0,y=0)

    currentFrame = playlistPageFrame # O frame a ser usado passa a ser o userFrame

    # Frame menu Musicas
    MusicFrame = customtkinter.CTkFrame(playlistPageFrame, width=1300, height=800, fg_color="transparent", corner_radius=0)
    MusicFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Cria um scrollable frame dentro do frame principal
    MusicScrollFrame = customtkinter.CTkScrollableFrame(
        MusicFrame,
        orientation="vertical",
        width=1200,
        height=500,
        fg_color="transparent"
    )
    MusicScrollFrame.place(x=0, y=50)

    MusicLabel = customtkinter.CTkLabel(MusicFrame,text=f"{playListName}",font=("Roboto", 25))
    MusicLabel.place(x=20,y=10)

    playlistDeleteBtn = customtkinter.CTkButton(MusicFrame,text="Delete Playlist",font=("Roboto", 25),command=lambda:delete_playlist(playListName, playlistPageFrame))
    playlistDeleteBtn.place(x=200,y=10)

    # Criar botões num ciclo for, na horizontal
    musicList = read_content("music")  # receber dados da lista (lista com sublistas)

    playlistList=get_playlist_list(musicList, usernameFinal, playListName)

    # Loop para criar os botões sem usar enumerate
    index = 0
    for music in playlistList:
        musicName = music[0]
        musicAuthor = music[1]
        musicCategory = music[2]
        musicViews = music[3]
        musicCover = coverArtPath + music[4]
        musicURL = music[5]

        coverArt = customtkinter.CTkImage(Image.open(musicCover), size=(150, 150))
        coverArt2 = customtkinter.CTkImage(Image.open(musicCover), size=(52, 52))

        button = customtkinter.CTkButton(
            MusicScrollFrame,
            width=150,
            height=150,
            text="",
            image=coverArt,
            fg_color="transparent",
            compound="top",
            command=lambda idx=index, playlist=playlistList: play_music(idx, playlist) 
        )

        button.grid(row=index, column=0, padx=40, pady=20)

        nameLabel = customtkinter.CTkLabel(
            MusicScrollFrame,
            text=f"{musicName}"
        )
        nameLabel.grid(row=index, column=1,padx=40, pady=20)

        authorLabel = customtkinter.CTkLabel(
            MusicScrollFrame,
            text=f"{musicAuthor}"
        )
        authorLabel.grid(row=index, column=2,padx=40, pady=20)

        viewsLabel = customtkinter.CTkLabel(
            MusicScrollFrame,
            text=f"{musicViews} Views"
        )
        viewsLabel.grid(row=index, column=3,padx=40, pady=20)

        button2 = customtkinter.CTkButton(
            MusicScrollFrame,
            width=150,
            height=50,
            text="Remove from Playlist",
            command=lambda name=musicName, author=musicAuthor: refresh_playlist(name, author,mainContentFrame,currentFrame, playListName)
        )

        button2.grid(row=index, column=4, padx=40, pady=20)

        index += 1  # Incrementar manualmente o índice

def favoritepage_render(mainContentFrame, oldFrame):
    """Mostra a homepage"""

    global currentFrame # Variável global para frame a ser usado

    if oldFrame != None:
        oldFrame.destroy() # Apagar o estilo do frame anterior
    
    
    #Frame Music Page
    favoritePageFrame = customtkinter.CTkFrame(mainContentFrame,
	width=1238,
	height=appHeight-(90+131),
	fg_color="black",
	corner_radius = 0
	)
    favoritePageFrame.place(x=0,y=0)

    currentFrame = favoritePageFrame # O frame a ser usado passa a ser o userFrame

    # Frame menu Musicas
    MusicFrame = customtkinter.CTkFrame(favoritePageFrame, width=1300, height=800, fg_color="transparent", corner_radius=0)
    MusicFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    # Cria um scrollable frame dentro do frame principal
    MusicScrollFrame = customtkinter.CTkScrollableFrame(
        MusicFrame,
        orientation="vertical",
        width=1200,
        height=500,
        fg_color="transparent"
    )
    MusicScrollFrame.place(x=0, y=50)

    MusicLabel = customtkinter.CTkLabel(MusicFrame,text=f"{nameFull} Favorite List",font=("Roboto", 25))
    MusicLabel.place(x=20,y=10)

    # Criar botões num ciclo for, na horizontal
    musicList = read_content("music")  # receber dados da lista (lista com sublistas)

    favoritesList=get_favorites(musicList,usernameFinal)

    # Loop para criar os botões sem usar enumerate
    index = 0
    for music in favoritesList:
        musicName = music[0]
        musicAuthor = music[1]
        musicCategory = music[2]
        musicViews = music[3]
        musicCover = coverArtPath + music[4]
        musicURL = music[5]

        coverArt = customtkinter.CTkImage(Image.open(musicCover), size=(150, 150))

        button = customtkinter.CTkButton(
            MusicScrollFrame,
            width=150,
            height=150,
            text="",
            image=coverArt,
            fg_color="transparent",
            compound="top",
            command=lambda idx=index, playlist=favoritesList: play_music(idx, playlist) 
        )

        button.grid(row=index, column=0, padx=10, pady=40)

        nameLabel = customtkinter.CTkLabel(
            MusicScrollFrame,
            text=f"{musicName}"
        )
        nameLabel.grid(row=index, column=1,padx=40, pady=20)

        authorLabel = customtkinter.CTkLabel(
            MusicScrollFrame,
            text=f"{musicAuthor}"
        )
        authorLabel.grid(row=index, column=2,padx=40, pady=20)

        viewsLabel = customtkinter.CTkLabel(
            MusicScrollFrame,
            text=f"{musicViews} Views"
        )
        viewsLabel.grid(row=index, column=3,padx=40, pady=20)

        button2 = customtkinter.CTkButton(
            MusicScrollFrame,
            width=150,
            height=50,
            text="Remove from Favorites",
            command=lambda name=musicName, author=musicAuthor: refresh_favorite(name, author,mainContentFrame,oldFrame)
        )

        button2.grid(row=index, column=4, padx=40, pady=20)

        index += 1  # Incrementar manualmente o índice
    
def refresh_favorite(name, author,mainContentFrame,oldFrame):
    remove_favorite(name, author, usernameFinal)
    favoritepage_render(mainContentFrame,oldFrame)

def refresh_playlist(name, author,mainContentFrame,oldFrame,playListName):
    remove_music_playlist(name, author,usernameFinal, playListName)
    playlist_page_render(mainContentFrame,oldFrame,playListName)

def read_content(contentType):
    if contentType == "podcast":
        with open(podcastEpisodesPath, "r", encoding="utf-8") as file:
            lines = file.readlines()

    elif contentType == "music":
        with open(musicPath, "r", encoding="utf-8") as file:
            lines = file.readlines()

    returnList = []
    for line in lines:
        fields = line.strip().split(";")
        returnList.append(fields)  # Each entry is a list: [name, author, cover, link]

    return returnList

def toggle_play():
    global isPaused

    if isPaused:
        mixer.music.unpause()
        btnPlay.configure(image=pauseIcon)
        isPaused = False
    else:
        mixer.music.pause()
        btnPlay.configure(image=playIcon)
        isPaused = True

def toggle_mute():
    global currentLevel
    
    if volumeSlider.get() == 0:
        volumeSlider.set(currentLevel)
    else:
        currentLevel = volumeSlider.get()
        volumeSlider.set(0)

    adjust_volume()
    
##########################################################

login_render("")

# Loop de event listening
app.mainloop()