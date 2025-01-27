import os
import shutil 

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
mainFiles = [f".{pathFormat}db{pathFormat}auto_notifications.txt", f".{pathFormat}db{pathFormat}custom_notifications.txt",f".{pathFormat}db{pathFormat}categories.csv",f".{pathFormat}db{pathFormat}user_accounts.csv",f".{pathFormat}db{pathFormat}podcast_list.csv",f".{pathFormat}db{pathFormat}music_list.csv",f".{pathFormat}db{pathFormat}admin_list.csv"]

#Criar ficheiros
for file in mainFiles:
    create_main_files(file)
############################################################################################################
def write_notifications(name,author,type):
    updatedLine = f"{type};{name};{author}\n"  # Create the new line to write

    # Read the current contents of the file
    with open(autoNotificationFile, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Initialize an empty list for modified lines
    modifiedLines = []
    replaced = False

    # Check and replace the existing line by type
    for line in lines:
        if line.startswith(f"{type};"):  # Match the type (music or podcast)
            modifiedLines.append(updatedLine)  # Replace the line
            replaced = True
        else:
            modifiedLines.append(line)  # Keep the other lines as they are

    if not replaced:
        modifiedLines.append(updatedLine)  # Add the new line if no match was found

    # Write all modified lines back to the file
    with open(autoNotificationFile, "w", encoding="utf-8") as file:
        file.writelines(modifiedLines)

def get_categories():
    categoriesList = []

    with open(categoriesFile, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    for line in lines:
        categoriesList.append(line.strip())

    return categoriesList

def confirm_categories(categoriesNameEntry, erroradd_categoriesLabel):
    """Guarda os dados da música a adicionar"""

    if categoriesNameEntry.get():
        #Variável com a estrutura de dados
        categoryData = f"{categoriesNameEntry.get()}\n"

        #Abre o caminho da música no formato "append" para adicionar a linha sem apagar o conteúdo existente
        with open(categoriesFile, "a", encoding="utf-8") as file:
            file.writelines(categoryData) # escreve os dados com a estrutura anteriormente definida
            file.close
        
        #Apagar conteúdo
        categoriesNameEntry.delete(0,"end")
        erroradd_categoriesLabel.configure(text="Category added with success!")

        return

    else:
        erroradd_categoriesLabel.configure(text="Fill all fields!")
        return


def confirm_episode(episodeNameEntry, strPodcast,episodeUrlEntry, erroradd_episodeLabel):
    """Guarda os dados do episódio a adicionar"""

    if episodeNameEntry.get() and episodeUrlEntry.get():
        #Variável com a estrutura de dados
        episodeData = f"{episodeNameEntry.get()};{strPodcast.get()};0;{episodeUrlEntry.get()}\n"

        #Abre o caminho da música no formato "append" para adicionar a linha sem apagar o conteúdo existente
        with open(podcastEpisodesPath, "a", encoding="utf-8") as file:
            file.writelines(episodeData) # escreve os dados com a estrutura anteriormente definida
            file.close
        
        #Apagar conteúdo
        episodeNameEntry.delete(0,"end")
        episodeUrlEntry.delete(0,"end")
        erroradd_episodeLabel.configure(text="Category added with success!")

        return

    else:
        erroradd_episodeLabel.configure(text="Fill all fields!")
        return

def refresh_tree(tree, type):
    if type=="podcast":
        path=podcastPath
    elif type=="music":
        path=musicPath
    elif type=="users":
        path=accountsPath
    elif type=="categories":
        path=categoriesFile
    elif type=="episodes":
        path=podcastEpisodesPath
    elif type=="admin":
        path=adminListfile

    # Delete all rows in the Treeview
    for row in tree.get_children():  # Iterate over all row IDs in the Treeview
        tree.delete(row)  # Delete each row

    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    if type=="music":
        for line in lines:
            fields = line.strip().split(";")
            tree.insert("","end", values=(fields[0], fields[1],fields[2], fields[3]))
    elif type=="podcast":
        for line in lines:
            fields = line.strip().split(";")
            tree.insert("","end", values=(fields[0], fields[1]))
    elif type=="users":
        for line in lines:
            fields = line.strip().split(";")
            tree.insert("","end", values=(fields[2],fields[0], fields[1])) #Nome, username, password
    elif type=="categories" or type=="admin":
        for line in lines:
            fields = line.strip()
            tree.insert("","end", values=(fields))
    elif type=="episodes":
        for line in lines:
            fields = line.strip().split(";")
            tree.insert("","end", values=(fields[0], fields[1] ,fields[2] ,fields[3]))

def confirm_change(usernameEntry, nameEntry,usernameCurrent,NameCurrent):
     # Lê o conteúdo do arquivo
    with open(accountsPath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Cria uma nova lista sem a música que será removida
    updated_lines = []
    for line in lines:
        fields = line.strip().split(";")

        # Se o nome e autor não coincidem, mantém a linha
        if not (fields[0] == usernameCurrent and fields[2] == NameCurrent):
            updated_lines.append(line)
        if (fields[0] == usernameCurrent and fields[2] == NameCurrent):
            if nameEntry.get()=="" or nameEntry.get==" ":
                newName=NameCurrent
            else:
                newName=nameEntry.get()
            if usernameEntry.get()=="" or usernameEntry.get==" ":
                newuserName=usernameCurrent
            else:
                newuserName=usernameEntry.get()
            updated_lines.append(f"{newuserName};{fields[1]};{newName}\n")

    # Escreve as linhas atualizadas de volta no arquivo
    with open(accountsPath, "w", encoding="utf-8") as file:
        file.writelines(updated_lines)

     # Lê o conteúdo do arquivo
    with open(adminListfile, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Cria uma nova lista sem a música que será removida
    updated_lines = []
    for line in lines:
        # Se o nome
        if not fields[0] == usernameCurrent:
            updated_lines.append(line)
        if fields[0] == usernameCurrent:
            updated_lines.append(f"{newuserName}\n")

    # Escreve as linhas atualizadas de volta no arquivo
    with open(adminListfile, "w", encoding="utf-8") as file:
        file.writelines(updated_lines)

    return newuserName, newName

def save_notifications(notificationsText):

    textSave = notificationsText.get("0.0", "end")
    
    if textSave == "":
        return

    newText = textSave.replace("\n", " ")

    with open(customNotificationFile, "a", encoding="utf-8") as file:
        file.write(newText)

def delete_notifications():
    with open(customNotificationFile, "w", encoding="utf-8") as file:
        pass

def delete_folder(username):
    shutil.rmtree(usersPath+username)

    print(f"Folder {usersPath+username} deleted.")

##########################################[CAMINHOS]############################################################

imagePath = f".{pathFormat}images{pathFormat}icons{pathFormat}" # Caminho para o diretório onde são armazenadas as imagens
profileimagePath = f".{pathFormat}images{pathFormat}profile_images{pathFormat}" # Caminho para o diretório onde são armazenadas as imagens de perfil
accountsPath = f".{pathFormat}db{pathFormat}user_accounts.csv" # Caminho para o ficheiro onde são armazenadas as contas
musicPath = f".{pathFormat}db{pathFormat}music_list.csv" # Caminho para o ficheiro onde são armazenadas as músicas
podcastPath = f".{pathFormat}db{pathFormat}podcast_list.csv" # Caminho para o ficheiro onde são armazenadas os podcasts
adminListfile = f".{pathFormat}db{pathFormat}admin_list.csv" # Caminho para o ficheiro onde são armazenadas as contas admin
categoriesFile = f".{pathFormat}db{pathFormat}categories.csv" # Caminho para o ficheiro onde são armazenadas as categorias
coverArtPath = f".{pathFormat}images{pathFormat}cover_art{pathFormat}" # Caminho para o diretório onde são armazenadas as imagens das músicas
musicAudioPath = f".{pathFormat}audios{pathFormat}music{pathFormat}" # Caminho para o diretório onde são armazenadas as músicas
usersPath = f".{pathFormat}db{pathFormat}users{pathFormat}" # Caminho para o diretório onde são armazenadas os users na db
podcastEpisodesPath = f".{pathFormat}db{pathFormat}podcast_episodes.csv"
customNotificationFile = f".{pathFormat}db{pathFormat}custom_notifications.txt"
autoNotificationFile = f".{pathFormat}db{pathFormat}auto_notifications.txt"
#################################################################################################################