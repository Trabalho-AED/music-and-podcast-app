import customtkinter
from PIL import Image
import os
#from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#from comtypes import CLSCTX_ALL
import tkinter as tk
from tkinter import ttk

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light" Alterar entre tema escuro e claro
#customtkinter.set_default_color_theme(".\\theme\\rime.json") # Tema de cores

###############[VERIFICAR SISTEMA OPERATIVO]##################
def path_format():
    """Retorna o formato de declarar caminhos, dependendo do Sistema Operativo"""

    #Se os SO for windows
    if os.name=="nt":
        pathFormat = "\\"
    #Se for outro SO
    else:
        pathFormat = "/"

    return pathFormat # Retorna o formato

pathFormat = path_format()
##################################################################


imagePath = f".{pathFormat}images{pathFormat}icons{pathFormat}" # Caminho para o diretório onde são armazenadas as imagens
accountsPath = f".{pathFormat}db{pathFormat}user_accounts.csv" # Caminho para o ficheiro onde são armazenadas as contas
adminListfile = f".{pathFormat}db{pathFormat}admin_list.csv" # Caminho para o ficheiro onde são armazenadas as contas que são admin

# Inicializar app
app = customtkinter.CTk()

# Titulo da app
app.title("Music App")

# Define a dimensão da app
appWidth = 1400
appHeight = 800

# Obtém a dimensão do ecrã
screenWidth = app.winfo_screenwidth()
screenHeight = app.winfo_screenheight()

# Calcula a posição para centralizar a janela
x = (screenWidth / 2) - (appWidth / 2)
y = (screenHeight / 2) - (appHeight / 2)

# Define o tamanho da app e começa no centro da tela
app.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")



##################[ALGORITMOS DA APP]################################
def read_file(path):
    """Lê um ficheiro com qualquer opção.
    Retorna o conteúdo do ficheiro"""

    #Abre o ficheiro
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines() # Lê o ficheiro
    
    return lines # Retorna o conteúdo

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

def check_admin(username):
    """Verifica se o utilizador é admin.
    Retorna um booleano"""

    lines = read_file(adminListfile) # Abrir os dados do ficheiro admin

    #Para cada linha de dados
    for line in lines:
        if line.strip() == username:
            return True # Se o utilizador na linha for igual ao username
        
    return False # Se o utilizador não estiver na lista de admin

def create_account(username, password, name):
    """Cria uma conta"""

    accountAdd = username+";"+password+";"+name+"\n" # String com o Formato dos dados
    with open(accountsPath, "a", encoding="utf-8") as file:
        file.write(accountAdd) # Escreve os dados no ficheiro

def login_action(usernameEntry, passwordEntry, resultLabel,loginFrame):
    """Gere o algoritmo de login"""
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
        mainwindow_render(loginFrame) # Passa para a janela principal

def register_action(usernameEntry, passwordEntry,nameEntry, resultLabel):
    """Gere o algoritmo de registo"""

    name = nameEntry.get() # Recebe o valor que está na entry do nome
    username = usernameEntry.get() # Recebe o valor que está na entry do username
    password = passwordEntry.get() # Recebe o valor que está na entry da password

    # Se algum campo estiver vazio
    if username == "" or password == "":
        resultLabel.configure(text="Preencha todos os campos.") # Texto a apresentar
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

##########################################################




#############################[RENDER SCREENS]##########################################
def register_render(oldFrame):
    """Renderiza a frame do formulário de registo"""

    print("Register") # Mensagem de confirmação na consola

    oldFrame.pack_forget() # Apagar o estilo do frame anterior

    #Frame
    frameRegister = customtkinter.CTkFrame(app, width=600, height=500)
    frameRegister.pack(expand=True)

    # Labels e campos de entrada
    nameLabel = customtkinter.CTkLabel(frameRegister, text="Nome:")
    nameLabel.pack(padx=20, pady=5)

    nameEntry = customtkinter.CTkEntry(frameRegister, placeholder_text="Nome...")
    nameEntry.pack(padx=20, pady=10)

    usernameLabel = customtkinter.CTkLabel(frameRegister, text="Username:")
    usernameLabel.pack(padx=20, pady=5)

    usernameEntry = customtkinter.CTkEntry(frameRegister, placeholder_text="Username...")
    usernameEntry.pack(padx=20, pady=10)

    passwordLabel = customtkinter.CTkLabel(frameRegister, text="Password:")
    passwordLabel.pack(padx=20, pady=5)

    passwordEntry = customtkinter.CTkEntry(frameRegister, placeholder_text="Password...", show="*")
    passwordEntry.pack(padx=20, pady=10)

    # Botão de login
    loginButton = customtkinter.CTkButton(frameRegister, text="Login", command=lambda:login_render(frameRegister))
    loginButton.pack(padx=20, pady=5)

    # Botão de criar conta
    loginButton = customtkinter.CTkButton(frameRegister, text="Criar Conta", command=lambda:register_action(usernameEntry, passwordEntry,nameEntry, resultLabel))
    loginButton.pack(padx=20, pady=5)

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
    frameLogin = customtkinter.CTkFrame(app, width=600, height=500)
    frameLogin.pack(expand=True)

    # Labels e campos de entrada
    usernameLabel = customtkinter.CTkLabel(frameLogin, text="Username:")
    usernameLabel.pack(padx=20, pady=5)

    usernameEntry = customtkinter.CTkEntry(frameLogin, placeholder_text="Username...")
    usernameEntry.pack(padx=20, pady=10)

    passwordLabel = customtkinter.CTkLabel(frameLogin, text="Password:")
    passwordLabel.pack(padx=20, pady=5)

    passwordEntry = customtkinter.CTkEntry(frameLogin, placeholder_text="Password...", show="*")
    passwordEntry.pack(padx=20, pady=10)

    # Botão de login
    loginButton = customtkinter.CTkButton(frameLogin, text="Login", command=lambda:login_action(usernameEntry, passwordEntry, resultLabel, frameLogin))
    loginButton.pack(padx=20, pady=5)

    # Botão de criar conta
    createaccButton = customtkinter.CTkButton(frameLogin, text="Criar Conta", command=lambda:register_render(frameLogin))
    createaccButton.pack(padx=20, pady=5)

    # Label para exibir resultados ou mensagens de erro
    resultLabel = customtkinter.CTkLabel(frameLogin, text="")
    resultLabel.pack(padx=20, pady=20)


def mainwindow_render(oldFrame):
    """Rendriza a frame da janela principal"""

    oldFrame.destroy() # Apagar o estilo do frame anterior

    #Frame menu lateral
    menuFrame = customtkinter.CTkFrame(app, width=246, height=916, fg_color="#0E0D11",corner_radius=0)  
    menuFrame.place(x=0,y=0)

    #Frame barra inferior com os comandos da música
    playFrame = customtkinter.CTkFrame(app, width=1920, height=131, fg_color="#0A090C",corner_radius=0) 
    playFrame.place(x=0,y=650)

    #Frame separador user e home
    upperMenuFrame = customtkinter.CTkFrame(menuFrame, width=162, height=110, fg_color="transparent") 
    upperMenuFrame.place(x=42,y=44)

    #Frame separador collection
    collectionMenuFrame = customtkinter.CTkFrame(menuFrame, width=162, height=165, fg_color="transparent") 
    collectionMenuFrame.place(x=42,y=191)

    #Frame separador playlists
    playlistMenuFrame = customtkinter.CTkFrame(menuFrame, width=162, height=659, fg_color="transparent")  
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


    ############################## APLICAÇAO DAS IMAGENS NOS BUTTONS E LAYERS PARA CADA BUTTON######################
    ############################################### UpperMenuFrame ###############################################

    #Botão com Icon e texto de user
    btnUser = customtkinter.CTkButton(upperMenuFrame, image=userIcon, width=31, height=31, fg_color="transparent", text="User Name")
    btnUser.place(x=0, y=0)

    #Botão com Icon e texto de home
    btnHome = customtkinter.CTkButton(upperMenuFrame, image= homeIcon , width = 31, height = 31, fg_color="transparent", text="Home Page")
    btnHome.place(x=0, y=65)

    #---------------------------------------------------------------------------------------------------------------------

    #Label para o separador collection
    labelCollection = customtkinter.CTkLabel(collectionMenuFrame, text="Collection")
    labelCollection.place(x=0, y=0) # Inicio do frame

    #Botão com Icon e texto de musica
    btnMusic = customtkinter.CTkButton(collectionMenuFrame, image=musicIcon, width=31, height=31, fg_color="transparent", text="Music")
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

    #Botão com Icone de playlist
    btnPlaylist1 = customtkinter.CTkButton(playlistMenuFrame, image=playlistIcon, width=31, height=31, fg_color="transparent", text="Playlist1")
    btnPlaylist1.place(x=0, y=30)

    #Botão com Icone de playlist
    btnPlaylist2 = customtkinter.CTkButton(playlistMenuFrame, image=playlistIcon, width=31, height=31, fg_color="transparent", text="Playlist2")
    btnPlaylist2.place(x=0, y=76)
    
    #Botão com Icone de playlist
    btnPlaylist3 = customtkinter.CTkButton(playlistMenuFrame, image=playlistIcon, width=31, height=31, fg_color="transparent", text="Playlist3")
    btnPlaylist3.place(x=0, y=122)

    #---------------------------------------------------------------------------------------------------------------------

    ##################################IMAGENS PARA OS BUTTONS#############################################################
    ####################################### PLAYFRAME ###############################################

    # Icon de play
    playIcon = customtkinter.CTkImage(Image.open(f"{imagePath}play_icon.png"), size=(34, 34))

    # Icon de avançar música
    forwardIcon = customtkinter.CTkImage(Image.open(f"{imagePath}forward_icon.png"), size=(20, 20))

    # Icon de recuar música
    backIcon = customtkinter.CTkImage(Image.open(f"{imagePath}back_icon.png"), size=(20, 20))

    # Icon de áudio
    audioIcon = customtkinter.CTkImage(Image.open(f"{imagePath}audio_icon.png"), size=(20, 20)) 

    ############################## APLICAÇAO DAS IMAGENS NOS BUTTONS E LAYERS PARA CADA BUTTON######################
    ############################################### FRAMES BARRA MUSICA ###############################################
    #Frame com conteúdo
    musicContentFrame = customtkinter.CTkFrame(playFrame, width=1600, height=70, fg_color="#0A090C")
    musicContentFrame.place(x=107, y=43)

    #Frame para mostrar música e info na barra inferior
    showMusicFrame = customtkinter.CTkFrame(musicContentFrame, width=170, height=53, fg_color="#0A090C")
    showMusicFrame.place(x=0, y=0)

    #Frame dos botões para controlar música
    musicActionFrame = customtkinter.CTkFrame(musicContentFrame, width=626, height=100, fg_color="#0A090C")
    musicActionFrame.place(x=400, y=0)
    
    #Frame slider de aúdio
    audioSliderFrame = customtkinter.CTkFrame(musicContentFrame, width=150, height=30, fg_color="#0A090C")
    audioSliderFrame.place(x=1200, y=16.5)

    #-------------------------------------------------------------------------------------------------------

    #-------------------------------------[FRAME INFO]-------------------------------------------------------------

    #Frame para mostrar info: Nome da música e artista
    musicInfoFrame = customtkinter.CTkFrame(showMusicFrame, width=90, height=50, fg_color="#0A090C")
    musicInfoFrame.place(x=72, y=7)

    #Capa da Música (substituir por imagem)
    musicCover = customtkinter.CTkButton(showMusicFrame, width=53, height=53, text="", fg_color="Red")
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
    btnPlay = customtkinter.CTkButton(controlBtnFrame, image=playIcon, width=34, height=34, fg_color="transparent", text="")
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
    command=mute_volume)
    btnAudio.place(x=0, y=0)

    #Slider de audio
    volumeSlider = customtkinter.CTkSlider(audioSliderFrame,width=100, from_=0, to=100, number_of_steps=100)
    volumeSlider.set(50)
    volumeSlider.place(x=40, y=8)
"""
def adjust_volume(val):


    # Converter o valor do slider para o intervalo real de volume
    volume_level = float(val) / 100.0  
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate( IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    # Ajusta o volume no dispositivo
    volume.SetMasterVolumeLevelScalar(volume_level, None)

is_muted = False
def mute_volume():
    global is_muted  # Para alterar a variável global de estado

    # Obter o dispositivo padrão de áudio
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

    # Obter a interface de controle de volume
    volume = interface.QueryInterface(IAudioEndpointVolume)

    # Verificar o estado atual e alternar
    if is_muted:
        volume.SetMute(0, None)  # Desativa o mute
        is_muted = False  # Atualiza o estado para desmutado
    else:
        volume.SetMute(1, None)  # Ativa o mute
        is_muted = True  # Atualiza o estado para mutado
"""
##########################################################

login_render("")

# Loop de event listening
app.mainloop()