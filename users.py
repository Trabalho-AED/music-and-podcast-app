from file_management import *
import re
import os

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