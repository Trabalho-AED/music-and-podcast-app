import customtkinter
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

    OptionsFrame = customtkinter.CTkFrame(app, width=246, height=890, fg_color="green")  #Frame grande das opcoes laterais lado direito 
    #OptionsFrame.pack(expand=True)
    OptionsFrame.place(x=0,y=0)

    MusicFrame = customtkinter.CTkFrame(app, width=1920, height=139, fg_color="red") #Frame Grande em baixo onde se pode pausar a musica
    #MusicFrame.pack(expand=True)
    MusicFrame.place(x=0,y=890)

    CollectionsFrame = customtkinter.CTkFrame(OptionsFrame, width=200, height=200, fg_color="blue") #Frame collection dentro da Optionsframe 
    CollectionsFrame.place(x=0,y=890)

    PlaylistFrame = customtkinter.CTkFrame(OptionsFrame, width=200, height=200, fg_color="blue") #Frame Playlist dentro da Optionsframe 
    PlaylistFrame.place(x=0,y=890)

##################################IMAGENS PARA OS BUTTONS#############################################################
####################################### OPTIONSFRAME ###############################################

    ImageIconbtn = customtkinter.CTkImage(Image.open(".\\image\\icons\\icone.png"), size=(39, 39))

    ImageHomebtn = customtkinter.CTkImage(Image.open(".\\image\\icons\\homeicone.png"), size=(39, 39))

    ImageMusicButton = customtkinter.CTkImage(Image.open(".\\image\\icons\\homeicone.png"), size=(39, 39))

    ImageArtistButton = customtkinter.CTkImage(Image.open(".\\image\\icons\\cantor.png"), size=(39, 39))


############################## APLICAÇAO DAS IMAGENS NOS BUTTONS E LAYERS PARA CADA BUTTON######################
############################################### OPTIONSFRAME ###############################################


    btnIcon = customtkinter.CTkLabel(OptionsFrame, image= ImageIconbtn , width = 39, height = 39,fg_color="transparent")
    btnUser.place(x=10, y=470)

    LabelIcone = customtkinter.CTkLabel(OptionsFrame,text='Nome da Aplicaçao',text_color="white", font=("Helvetica", 14))
#---------------------------------------------------------------------------------------------------------------------
    btnHome = customtkinter.CTkLabel(OptionsFrame, image= ImageHomebtn , width = 39, height = 39,fg_color="transparent")
    btnHome.place(x=10, y=470)

    LabelHome = customtkinter.CTkLabel(OptionsFrame,text='Home',text_color="white", font=("Helvetica", 14))
#---------------------------------------------------------------------------------------------------------------------

    btnMusic = customtkinter.CTkLabel(CollectionsFrame, image= ImageMusicButton , width = 39, height = 39,fg_color="transparent")
    btnMusic.place(x=10, y=470)

    btnMusic = customtkinter.CTkLabel(CollectionsFrame,text='Music',text_color="white", font=("Helvetica", 14))

#---------------------------------------------------------------------------------------------------------------------

    btnArtist = customtkinter.CTkLabel(CollectionsFrame, image= ImageArtistButton , width = 39, height = 39,fg_color="transparent")
    btnArtist.place(x=10, y=470)

    btnArtist = customtkinter.CTkLabel(CollectionsFrame,text='Artist',text_color="white", font=("Helvetica", 14))


##################################IMAGENS PARA OS BUTTONS#############################################################
####################################### MUSICFRAME ###############################################

    ImagePlaybtn = customtkinter.CTkImage(Image.open(".\\image\\icons\\play.png"), size=(39, 39))

    ImagePausebtn = customtkinter.CTkImage(Image.open(".\\image\\icons\\pause.png"), size=(39, 39))

    ImageSkipButton = customtkinter.CTkImage(Image.open(".\\image\\icons\\skip.png"), size=(39, 39))

    ImageGobackButton = customtkinter.CTkImage(Image.open(".\\image\\icons\\goback.png"), size=(39, 39))

    ImageAudioButton = customtkinter.CTkImage(Image.open(".\\image\\icons\\audio.png"), size=(39, 39))


############################## APLICAÇAO DAS IMAGENS NOS BUTTONS E LAYERS PARA CADA BUTTON######################
############################################### MUSICFRAME ###############################################

    btnPlay = customtkinter.CTkLabel(MusicFrame, image= ImagePlaybtn , width = 39, height = 39,fg_color="transparent")
    btnPlay.place(x=10, y=470)

    btnPause = customtkinter.CTkLabel(MusicFrame, image= ImagePausebtn , width = 39, height = 39,fg_color="transparent")
    btnPause.place(x=10, y=470)

    btnSkip = customtkinter.CTkLabel(MusicFrame, image= ImageSkipButton , width = 39, height = 39,fg_color="transparent")
    btnSkip.place(x=10, y=470)

    btnGoback = customtkinter.CTkLabel(MusicFrame, image= ImageGobackButton , width = 39, height = 39,fg_color="transparent")
    btnGoback.place(x=10, y=470)

    btnAudio = customtkinter.CTkLabel(MusicFrame, image= ImageAudioButton , width = 39, height = 39,fg_color="transparent")
    btnAudio.place(x=10, y=470)

















##########################################################

login_render("")
# Loop de event listening
app.mainloop()