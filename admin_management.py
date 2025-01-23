from file_management import *
import os

def delete_music(tree):
    # Get the selected row ID from the Treeview
    rowId = tree.focus()

    if not rowId:
        print("No row selected!")
        return
    
    # Get the values from the selected row
    values = tree.item(rowId, "values")
    valuesList = list(values)

    # Open the file and read all lines
    with open(musicPath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Print the selected row values for debugging
    print("Deleting row with values:", valuesList)

    # Filter out the line that matches the selected row's values
    updated_lines = []
    for line in lines:
        fields = line.strip().split(";")  # Assuming semicolon is the delimiter in the file
        if fields[0] == values[0] and fields[1] == values[1]:
            continue  # Skip this line as it matches the selected row
        updated_lines.append(line)

    # Check if the line was found and removed
    if len(updated_lines) == len(lines):
        print("No matching line found to delete.")
    else:
        print("Line deleted successfully.")

        # Write the updated lines back to the file
        with open(musicPath, "w", encoding="utf-8") as file:
            file.writelines(updated_lines)

        # Optionally, remove the row from the Treeview
        tree.delete(rowId)

def edit_music(tree):
    # Get the selected row ID from the Treeview
    rowId = tree.focus()

    if not rowId:
        print("No row selected!")
        return
    
    # Get the values from the selected row
    values = tree.item(rowId, "values")
    valuesList = list(values)

    # Open the file and read all lines
    with open(musicPath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Print the selected row values for debugging
    print("Deleting row with values:", valuesList)

    # Filter out the line that matches the selected row's values
    updated_lines = []
    for line in lines:
        fields = line.strip().split(";")  # Assuming semicolon is the delimiter in the file
        if fields[0] == values[0] and fields[1] == values[1]:
            continue  # Skip this line as it matches the selected row
        updated_lines.append(line)

    # Check if the line was found and removed
    if len(updated_lines) == len(lines):
        print("No matching line found to delete.")
    else:
        print("Line deleted successfully.")

        # Write the updated lines back to the file
        with open(musicPath, "w", encoding="utf-8") as file:
            file.writelines(updated_lines)

        # Optionally, remove the row from the Treeview
        tree.delete(rowId)