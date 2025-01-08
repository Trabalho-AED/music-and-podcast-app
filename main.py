import customtkinter
from PIL import Image
import os

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
appWidth = 1920
appHeight = 1080

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

    oldFrame.pack_forget() # Apagar o estilo do frame anterior

    ###################################FRAMES#################################################

    #Frame menu lateral
    menuFrame = customtkinter.CTkFrame(app, width=246, height=890, fg_color="#0E0D11",corner_radius=0)  
    menuFrame.place(x=0,y=0)

    #Frame barra inferior com os comandos da música
    playFrame = customtkinter.CTkFrame(app, width=1920, height=139, fg_color="#0A090C",corner_radius=0) 
    playFrame.place(x=0,y=890)

    #Frame separador user e home
    upperMenuFrame = customtkinter.CTkFrame(menuFrame, width=162, height=139, fg_color="transparent") 
    upperMenuFrame.place(x=42,y=44)

    #Frame separador collection
    collectionMenuFrame = customtkinter.CTkFrame(menuFrame, width=162, height=204, fg_color="transparent") 
    collectionMenuFrame.place(x=42,y=224)

    #Frame separador playlists
    playlistMenuFrame = customtkinter.CTkFrame(menuFrame, width=162, height=460, fg_color="transparent")  
    playlistMenuFrame.place(x=42,y=442)

    ##################################IMAGENS PARA OS BUTTONS#############################################################
    ####################################### OPTIONSFRAME ###############################################

    # Icon user
    userIcon = customtkinter.CTkImage(Image.open(f"{imagePath}user_icon.png"), size=(39, 39))

    # Icon home
    homeIcon = customtkinter.CTkImage(Image.open(f"{imagePath}home_icon.png"), size=(39, 39))

    # Icon música
    musicIcon = customtkinter.CTkImage(Image.open(f"{imagePath}music_icon.png"), size=(39, 39))

    # Icon artista
    artistIcon = customtkinter.CTkImage(Image.open(f"{imagePath}singer_icon.png"), size=(39, 39))

    # Icon favoritos
    favoriteIcon = customtkinter.CTkImage(Image.open(f"{imagePath}favorite_icon.png"), size=(39, 39))

    # Icon playlist
    playlistIcon = customtkinter.CTkImage(Image.open(f"{imagePath}playlist_icon.png"), size=(39, 39))


    ############################## APLICAÇAO DAS IMAGENS NOS BUTTONS E LAYERS PARA CADA BUTTON######################
    ############################################### OPTIONSFRAME ###############################################

    #Botão com Icon e texto de user
    btnUser = customtkinter.CTkButton(upperMenuFrame, image=userIcon, width=39, height=39, fg_color="transparent", text="User Name")
    btnUser.place(x=0, y=0)

    #Botão com Icon e texto de home
    btnHome = customtkinter.CTkButton(upperMenuFrame, image= homeIcon , width = 39, height = 39, fg_color="transparent", text="Home Page")
    btnHome.place(x=0, y=90)

    #---------------------------------------------------------------------------------------------------------------------

    #Label para o separador collection
    labelCollection = customtkinter.CTkLabel(collectionMenuFrame, text="Collection")
    labelCollection.place(x=0, y=0) # Inicio do frame

    #Botão com Icon e texto de musica
    btnMusic = customtkinter.CTkButton(collectionMenuFrame, image=musicIcon, width=39, height=39, fg_color="transparent", text="Music")
    btnMusic.place(x=0, y=30)

    #Botão com Icon e texto de podcast
    btnPodcast = customtkinter.CTkButton(collectionMenuFrame, image=artistIcon, width=39, height=39, fg_color="transparent", text="Podcast")
    btnPodcast.place(x=0, y=84)

    #Botão com Icon e texto de Favoritos
    btnFavorites = customtkinter.CTkButton(collectionMenuFrame, image=favoriteIcon, width=39, height=39, fg_color="transparent", text="Favorites")
    btnFavorites.place(x=0, y=138)

    #---------------------------------------------------------------------------------------------------------------------
    
    #Label para o separador playlists
    labelPlaylists = customtkinter.CTkLabel(playlistMenuFrame, text="Playlists")
    labelPlaylists.place(x=0, y=0) # Inicio do frame

    ####[PLAYLISTS, mudar para criar as playlists mais tarde]####

    #Botão com Icone de playlist
    btnPlaylist1 = customtkinter.CTkButton(playlistMenuFrame, image=playlistIcon, width=39, height=39, fg_color="transparent", text="Playlist1")
    btnPlaylist1.place(x=0, y=30)

    #Botão com Icone de playlist
    btnPlaylist2 = customtkinter.CTkButton(playlistMenuFrame, image=playlistIcon, width=39, height=39, fg_color="transparent", text="Playlist2")
    btnPlaylist2.place(x=0, y=84)
    
    #Botão com Icone de playlist
    btnPlaylist3 = customtkinter.CTkButton(playlistMenuFrame, image=playlistIcon, width=39, height=39, fg_color="transparent", text="Playlist3")
    btnPlaylist3.place(x=0, y=138)

    #---------------------------------------------------------------------------------------------------------------------

    ##################################IMAGENS PARA OS BUTTONS#############################################################
    ####################################### MUSICFRAME ###############################################

    # Icon de play
    playIcon = customtkinter.CTkImage(Image.open(f"{imagePath}play_icon.png"), size=(53, 53))

    # Icon de avançar música
    forwardIcon = customtkinter.CTkImage(Image.open(f"{imagePath}forward_icon.png"), size=(53, 53))

    # Icon de recuar música
    backIcon = customtkinter.CTkImage(Image.open(f"{imagePath}back_icon.png"), size=(53, 53))

    # Icon de áudio
    audioIcon = customtkinter.CTkImage(Image.open(f"{imagePath}audio_icon.png"), size=(53, 53)) 

    ############################## APLICAÇAO DAS IMAGENS NOS BUTTONS E LAYERS PARA CADA BUTTON######################
    ############################################### MUSICFRAME ###############################################

    #Frame para mostrar música e info na barra inferior
    showMusicFrame = customtkinter.CTkFrame(playFrame, width=180, height=53, fg_color="#0A090C")
    showMusicFrame.place(x=151, y=35)

    #Frame para mostrar info: Nome da música e artista
    musicInfoFrame = customtkinter.CTkFrame(showMusicFrame, width=90, height=49, fg_color="#0A090C")
    musicInfoFrame.place(x=88, y=3)

    #Capa da Música (substituir por imagem)
    musicCover = customtkinter.CTkButton(showMusicFrame, width=53, height=53, text="", fg_color="Red")
    musicCover.place(x=0,y=0)

    #Nome da música
    musicName = customtkinter.CTkLabel(musicInfoFrame, text="Music Name", font=("Arial", 17))
    musicName.place(x=0, y=0)

    #Nome do artista
    artistName = customtkinter.CTkLabel(musicInfoFrame, text="Artist Name", font=("Arial", 12) )
    artistName.place(x=0, y=24)

    #---------------------------------------------------------------------------------------------------------------------
    
    #Frame dos botões para controlar música
    musicActionFrame = customtkinter.CTkFrame(playFrame, width=260, height=60, fg_color="#0A090C")
    musicActionFrame.place(x=902, y=35)

    #Botão com Icone de recuar
    btnBack = customtkinter.CTkButton(musicActionFrame, image=backIcon, width=53, height=53, fg_color="transparent", text="")
    btnBack.place(x=0, y=0)

    #Botão com Icone de play
    btnPlay = customtkinter.CTkButton(musicActionFrame, image=playIcon, width=53, height=53, fg_color="transparent", text="")
    btnPlay.place(x=88, y=0)

    #Botão com Icone de avançar
    btnForward = customtkinter.CTkButton(musicActionFrame, image=forwardIcon, width=53, height=53, fg_color="transparent", text="")
    btnForward.place(x=176, y=0)

    #------------------------------------------------------------------------------------------------------------------------

    #Frame slider de aúdio (adicionar lógica)
    audioSliderFrame = customtkinter.CTkFrame(playFrame, width=80, height=80, fg_color="#0A090C")
    audioSliderFrame.place(x=1716, y=35)

    #Botão com Icone do áudio
    btnAudio = customtkinter.CTkButton(audioSliderFrame, image=audioIcon, width=53, height=53, fg_color="transparent", text="")
    btnAudio.place(x=0, y=0)

##########################################################

login_render("")

# Loop de event listening
app.mainloop()