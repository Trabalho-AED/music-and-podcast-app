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