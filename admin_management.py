import os

from file_management import *

def edit_music(musicNameEntry, musicAuthorEntry, strCategories, tree):
    """Edita a música selecionada no Treeview e atualiza o ficheiro."""

    # Obtém o ID da linha selecionada no Treeview
    rowId = tree.focus()

    if not rowId:
        print("Nenhuma linha selecionada!")
        return

    # Obtém os valores da linha selecionada
    values = tree.item(rowId, "values")
    valuesList = list(values)

    # Obtém os novos valores dos campos de entrada
    newMusicName = musicNameEntry.get()
    newArtistName = musicAuthorEntry.get()
    newCategory = strCategories.get()

    # Abre o ficheiro e lê todas as linhas
    with open(musicPath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Imprime os valores da linha selecionada para depuração
    print("Editar linha com valores:", valuesList)
    print("Novos valores:", newMusicName, newArtistName, newCategory)

    # Atualiza a linha correspondente aos valores da linha selecionada
    updated_lines = []
    for line in lines:
        fields = line.strip().split(";")  # Assumindo que o delimitador é o ponto e vírgula
        # Verifica se esta linha corresponde ao nome e autor da linha selecionada
        if fields[0] == values[0] and fields[1] == values[1]:
            # Atualiza os campos com os novos valores
            fields[0] = newMusicName
            fields[1] = newArtistName
            fields[2] = newCategory  # Atualiza o campo de categoria
            # Reconstrói a linha com os campos atualizados, mantendo visualizações, imagem e ficheiro de áudio inalterados
            updated_line = ";".join(fields) + "\n"
            updated_lines.append(updated_line)
        else:
            updated_lines.append(line)

    with open(musicPath, "w", encoding="utf-8") as file:
        file.writelines(updated_lines)


def delete_category(tree):
    # Obtém o ID da linha selecionada no Treeview
    rowId = tree.focus()

    if not rowId:
        print("Nenhuma linha selecionada!")
        return

    # Obtém os valores da linha selecionada
    values = tree.item(rowId, "values")
    valuesList = list(values)

    # Abre o ficheiro e lê todas as linhas
    with open(categoriesFile, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Imprime os valores da linha selecionada para depuração
    print("Eliminar linha com valores:", valuesList)

    # Filtra a linha correspondente aos valores da linha selecionada
    updated_lines = []
    for line in lines:
        fields = line.strip()  # Assumindo que o delimitador é o ponto e vírgula
        if fields == values[0]:
            continue  # Ignora esta linha, pois corresponde à linha selecionada
        updated_lines.append(line)

    # Verifica se a linha foi encontrada e removida
    if len(updated_lines) == len(lines):
        print("Nenhuma linha correspondente encontrada para eliminar.")
    else:
        print("Linha eliminada com sucesso.")

        # Escreve as linhas atualizadas de volta no ficheiro
        with open(categoriesFile, "w", encoding="utf-8") as file:
            file.writelines(updated_lines)

        # Opcionalmente, remove a linha do Treeview
        tree.delete(rowId)


def delete_type(tree, type):

    if type == "podcast":
        path = podcastPath
    elif type == "music":
        path = musicPath
    elif type == "users":
        path = accountsPath
    elif type == "episodes":
        path = podcastEpisodesPath
    elif type == "admin":
        path = adminListfile

    # Obtém o ID da linha selecionada no Treeview
    rowId = tree.focus()

    if not rowId:
        print("Nenhuma linha selecionada!")
        return

    # Obtém os valores da linha selecionada
    values = tree.item(rowId, "values")
    valuesList = list(values)

    # Abre o ficheiro e lê todas as linhas
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Imprime os valores da linha selecionada para depuração
    print("Eliminar linha com valores:", valuesList)

    # Filtra a linha correspondente aos valores da linha selecionada
    updated_lines = []
    for line in lines:
        fields = line.strip().split(";")  # Assumindo que o delimitador é o ponto e vírgula
        if type == "users":
            if fields[0] == values[1] and fields[1] == values[2]:
                username = fields[1]
                continue  # Ignora esta linha, pois corresponde à linha selecionada
        elif type == "episodes" or type == "podcast":
            if fields[0] == values[0] and fields[1] == values[1]:
                continue  # Ignora esta linha, pois corresponde à linha selecionada
        elif type == "admin":
            if line.strip() == values[0]:
                continue
        else:
            if fields[0] == values[0] and fields[1] == values[1]:
                coverArt = fields[4]
                audio = fields[5]
                continue  # Ignora esta linha, pois corresponde à linha selecionada
        updated_lines.append(line)

    # Verifica se a linha foi encontrada e removida
    if len(updated_lines) == len(lines):
        print("Nenhuma linha correspondente encontrada para eliminar.")
    else:
        print("Linha eliminada com sucesso.")

        # Escreve as linhas atualizadas de volta no ficheiro
        with open(path, "w", encoding="utf-8") as file:
            file.writelines(updated_lines)

        # Opcionalmente, remove a linha do Treeview
        tree.delete(rowId)

    if type == "users":
        delete_folder(username)
    if type == "admin":
        print(f"{values[0]} já não é administrador.")
    if type == "music":
        os.remove(coverArtPath + coverArt)
        print(f"Eliminado {coverArtPath + coverArt} com sucesso!")
        os.remove(musicAudioPath + audio)
        print(f"Eliminado {musicAudioPath + audio} com sucesso!")


def confirm_admin_refresh(adminEntry, erroradd_adminLabel, tree):
    confirm_admin(adminEntry, erroradd_adminLabel)
    refresh_tree(tree, "admin")


def confirm_admin(adminEntry, erroradd_adminLabel):
    userCheck = []

    with open(adminListfile, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        userCheck.append(line.strip())

    if adminEntry.get() in userCheck:
        erroradd_adminLabel.configure(text="Utilizador já é administrador")
        return

    with open(adminListfile, "a", encoding="utf-8") as file:
        file.write(adminEntry.get() + "\n")

    adminEntry.delete(0, "end")

    erroradd_adminLabel.configure(text=f"{adminEntry.get()} agora é administrador")


def get_notification(type):
    if type == "custom":
        with open(customNotificationFile, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines:
            returnString = line.strip()

        return returnString
    else:
        notificationList = []

        with open(autoNotificationFile, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines:
            fields = line.strip().split(";")
            if fields[0] == type:
                notificationList.append(fields[1])
                notificationList.append(fields[2])

        return notificationList


def get_type_notification(usernameFinal):
    acceptedNotifications = []
    with open(f"{usersPath}{usernameFinal}{pathFormat}notification.csv", "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        acceptedNotifications.append(line.strip())

    return acceptedNotifications
