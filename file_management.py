import os

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

def read_file(path):
    """Lê um ficheiro com qualquer opção.
    Retorna o conteúdo do ficheiro"""

    #Abre o ficheiro
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines() # Lê o ficheiro
    
    return lines # Retorna o conteúdo

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
subFolders = [f"images{pathFormat}cover_art", f"images{pathFormat}icons", f"audios{pathFormat}music", f"db{pathFormat}users" ] # Lista com as pastas secundárias

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
mainFiles = [f".{pathFormat}db{pathFormat}categories.csv",f".{pathFormat}db{pathFormat}category_list.csv",f".{pathFormat}db{pathFormat}user_accounts.csv",f".{pathFormat}db{pathFormat}podcast_list.csv",f".{pathFormat}db{pathFormat}music_list.csv",f".{pathFormat}db{pathFormat}admin_list.csv"]

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
categoriesFile = f".{pathFormat}db{pathFormat}categories.csv" # Caminho para o ficheiro onde são armazenadas as categorias
coverArtPath = f".{pathFormat}images{pathFormat}cover_art{pathFormat}" # Caminho para o diretório onde são armazenadas as imagens das músicas
musicAudioPath = f".{pathFormat}audios{pathFormat}music{pathFormat}" # Caminho para o diretório onde são armazenadas as músicas
categoriesPath = f".{pathFormat}db{pathFormat}category_list.csv" # Caminho para o ficheiro onde são armazenadas as categorias
usersPath = f".{pathFormat}db{pathFormat}users{pathFormat}" # Caminho para o diretório onde são armazenadas os users na db
#################################################################################################################