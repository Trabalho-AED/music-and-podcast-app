from file_management import *
import os

def edit_music(musicNameEntry, musicAuthorEntry, strCategories,tree):
    """Edit the selected music entry in the Treeview and update the file."""

    # Get the selected row ID from the Treeview
    rowId = tree.focus()

    if not rowId:
        print("No row selected!")
        return
    
    # Get the values from the selected row
    values = tree.item(rowId, "values")
    valuesList = list(values)

    # Get the new values from the entry fields
    newMusicName = musicNameEntry.get()
    newArtistName = musicAuthorEntry.get()
    newCategory = strCategories.get()

    # Open the file and read all lines
    with open(musicPath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Print the selected row values for debugging
    print("Editing row with values:", valuesList)
    print("New values:", newMusicName, newArtistName, newCategory)

    # Update the line that matches the selected row's values
    updated_lines = []
    for line in lines:
        fields = line.strip().split(";")  # Assuming semicolon is the delimiter in the file
        # Check if this line matches the selected row's name and artist
        if fields[0] == values[0] and fields[1] == values[1]:
            # Update the fields with new values
            fields[0] = newMusicName
            fields[1] = newArtistName
            fields[2] = newCategory  # Update the category field
            # Rebuild the line with the updated fields, keeping views, image, and audio filename the same
            updated_line = ";".join(fields) + "\n"
            updated_lines.append(updated_line)
        else:
            updated_lines.append(line)

    with open(musicPath, "w", encoding="utf-8") as file:
        file.writelines(updated_lines)


def delete_category(tree):
    # Get the selected row ID from the Treeview
    rowId = tree.focus()

    if not rowId:
        print("No row selected!")
        return
    
    # Get the values from the selected row
    values = tree.item(rowId, "values")
    valuesList = list(values)

    # Open the file and read all lines
    with open(categoriesFile, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Print the selected row values for debugging
    print("Deleting row with values:", valuesList)

    # Filter out the line that matches the selected row's values
    updated_lines = []
    for line in lines:
        fields = line.strip()  # Assuming semicolon is the delimiter in the file
        if fields == values[0]:
            continue  # Skip this line as it matches the selected row
        updated_lines.append(line)

    # Check if the line was found and removed
    if len(updated_lines) == len(lines):
        print("No matching line found to delete.")
    else:
        print("Line deleted successfully.")

        # Write the updated lines back to the file
        with open(categoriesFile, "w", encoding="utf-8") as file:
            file.writelines(updated_lines)

        # Optionally, remove the row from the Treeview
        tree.delete(rowId)


def delete_type(tree,type):

    if type=="podcast":
        path = podcastPath
    elif type=="music":
        path = musicPath
    elif type=="users":
        path = accountsPath

    # Get the selected row ID from the Treeview
    rowId = tree.focus()

    if not rowId:
        print("No row selected!")
        return
    
    # Get the values from the selected row
    values = tree.item(rowId, "values")
    valuesList = list(values)

    # Open the file and read all lines
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Print the selected row values for debugging
    print("Deleting row with values:", valuesList)

    # Filter out the line that matches the selected row's values
    updated_lines = []
    for line in lines:
        fields = line.strip().split(";")  # Assuming semicolon is the delimiter in the file
        if type=="users":
            if fields[0] == values[1] and fields[1] == values[2]:
                username=fields[1]
                continue  # Skip this line as it matches the selected row
        else:
            if fields[0] == values[0] and fields[1] == values[1]:
                coverArt=fields[4]
                audio=fields[5]
                continue  # Skip this line as it matches the selected row
        updated_lines.append(line)

    # Check if the line was found and removed
    if len(updated_lines) == len(lines):
        print("No matching line found to delete.")
    else:
        print("Line deleted successfully.")

        # Write the updated lines back to the file
        with open(path, "w", encoding="utf-8") as file:
            file.writelines(updated_lines)

        # Optionally, remove the row from the Treeview
        tree.delete(rowId)
    
    if type=="users":
        delete_folder(username)
    if type=="music":
        os.remove(coverArtPath+coverArt)
        print(f"Deleted {coverArtPath+coverArt} successfully!")
        os.remove(musicAudioPath+audio)
        print(f"Deleted {musicAudioPath+audio} successfully!")