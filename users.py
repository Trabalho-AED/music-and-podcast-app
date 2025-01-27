import re

from file_management import *

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

def save_preferences(usernameFinal, checkVarMusic, checkVarPodcast, checkVarOthers):
    saveList = []

    if checkVarMusic.get() == "on":
        saveList.append("music")
    if checkVarPodcast.get() == "on":
        saveList.append("podcast")
    if checkVarOthers.get() == "on":
        saveList.append("others")
    
    if len(saveList) == 0:
        saveString=""
    else:
        saveString = ""
        for element in saveList:
            saveString+=element+"\n"

    with open(f"{usersPath}{usernameFinal}{pathFormat}notification.csv", "w", encoding="utf-8") as file:
        file.write(saveString)

def set_check_var(usernameFinal, checkVarMusic, checkVarPodcast, checkVarOthers):
    with open(f"{usersPath}{usernameFinal}{pathFormat}notification.csv", "r", encoding="utf-8") as file:
        lines=file.readlines()

    for line in lines:
        if line.strip() == "music":
            checkVarMusic.set("on")
        if line.strip() == "podcast":
            checkVarPodcast.set("on")
        if line.strip() == "others":
            checkVarOthers.set("on")

def create_account(username, password, name):
    """Cria uma conta"""

    accountAdd = username+";"+password+";"+name+"\n" # String com o Formato dos dados
    create_sub_folders(f"files{pathFormat}users{pathFormat}{username}")
    create_sub_folders(f"files{pathFormat}users{pathFormat}{username}{pathFormat}playlists")
    create_main_files(f"files{pathFormat}users{pathFormat}{username}{pathFormat}favorites.csv")
    create_main_files(f"files{pathFormat}users{pathFormat}{username}{pathFormat}music_activity.csv")
    create_main_files(f"files{pathFormat}users{pathFormat}{username}{pathFormat}podcast_activity.csv")
    create_main_files(f"files{pathFormat}users{pathFormat}{username}{pathFormat}notification.csv")
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