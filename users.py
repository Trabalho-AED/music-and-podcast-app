from file_management import *

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
    create_sub_folders(f"db{pathFormat}users{pathFormat}{username}")
    create_sub_folders(f"db{pathFormat}users{pathFormat}{username}{pathFormat}playlists")
    create_main_files(f"db{pathFormat}users{pathFormat}{username}{pathFormat}favorites.csv")
    with open(accountsPath, "a", encoding="utf-8") as file:
        file.write(accountAdd) # Escreve os dados no ficheiro

    return