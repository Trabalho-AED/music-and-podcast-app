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
import webbrowser                        # https://docs.python.org/3/library/webbrowser.html 
import time #Sleep
from file_management import *
from users import *
from music_management import *

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
###########################################################

# Inicializar app
app = customtkinter.CTk(fg_color= "#000000")

# Titulo da app
app.title("Music App")

# Define a dimensão da app
appWidth = 1500
appHeight = 800

# App não resizable em x
#app.resizable(width=False, height=False)

# Obtém a dimensão do ecrã
screenWidth = app.winfo_screenwidth()
screenHeight = app.winfo_screenheight()

# Calcula a posição para centralizar a janela
x = (screenWidth / 2) - (appWidth / 2)
y = (screenHeight / 2) - (appHeight / 2)

# Define o tamanho da app e começa no centro da tela
app.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")

##################[ALGORITMOS DA APP]################################

def user_check(username):
    """Verifica se o username já existe.
    Retorna um booleano"""

    lines = read_file(accountsPath) # Abrir os dados do ficheiro utilizador

    #Para cada linha de dados
    for line in lines:
        fields = line.strip().split(";")
        if fields[0] == username:
            return True # Se o nome de utilizador(fields na posição 0) for igual ao username
    
    return False # Se não for encontrado nenhum username igual

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

    global nameFull, usernameFinal

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

def confirm_music(musicNameEntry, musicAuthorEntry,musicCoverImg,musicAudioPathLabel, erroradd_musicLabel):
    """Guarda os dados da música a adicionar"""
    
    global tempCoverName, tempAudioName  # Indicar as variáveis globais

    if musicNameEntry.get() and musicAuthorEntry.get() and tempAudioName and tempCoverName:
        #Variável com a estrutura de dados
        musicData = f"{musicNameEntry.get()};{musicAuthorEntry.get()};{tempCoverName};{tempAudioName}\n"

        #Abre o caminho da música no formato "append" para adicionar a linha sem apagar o conteúdo existente
        with open(musicPath, "a", encoding="utf-8") as file:
            file.writelines(musicData) # escreve os dados com a estrutura anteriormente definida
            file.close
        
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

        musicAudioPathLabel.configure(text=f"{musicAudioPath+tempAudioName}") # Muda o texto da label para apresentar o aúdio

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
        btnPlaylist1 = customtkinter.CTkButton(playlistScrollFrame, image=playlistIcon, width=31, height=31, fg_color="transparent", text=f"{playLists[i]}")
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
    app.after(200, update_slider)  # Atualiza a cada 200ms

def adjust_volume(event=None):
    """Ajusta o volume da música baseado no slider."""
    volume = volumeSlider.get() / 100  # Converte para intervalo de 0 a 1
    mixer.music.set_volume(volume)

def play_music(music,musicName,musicAuthor,coverArt):
    """Toca a música e atualiza a interface."""

    global isPaused

    mixer.init()
    mixer.music.load(musicAudioPath + music)
    mixer.music.play(loops=0)  # Toca apenas uma vez
    btnPlay.configure(image=pauseIcon)
    isPaused = False

    # Atualiza informações na interface
    update_music_info(musicName, musicAuthor, coverArt)

    # Configura o slider de progresso
    musicLenSlider.configure(to=get_music_length(music))
    update_slider()

def new_playlist():
    """Abre um frame para adicionar playlists"""

    # Frame para adicionar playlist
    playlistCreateFrame = customtkinter.CTkFrame(app, width=appWidth-246, height=916)
    playlistCreateFrame.place(x=215, y=425)  # Abre o frame no canto superior direito

    # ----------------------------[Nome da Playlist]--------------------------------#

    # Label para mostrar o texto "Nome da Playlist:"
    playListNameLabel = customtkinter.CTkLabel(playlistCreateFrame, text="Nome da Playlist:")
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
        text="Criar",
        command=lambda: create_playlist(playListNameEntry.get(), playlistCreateFrame, errorLabel)  # Retrieve value when clicked
    )
    confirmBtn.pack(expand=True, pady=20)

    # Botão para cancelar
    cancBtn = customtkinter.CTkButton(
        playlistCreateFrame,
        width=100,
        height=50,
        text="Cancelar",
        command=lambda: playlistCreateFrame.destroy()  # Retrieve value when clicked
    )
    cancBtn.pack(expand=True, pady=5)

    errorLabel = customtkinter.CTkLabel(playlistCreateFrame, text="")
    errorLabel.pack(expand=True, pady=5)

def add_music():
    """Abre um frame para adicionar músicas"""

    #Frame para adicionar música
    musicFrame = customtkinter.CTkFrame(app, width=appWidth-246, height=916)
    musicFrame.place(relx=1,rely=0, anchor="ne") #Abre o frame no canto superior direito
    
    #----------------------------[Nome da Música]--------------------------------#

    #Label para mostar o texto "Music Name:"
    musicNameLabel = customtkinter.CTkLabel(musicFrame, text="Music Name:")
    musicNameLabel.pack(expand=True)

    #Entry para o nome da música
    musicNameEntry = customtkinter.CTkEntry(musicFrame)
    musicNameEntry.pack(expand=True)

    #----------------------------------------------------------------------------#


    #----------------------------[Autor da Música]-------------------------------#
    
    #Label para mostrar o texto "Author:"
    musicAuthorLabel = customtkinter.CTkLabel(musicFrame, text="Author:")
    musicAuthorLabel.pack(expand=True)

    #Entry para o nome do autor
    musicAuthorEntry = customtkinter.CTkEntry(musicFrame)
    musicAuthorEntry.pack(expand=True)

    #----------------------------------------------------------------------------#


    #----------------------------[Imagem da Música]------------------------------#
    
    #Label para mostrar o texto "Cover Art:"
    musicCoverLabel = customtkinter.CTkLabel(musicFrame, text="Cover Art:")
    musicCoverLabel.pack(expand=True)

    #Label para mostrar a imagem escolhida
    musicCoverImg = customtkinter.CTkLabel(musicFrame, text="")
    musicCoverImg.pack(expand=True)

    #Botão para escolher a imagem da música
    musicCoverBtn = customtkinter.CTkButton(musicFrame, width=300, height=100, text="Add cover art", command=lambda:select_file(musicCoverImg, ""))
    musicCoverBtn.pack(expand=True)

    #--------------------------------------------------------------------------#


    #----------------------------[Aúdio da Música]-----------------------------#
    
    #Label para mostrar a o texto "Audio:"
    musicAudioLabel = customtkinter.CTkLabel(musicFrame, text="Audio:")
    musicAudioLabel.pack(expand=True)

    #Label para mostrar o aúdio a ser adicionado
    musicAudioPathLabel = customtkinter.CTkLabel(musicFrame, text="")
    musicAudioPathLabel.pack(expand=True)

    #Botão para escolher o aúdio
    musicAudioBtn = customtkinter.CTkButton(musicFrame, width=300, height=100, text="Add audio", command=lambda:select_file("", musicAudioPathLabel))
    musicAudioBtn.pack(expand=True)

    #--------------------------------------------------------------------------#


    #Botão para salvar a os dados
    confirmBtn = customtkinter.CTkButton(musicFrame, width=300, height=100, text="Confirm", command=lambda:confirm_music(musicNameEntry, musicAuthorEntry,musicCoverImg,musicAudioPathLabel, erroradd_musicLabel))
    confirmBtn.pack(expand=True)

    #Label para mostrar erros
    erroradd_musicLabel = customtkinter.CTkLabel(musicFrame, text="")
    erroradd_musicLabel.pack(expand=True)


def mainwindow_render(oldFrame):
    """Rendriza a frame da janela principal"""

    global currentFrame,nameFull,addIcon,playlistMenuFrame, musicName, artistName, musicLenSlider, volumeSlider, musicCover, playIcon, pauseIcon, btnPlay, playlistScrollFrame,playlistIcon # Variável global do frame em uso

    oldFrame.destroy() # Apagar o estilo do frame anterior

    #Frame menu lateral
    menuFrame = customtkinter.CTkFrame(app, width=246, height=916, fg_color="#0E0D11",corner_radius=0)  
    menuFrame.place(relx=0, rely=0,anchor="nw")
    
    #Frame de cima com a função de procurar e, para admin, entrar no dashboard
    upperSearchFrame = customtkinter.CTkFrame(app, width=appWidth, height=90, fg_color="#020202",corner_radius=0)  
    upperSearchFrame.place(x=246,y=0)

    #Frame para o conteúdo principal
    mainContentFrame = customtkinter.CTkFrame(app, width=appWidth-246, height=appHeight-221, fg_color="red",corner_radius=0)  
    mainContentFrame.place(x=246,y=90)

    #Search Bar na Upper Search Frame
    search_entry = customtkinter.CTkEntry(
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
    search_entry.place(x=531, y=39, anchor="center")

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

    # Icon favoritos
    favoriteIcon = customtkinter.CTkImage(Image.open(f"{imagePath}favorite_icon.png"), size=(31, 31))

    # Icon playlist
    playlistIcon = customtkinter.CTkImage(Image.open(f"{imagePath}playlist_icon.png"), size=(31, 31))

    # Icon add 
    addIcon = customtkinter.CTkImage(Image.open(f"{imagePath}add_icon.png"), size=(31, 31))


    ############################## APLICAÇAO DAS IMAGENS NOS BUTTONS E LAYERS PARA CADA BUTTON######################
    ############################################### UpperMenuFrame ###############################################

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
    btnPodcast = customtkinter.CTkButton(collectionMenuFrame, image=artistIcon, width=31, height=31, fg_color="transparent", text="Podcast")
    btnPodcast.place(x=0, y=76)

    #Botão com Icon e texto de Favoritos
    btnFavorites = customtkinter.CTkButton(collectionMenuFrame, image=favoriteIcon, width=31, height=31, fg_color="transparent", text="Favorites")
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

    ############################## APLICAÇAO DAS IMAGENS NOS BUTTONS E LAYERS PARA CADA BUTTON######################
    ############################################### FRAMES BARRA MUSICA ###############################################
    #Frame com conteúdo
    # Frame com conteúdo
    musicContentFrame = customtkinter.CTkFrame(playFrame, width=2000, height=70, fg_color="#0A090C")
    musicContentFrame.place(x=107, y=43)

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
    audioSliderFrame.grid(row=0, column=2, sticky="nsew", padx=50, pady=5)  # Alinhado e espaçado


    #-------------------------------------------------------------------------------------------------------

    #-------------------------------------[FRAME INFO]-------------------------------------------------------------

    #Frame para mostrar info: Nome da música e artista
    musicInfoFrame = customtkinter.CTkFrame(showMusicFrame, width=300, height=50, fg_color="#0A090C")
    musicInfoFrame.place(x=72, y=7)

    #Capa da Música (substituir por imagem)
    musicCover = customtkinter.CTkButton(showMusicFrame, width=53, height=53, text="",image="", fg_color="Red")
    musicCover.place(x=0,y=0)

    #Nome da música
    musicName = customtkinter.CTkLabel(musicInfoFrame, text="Music Name", font=("Arial", 17))
    musicName.place(x=0, y=0)

    #Nome do artista
    artistName = customtkinter.CTkLabel(musicInfoFrame, text="Artist Name", font=("Arial", 12) )
    artistName.place(x=0, y=24)

    #------------------------------------[FRAME CONTROLOS MÚSICA]---------------------------------------------------------------------------

    #Frame botões de controlo
    controlBtnFrame = customtkinter.CTkFrame(musicActionFrame, width=130, height=44, fg_color="#0A090C")
    controlBtnFrame.place(x=256, y=1)

    #Botão com Icone de recuar
    btnBack = customtkinter.CTkButton(controlBtnFrame, image=backIcon, width=20, height=20, fg_color="transparent", text="")
    btnBack.place(x=0, y=7)

    #Botão com Icone de play
    btnPlay = customtkinter.CTkButton(controlBtnFrame, image=playIcon, width=34, height=34, fg_color="transparent", text="", command=toggle_play)
    btnPlay.place(x=40, y=0)

    #Botão com Icone de avançar
    btnForward = customtkinter.CTkButton(controlBtnFrame, image=forwardIcon, width=20, height=20, fg_color="transparent", text="")
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

def userpage_render(mainContentFrame, oldFrame):
    """Mostra o frame da página de utilizador"""

    global currentFrame # Variável global para frame a ser usado

    oldFrame.destroy() # Apagar o estilo do frame anterior

    #Frame User Menu
    userFrame = customtkinter.CTkFrame(mainContentFrame, width=1674, height=890, fg_color="#242424",corner_radius=0)  
    userFrame.place(x=0,y=0)

    currentFrame = userFrame # O frame a ser usado passa a ser o userFrame

    #Frame options Menu
    optionsFrame = customtkinter.CTkFrame(userFrame, width=542, height=430, corner_radius=50,fg_color="#242424")
    optionsFrame.place(x=362,y=140)

    #Frame Change Image
    changeImageFrame = customtkinter.CTkFrame(optionsFrame, width=542, height=158, corner_radius=10,fg_color="#242424")
    changeImageFrame.place(x=0,y=0)

    #Frame Change Name
    changeNameFrame = customtkinter.CTkFrame(optionsFrame, width=542, height=158, corner_radius=10,fg_color="#242424")
    changeNameFrame.place(x=0,y=158)

    #Frame Change Username
    changeUserNameFrame = customtkinter.CTkFrame(optionsFrame, width=542, height=158, corner_radius=10,fg_color="#242424")
    changeUserNameFrame.place(x=0,y=224)

    #Frame Change Password
    changePassFrame = customtkinter.CTkFrame(optionsFrame, width=542, height=158, corner_radius=10,fg_color="#242424")
    changePassFrame.place(x=0,y=290)

    #Titulo
    title = customtkinter.CTkLabel(userFrame, text="User Page", font=("Arial", 30),text_color="white")
    title.place(x=553,y=70)

    # Butao mudar imagem
    btnChgImage = customtkinter.CTkButton(changeImageFrame, width=150, height=30,text="Change Image")
    btnChgImage.place(x=300, y=30)

    # Butao mudar nome
    btnChgName = customtkinter.CTkButton(changeNameFrame, width=150, height=30,text="Change Name")
    btnChgName.place(x=300, y=30)

    # Butao mudar Username
    btnChgUsername = customtkinter.CTkButton(changeUserNameFrame, width=150, height=30,text="Change Username")
    btnChgUsername.place(x=300, y=30)

    # Butao mudar Password
    btnChgPass = customtkinter.CTkButton(changePassFrame, width=150, height=30,text="Change Password")
    btnChgPass.place(x=300, y=30)

    # Label Imagem do User
    userImg = customtkinter.CTkLabel(changeImageFrame, text="")
    userImg.place(x=105,y=35)

    # Label Nome
    labelName = customtkinter.CTkLabel(changeNameFrame, text="User Name", font=("Arial", 20),text_color="white")
    labelName.place(x=105,y=35)
    
    # Label Username
    labelUsername = customtkinter.CTkLabel(changeUserNameFrame, text="username", font=("Arial", 20),text_color="white")
    labelUsername.place(x=105,y=35)

    # Label Password
    labelPass = customtkinter.CTkLabel(changePassFrame, text="Password", font=("Arial", 20),text_color="white")
    labelPass.place(x=105,y=35)

    btnLogout = customtkinter.CTkButton(changePassFrame, width=100, height=30,text="Logout",command=lambda:login_render(userFrame),fg_color="Red")
    btnLogout.place(x=200, y=85)

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
        errorLabel.configure(text="O nome da playlist não pode estar vazio")
        return
    
    elif playListName+".csv" in os.listdir(f"{usersPath}{usernameFinal}{pathFormat}playlists"):
        errorLabel.configure(text="Playlist já existe!")
        return

    else:
        with open(playlistPath, "w", encoding="utf-8") as file:
            pass

        refresh_playlists(playlistScrollFrame)

        playlistCreateFrame.destroy()

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
	fg_color="black",
	corner_radius = 0
	)
    homepageFrame.place(x=0,y=0)

    currentFrame = homepageFrame # O frame a ser usado passa a ser o userFrame
    
   # Configure the grid to center the elements
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

    # Botão para adicionar música
    addBtn = customtkinter.CTkButton(homepageFrame, width=200, height=50, text="Add Music")
    addBtn.grid(row=2, column=1, padx=20, pady=10, sticky="e")

    # Botão para adicionar podcast
    addPodcastBtn = customtkinter.CTkButton(homepageFrame, width=200, height=50, text="Add Podcast")
    addPodcastBtn.grid(row=2, column=2, padx=20, pady=10, sticky="w")

    #Label para mostrar Music"
    labelMusics = customtkinter.CTkLabel(homepageFrame, text="Music", font=("Roboto", 25))
    labelMusics.grid(row=3, column=1, padx=20, pady=10, sticky="e")

    #Label para mostrar Podcasts"
    labelPodcasts = customtkinter.CTkLabel(homepageFrame, text="Podcasts", font=("Roboto", 25))
    labelPodcasts.grid(row=4, column=1, padx=20, pady=10, sticky="e")

    #Botão para gerir músicas
    ManageMusicsbtn = customtkinter.CTkButton(homepageFrame, width=200, height=50, text="Manage Musics")
    ManageMusicsbtn.grid(row=3, column=2, padx=20, pady=10, sticky="w")

    #Botão para gerir podcasts
    ManagePodcastsbtn = customtkinter.CTkButton(homepageFrame, width=200, height=50, text="Manage Podcasts")
    ManagePodcastsbtn.grid(row=4, column=2, padx=20, pady=10, sticky="w")

    #Label para mostrar Users
    labelManageUsers = customtkinter.CTkLabel(homepageFrame, text="Users", font=("Roboto", 25))
    labelManageUsers.grid(row=5, column=1, padx=20, pady=10, sticky="e")

    #Botão para gerir utilizadores
    ManageUsersbtn = customtkinter.CTkButton(homepageFrame, width=200, height=50, text="Manage Users")
    ManageUsersbtn.grid(row=5, column=2, padx=20, pady=10, sticky="w")


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

    # Criar botões num ciclo for, na horizontal
    musicList = read_content("music")  # receber dados da lista (lista com sublistas)

    for i in range(len(musicList)):
        musicName = musicList[i][0]
        musicAuthor = musicList[i][1]
        musicCover = coverArtPath + musicList[i][2]
        musicURL = musicList[i][3]

        coverArt = customtkinter.CTkImage(Image.open(musicCover), size=(150, 150))
        coverArt2 = customtkinter.CTkImage(Image.open(musicCover), size=(52, 52))

        button = customtkinter.CTkButton(
            trendingScrollFrame,
            width=150,
            height=150,
            text=f"{musicName}\n{musicAuthor}",
            image=coverArt,
            fg_color="red",
            compound="top",
            command=lambda url=musicURL, name=musicName, author=musicAuthor, art=coverArt2: play_music(url, name, author, art)
        )

        button.grid(row=0, column=i, padx=10, pady=40)

    

    # Abrir lista de podcasts disponiveis
    podcastList = read_content("podcast")

def musicpage_render(mainContentFrame, oldFrame):
    """Mostra a homepage"""

    global currentFrame # Variável global para frame a ser usado

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
    MusicScrollFrame.place(x=0, y=20)

    MusicLabel = customtkinter.CTkLabel(MusicFrame,text="Music",font=("Roboto", 25))
    MusicLabel.place(x=20,y=10)

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
    MusicScrollFrame.place(x=0, y=20)

    #Label para mostrar "Your Activity"
    MusicLabel = customtkinter.CTkLabel(MusicYourActivityFrame,text="Your Activity",font=("Roboto", 25))
    MusicLabel.place(x=20,y=10)

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
    MusicScrollFrame.place(x=0, y=20)

    #Label para mostrar "Your Activity"
    MusicLabel = customtkinter.CTkLabel(MusicDiscoverFrame,text="Discover",font=("Roboto", 25))
    MusicLabel.place(x=20,y=10)

    

def read_content(contentType):
    if contentType == "podcast":
        with open(podcastPath, "r", encoding="utf-8") as file:
            podcastList = file.readlines()
        return podcastList
    elif contentType == "music":
        with open(musicPath, "r", encoding="utf-8") as file:
            lines = file.readlines()

        musicList = []
        for line in lines:
            fields = line.strip().split(";")
            musicList.append(fields)  # Each entry is a list: [name, author, cover, link]

        return musicList

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

def podcast_video_render(videoURL):
    """
    Abre o browser definido por defeito com um url
    """
    webbrowser.open(videoURL, new = 0, autoraise=True)
    
##########################################################

login_render("")

# Loop de event listening
app.mainloop()