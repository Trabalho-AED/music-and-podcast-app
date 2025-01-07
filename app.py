import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light" Alterar entre tema escuro e claro
#customtkinter.set_default_color_theme(".\\theme\\rime.json") # Tema de cores

accounts_path = "user_accounts.csv" # Caminho para o ficheiro onde são armazenadas as contas
admin_listfile = "admin_list.csv" # Caminho para o ficheiro onde são armazenadas as contas que são admin

# Inicializar app
app = customtkinter.CTk()

# Titulo da app
app.title("Login Form")

# Define a dimensão da app
appWidth = 600
appHeight = 500
# Obtém a dimensão do ecrã
screenWidth = app.winfo_screenwidth()
screenHeight = app.winfo_screenheight()

# Calcula a posição para centralizar a janela
x = (screenWidth / 2) - (appWidth / 2)
y = (screenHeight / 2) - (appHeight / 2)

# Define o tamanho da app e começa no centro da tela
app.geometry(f"{appWidth}x{appHeight}+{int(x)}+{int(y)}")

def get_accounts(username,password):
    with open(accounts_path, encoding="utf-8") as file:
        lines = file.readlines()
    
    for line in lines:
        campos = line.strip().split(";")
        if campos[0] == username and campos[1] == password:
            return campos[0], campos[1], campos[2]
    
    return "not_found", "not_found", ""

def check_admin(username):
    with open(admin_listfile, encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        if line.strip() == username:
            return True
    return False

# Criar o formulário de login
def login_action(username_entry, password_entry, result_label):
    username = username_entry.get()
    password = password_entry.get()
    if username == "" or password == "":
        result_label.configure(text="Preencha todos os campos.")
        return
    print(f"Username: {username}, Password: {password}")  # Substituir por lógica real de autenticação
    username, password, name = get_accounts(username, password)

    is_admin = check_admin(username)
    if is_admin:
        adminflag = "Admin"
    else:
        adminflag = "Não Admin"
    if username == "not_found" and password == "not_found":
        result_label.configure(text="Utilizador Inexistente.")
    else:
        result_label.configure(text=f"Bem vindo {name}, Login realizado com sucesso!\nTipo de Utilizador: {adminflag}")


################[RENDER SCREENS]##########################
def register_render(oldFrame):
    print("Register")
    oldFrame.pack_forget()
    ################[LOGIN FORM]##############################
    #Frame
    frameRegister = customtkinter.CTkFrame(app, width=600, height=500)
    frameRegister.pack(expand=True)

    # Labels e campos de entrada
    name_label = customtkinter.CTkLabel(frameRegister, text="Nome:")
    name_label.pack(padx=20, pady=5)

    name_entry = customtkinter.CTkEntry(frameRegister, placeholder_text="Nome...")
    name_entry.pack(padx=20, pady=10)

    username_label = customtkinter.CTkLabel(frameRegister, text="Username:")
    username_label.pack(padx=20, pady=5)

    username_entry = customtkinter.CTkEntry(frameRegister, placeholder_text="Username...")
    username_entry.pack(padx=20, pady=10)

    password_label = customtkinter.CTkLabel(frameRegister, text="Password:")
    password_label.pack(padx=20, pady=5)

    password_entry = customtkinter.CTkEntry(frameRegister, placeholder_text="Password...", show="*")
    password_entry.pack(padx=20, pady=10)

    # Botão de login
    login_button = customtkinter.CTkButton(frameRegister, text="Login", command=lambda:login_render(frameRegister))
    login_button.pack(padx=20, pady=5)

    # Botão de criar conta
    login_button = customtkinter.CTkButton(frameRegister, text="Criar Conta", command=register_render)
    login_button.pack(padx=20, pady=5)

    # Label para exibir resultados ou mensagens de erro
    result_label = customtkinter.CTkLabel(frameRegister, text="")
    result_label.pack(padx=20, pady=20)
    #######################################################

##########################################################

def login_render(oldFrame):
    if oldFrame == "":
        pass
    else:
        oldFrame.pack_forget()
    ################[LOGIN FORM]##############################
    #Frame
    frameLogin = customtkinter.CTkFrame(app, width=600, height=500)
    frameLogin.pack(expand=True)

    # Labels e campos de entrada
    username_label = customtkinter.CTkLabel(frameLogin, text="Username:")
    username_label.pack(padx=20, pady=5)

    username_entry = customtkinter.CTkEntry(frameLogin, placeholder_text="Username...")
    username_entry.pack(padx=20, pady=10)

    password_label = customtkinter.CTkLabel(frameLogin, text="Password:")
    password_label.pack(padx=20, pady=5)

    password_entry = customtkinter.CTkEntry(frameLogin, placeholder_text="Password...", show="*")
    password_entry.pack(padx=20, pady=10)

    # Botão de login
    login_button = customtkinter.CTkButton(frameLogin, text="Login", command=lambda:login_action(username_entry, password_entry, result_label))
    login_button.pack(padx=20, pady=5)

    # Botão de criar conta
    login_button = customtkinter.CTkButton(frameLogin, text="Criar Conta", command=lambda:register_render(frameLogin))
    login_button.pack(padx=20, pady=5)

    # Label para exibir resultados ou mensagens de erro
    result_label = customtkinter.CTkLabel(frameLogin, text="")
    result_label.pack(padx=20, pady=20)
    #######################################################

login_render("")
# Loop de event listening
app.mainloop()