import customtkinter
from PIL import Image
from tkinter import filedialog
import shutil #Copy images shutil.copy() https://docs.python.org/3/library/shutil.html
import re #Regex for expression check(username and password)
import os
#from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#from comtypes import CLSCTX_ALL
import tkinter as tk
from io import StringIO
from tkinter import ttk
#from tkVideoPlayer import TkinterVideo   #https://pypi.org/project/tkvideoplayer/ 
import webbrowser                        # https://docs.python.org/3/library/webbrowser.html 

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light" Alterar entre tema escuro e claro
#customtkinter.set_default_color_theme(".\\theme\\rime.json") # Tema de cores

################################[VERIFICAR SISTEMA OPERATIVO]######################################
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
######################################################################################################


#################################[CRIAR PASTAS]#######################################################
def create_main_folders(folderPath):
    #Cria as pastas principais

    #Caso não exista
    if not os.path.exists(f".{pathFormat}{folderPath}{pathFormat}"):
        os.mkdir(f".{pathFormat}{folderPath}{pathFormat}")
    #Caso exista
    else:
        print(f"Folder already exists: {folderPath}")

def create_sub_folders(folderPath):
    """Cria as subpastas"""

    #Caso não exista
    if not os.path.exists(f".{pathFormat}{folderPath}{pathFormat}"):
        os.mkdir(f".{pathFormat}{folderPath}{pathFormat}")
    #Caso exista
    else:
        print(f"Sub Folder already exists: {folderPath}")

mainFolders = ["audios", "images", "db"] # Lista com as pastas principais
subFolders = [f"images{pathFormat}cover_art", f"images{pathFormat}icons", f"audios{pathFormat}music"] # Lista com as pastas secundárias

#Criar Pastas
for folder in mainFolders:
    create_main_folders(folder) 

#Criar Subpastas
for folder in subFolders:
    create_sub_folders(folder)
##########################################################################################################


###############################[CRIAR FICHEIROS]##########################################################
def create_main_files(filePath):
    """Cria o ficheiro caso ele não exista."""

    #Caso não exista
    if not os.path.exists(filePath):
        # Abre o ficheiro no modo write, criando-o caso não exista.
        with open(filePath, "w", encoding="utf-8") as file:
            #Adiciona o username admin por defeito à lista de admins
            if filePath == f".{pathFormat}db{pathFormat}admin_list.csv":
                file.writelines("admin")
                file.close()
            #Adiciona o user admin com o username admin e password admin por defeito à lista de utilizadores por defeito
            elif filePath == f".{pathFormat}db{pathFormat}user_accounts.csv":
                file.writelines("admin;admin;Admin")
                file.close()
            else:
                pass  # O ficheiro será criado vazio.
        print(f"File created: {filePath}")
    #Caso já exista
    else:
        print(f"File already exists: {filePath}")

#Lista com os ficheiros da base de dados
mainFiles = [f".{pathFormat}db{pathFormat}user_accounts.csv",f".{pathFormat}db{pathFormat}podcast_list.csv",f".{pathFormat}db{pathFormat}music_list.csv",f".{pathFormat}db{pathFormat}admin_list.csv"]

#Criar ficheiros
for file in mainFiles:
    create_main_files(file)
############################################################################################################


##########################################[CAMINHOS]############################################################

imagePath = f".{pathFormat}images{pathFormat}icons{pathFormat}" # Caminho para o diretório onde são armazenadas as imagens
accountsPath = f".{pathFormat}db{pathFormat}user_accounts.csv" # Caminho para o ficheiro onde são armazenadas as contas
musicPath = f".{pathFormat}db{pathFormat}music_list.csv" # Caminho para o ficheiro onde são armazenadas as músicas
podcastPath = f".{pathFormat}db{pathFormat}podcast_list.csv" # Caminho para o ficheiro onde são armazenadas os podcasts
adminListfile = f".{pathFormat}db{pathFormat}admin_list.csv" # Caminho para o ficheiro onde são armazenadas as contas admin
coverArtPath = f".{pathFormat}images{pathFormat}cover_art{pathFormat}" # Caminho para o diretório onde são armazenadas as imagens das músicas
musicAudioPath = f".{pathFormat}audios{pathFormat}music{pathFormat}" # Caminho para o diretório onde são armazenadas as músicas

#################################################################################################################


###########################################################
currentFrame = None # Guarda o frame que o utilizador se encontra
isAdmin = False # Booleano que diz se o utilizador é ou não admin
tempCoverName = None # Para salvar o nome da imagem da música
tempAudioName = None # Para salvar o nome do aúdio da música
###########################################################

# Inicializar app
app = customtkinter.CTk()

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
        
def register_action(usernameEntry, passwordEntry,nameEntry, resultLabel):
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
    
    return

##########################################################




#############################[RENDER SCREENS]##########################################
def register_render(oldFrame):
    """Renderiza a frame do formulário de registo"""

    print("Register") # Mensagem de confirmação na consola

    oldFrame.destroy() # Apagar o estilo do frame anterior

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

    global currentFrame # Variável global do frame em uso

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
        addBtn = customtkinter.CTkButton(upperSearchFrame, width=100, height=10, fg_color="transparent", text="Add Music", command=add_music)
        addBtn.place(x=100, y=30)

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
    btnUser = customtkinter.CTkButton(upperMenuFrame, image=userIcon, width=31, height=31, fg_color="transparent", text="User Name",command=lambda:userpage_render(mainContentFrame, currentFrame))
    btnUser.place(x=0, y=0)

    #Botão com Icon e texto de home
    btnHome = customtkinter.CTkButton(upperMenuFrame, image= homeIcon , width = 31, height = 31, fg_color="transparent", text="Home Page", command=lambda:homepage_render(mainContentFrame, currentFrame))
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
    # Frame com conteúdo
    musicContentFrame = customtkinter.CTkFrame(playFrame, width=2000, height=70, fg_color="#0A090C")
    musicContentFrame.place(x=107, y=43)

    # Configurar o layout em grid com proporções
    musicContentFrame.columnconfigure(0, weight=1)  # Coluna para `showMusicFrame`
    musicContentFrame.columnconfigure(1, weight=1)  # Coluna para `musicActionFrame`
    musicContentFrame.columnconfigure(2, weight=1)  # Coluna para `audioSliderFrame`

    # Frame para mostrar música e info na barra inferior
    showMusicFrame = customtkinter.CTkFrame(musicContentFrame, fg_color="#0A090C")
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
    command="")
    btnAudio.place(x=0, y=0)

    #Slider de audio
    volumeSlider = customtkinter.CTkSlider(audioSliderFrame,width=100, from_=0, to=100, number_of_steps=100)
    volumeSlider.set(50)
    volumeSlider.place(x=40, y=8)

    homepage_render(mainContentFrame, currentFrame) # Mostra a homepage por defeito


def userpage_render(mainContentFrame, oldFrame):
    """Mostra o frame da página de utilizador"""

    global currentFrame # Variável global para frame a ser usado

    oldFrame.destroy() # Apagar o estilo do frame anterior

    #Frame User Menu
    userFrame = customtkinter.CTkFrame(mainContentFrame, width=1674, height=890, fg_color="green",corner_radius=0)  
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

def read_content(contentType):
    if contentType == "podcast":
        with open(podcastPath, "r", encoding="utf-8") as file:
            podcastList = file.readlines()
        return podcastList


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
    trendingFrame = customtkinter.CTkFrame(homepageFrame, width=500, height=200, fg_color="blue", corner_radius=0)
    trendingFrame.grid(row=0, column=0, padx=150, pady=150)

    podcastList = read_content("podcast")

    for i in range(len(podcastList)):
        podcastURL = podcastList[i].strip("\n")
        podcastButton = customtkinter.CTkButton(homepageFrame, width=200, height=100, command=lambda:podcast_video_render(podcastURL))
        podcastButton.grid(row=i, column=0, padx=90,pady=90)

    """
    #Frame menu trending Podcasts
    trendingPodcastsFrame = customtkinter.CTkFrame(homepageFrame, width=1400, height=200, fg_color="blue",corner_radius=0)  #0E0D11
    trendingPodcastsFrame.grid(row=1, column=0, padx=150, pady=150)

    #Frame menu Your Activity
    yourActivityFrame = customtkinter.CTkFrame(homepageFrame, width=1400, height=200, fg_color="blue",corner_radius=0)  
    yourActivityFrame.grid(row=2, column=0, padx=150, pady=150)

    #Frame menu Our Reccomendations
    ourReccomendationsFrame = customtkinter.CTkFrame(homepageFrame, width=1400, height=200, fg_color="blue",corner_radius=0)  
    ourReccomendationsFrame.grid(row=3, column=0, padx=150, pady=150)"""

def podcast_video_render(videoURL):
    """
    Abre o browser definido por defeito com um url
    """
    webbrowser.open(videoURL, new = 0, autoraise=True)
    
##########################################################

login_render("")

# Loop de event listening
app.mainloop()