import customtkinter

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

# Criar o formulário de login
def login_action():
    username = username_entry.get()
    password = password_entry.get()
    print(f"Username: {username}, Password: {password}")  # Substituir por lógica real de autenticação
    if username == "test" and password == "teste":
        result_label.configure(text="Login realizado com sucesso!" if username and password else "Preencha todos os campos.")
    else:
        result_label.configure(text="Conta inexistente!" if username and password else "Preencha todos os campos.")

# Labels e campos de entrada
username_label = customtkinter.CTkLabel(app, text="Username:")
username_label.pack(expand=True)

username_entry = customtkinter.CTkEntry(app, placeholder_text="Username...")
username_entry.pack(expand=True)

password_label = customtkinter.CTkLabel(app, text="Password:")
password_label.pack(expand=True)

password_entry = customtkinter.CTkEntry(app, placeholder_text="Password...", show="*")
password_entry.pack(expand=True)

# Botão de login
login_button = customtkinter.CTkButton(app, text="Login", command=login_action)
login_button.pack(expand=True)

# Label para exibir resultados ou mensagens de erro
result_label = customtkinter.CTkLabel(app, text="")
result_label.pack(pady=(10, 5))

# Loop de event listening
app.mainloop()
