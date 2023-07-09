import os
import pickle
import shutil

print("-------------------------")
print("VFX Shot Filetree Utility")
print("-------------------------")
print("Version 1.0")
print("created 21 February 2023")
print("modified 8 July 2023")
print("by Preston Mohr")
print("\n")

def save_data(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    else:
        return None

def copy_new_shots():
    global processed_subfolders
    if processed_subfolders is None:
        processed_subfolders = []

    for folder_name in os.listdir(incomingDirectory):
        folder_path = os.path.join(incomingDirectory, folder_name)
        if not os.path.isdir(folder_path) or folder_name in processed_subfolders:
            continue
        for file_name in os.listdir(folder_path):
            if not file_name.endswith('.mov'):
                continue
            shot_name_parts = file_name[:-4].split('_')
            if len(shot_name_parts) != 3:
                continue
            seq, shot, ver = shot_name_parts
            source_path = os.path.join(folder_path, file_name)
            dest_dir = os.path.join(fileTreePath, seq, shot)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            dest_path = os.path.join(dest_dir, file_name)
            shutil.copy(source_path, dest_path)
            print(f"Copied {source_path} to {dest_path}")
        processed_subfolders.append(folder_name)
    save_data(processed_subfolders, 'pkl/processed_subfolders.pkl')
    print("Finished copying new shots.")

def set_shot_name_format():
    global shotNameFormat
    print("Current shot name format: " + shotNameFormat)
    print("")
    choice = input("Change current shot name format (y/n)? ")
    if choice == 'y' or choice == 'Y':
        valid_formats = {'A': "<SHOW>_<SCN>_<SHOT>",
                         'a': "<SHOW>_<SCN>_<SHOT>",
                         'B': "<SCN>_<SHOW>_<SHOT>",
                         'b': "<SCN>_<SHOW>_<SHOT>",
                         'C': "<SHW>_<SCN>_<SHOT>",
                         'c': "<SHW>_<SCN>_<SHOT>",
                         'D': "<SCN>_<SHW>_<SHOT>",
                         'd': "<SCN>_<SHW>_<SHOT>",
                         'E': "<SEQ>_<SCN>_<SHOT>",
                         'e': "<SEQ>_<SCN>_<SHOT>",
                         'F': "<SCN>_<SEQ>_<SHOT>",
                         'f': "<SCN>_<SEQ>_<SHOT>"}
        print("Select a shot name format:")
        print("\tA. <SHOW>_<SCN>_<SHOT> | i.e. FILM_012_0010")
        print("\tB. <SCN>_<SHOW>_<SHOT> | i.e. 012_FILM_0010")
        print("\tC. <SHW>_<SCN>_<SHOT>  | i.e. FLM_012_0010")
        print("\tD. <SCN>_<SHW>_<SHOT>  | i.e. 012_FLM_0010")
        print("\tE. <SEQ>_<SCN>_<SHOT>  | i.e. ABC_012_0010")
        print("\tF. <SCN>_<SEQ>_<SHOT>  | i.e. 012_ABC_0010")
        print("\tG. Custom...")
        print("\tH. Legend...")
        print("\tI. Back...")
        print("")
        choice = input("Enter your choice (A/B/C/D/E/F/G/H/I): ")
        if choice == 'G' or choice == 'g':
            customChoice = input("Enter your custom shot name format: ")
            tempShotNameFormat = shotNameFormat
            try:
                shotNameFormat = customChoice
                #reset the file tree structure format too
                f = parse_filename_structure()
                fileTreeStructureFormat = (f[0] + "/" + f[1] + "/" + f[2])
                save_data(shotNameFormat, 'pkl/shot_name_format.pkl')
                print("Shot name format set to:", shotNameFormat)
                save_data(fileTreeStructureFormat, 'pkl/file_tree_structure_format.pkl')
                print(f"File tree structure format RESET to default structure:", fileTreeStructureFormat)
            except:
                shotNameFormat = tempShotNameFormat
                print("Invalid custom shot name format.")
                save_data(shotNameFormat, 'pkl/shot_name_format.pkl')
        elif choice == 'H' or choice == 'h':
            print("")
            print("*****************************")
            print("VFX Shot Naming Format Legend")
            print("*****************************")
            print("SHOW: 4 letter show abbreviation")
            print("SHW: 3 letter show abbreviation")
            print("SCN: 3 digit scene abbreviation")
            print("SHOT: 4 digit shot number")
            print("SEQ: 3 character sequence abbreviation")
            print("")
            set_shot_name_format()
        elif choice == 'I' or choice == 'i':
            print("Returning to main menu")
        elif choice in list(valid_formats.keys()):
            shotNameFormat = valid_formats.get(choice, "")
            save_data(shotNameFormat, 'pkl/shot_name_format.pkl')
            print("Shot name format set to:", shotNameFormat)

            #reset the file tree structure format too
            f = parse_filename_structure()
            fileTreeStructureFormat = (f[0] + "/" + f[1] + "/" + f[2])
            save_data(fileTreeStructureFormat, 'pkl/file_tree_structure_format.pkl')
            print(f"File tree structure format RESET to default structure:", fileTreeStructureFormat)
        else:
            print("Invalid choice")
    elif choice == 'n' or choice == 'N':
        print("")
        print("Returning to main menu")
    else:
        print("")
        print("Invalid choice")

def parse_filename_structure():
    global shotNameFormat
    parts = shotNameFormat.split('>_<')
    fst = parts[0].replace('<', '')
    mid = parts[1]
    lst = parts[2].replace('>', '')
    return fst,mid,lst

def get_example(t):
    if t=="SHOW" or t=="show":
        return "FILM"
    elif t=="SHW" or t=="shw":
        return "FLM"
    elif t=="SEQ" or t=="seq":
        return "ABC"
    elif t=="SCN" or t=="scn":
        return "012"
    elif t=="SHOT" or t=="shot":
        return "0010"
    else:
        return "#" * len(t)

def set_file_tree_structure_format():
    global shotNameFormat, fileTreeStructureFormat
    print("Current file tree structure format: " + fileTreeStructureFormat)
    print("")
    choice = input("Change current file tree structure format (y/n)? ")
    if choice == 'y' or choice == 'Y':
        print("Select a file tree structure format:")
        f = parse_filename_structure()

        valid_formats = {'A': (f[0] + "/" + f[1] + "/" + f[2]),
                         'a': (f[0] + "/" + f[1] + "/" + f[2]),
                         'B': (f[0] + "/" + f[1] + "_" + f[2]),
                         'b': (f[0] + "/" + f[1] + "_" + f[2]),
                         'C': (f[0] + "_" + f[1] + "/" + f[2]),
                         'c': (f[0] + "_" + f[1] + "/" + f[2]),
                         'D': (f[0] + "_" + f[1] + "_" + f[2]),
                         'd': (f[0] + "_" + f[1] + "_" + f[2])}
        print("Select a shot name format:")
        print(f"\tA. {f[0]}/{f[1]}/{f[2]} | i.e. {get_example(f[0])}/{get_example(f[1])}/{get_example(f[2])}")
        print(f"\tB. {f[0]}/{f[1]}_{f[2]} | i.e. {get_example(f[0])}/{get_example(f[1])}_{get_example(f[2])}")
        print(f"\tC. {f[0]}_{f[1]}/{f[2]} | i.e. {get_example(f[0])}_{get_example(f[1])}/{get_example(f[2])}")
        print(f"\tD. {f[0]}_{f[1]}_{f[2]} | i.e. {get_example(f[0])}_{get_example(f[1])}_{get_example(f[2])}")
        print("\tE. Custom...")
        print("\tG. Back...")
        print("")
        choice = input("Enter your choice (A/B/C/D/E/F): ")
        if choice == 'E' or choice == 'e':
            customChoice = input("Enter your custom file tree structure format: ")
            fileTreeStructureFormat = customChoice
            save_data(fileTreeStructureFormat, 'pkl/file_tree_structure_format.pkl')
            print(f"File tree structure format set to: {fileTreeStructureFormat}")
        elif choice == 'G' or choice == 'g':
            print("Returning to main menu")
        elif choice in list(valid_formats.keys()):
            fileTreeStructureFormat = valid_formats.get(choice, "")
            save_data(fileTreeStructureFormat, 'pkl/file_tree_structure_format.pkl')
            print(f"File tree structure format set to: {fileTreeStructureFormat}")
        else:
            print("Invalid choice")
    elif choice == 'n' or choice == 'N':
        print("")
        print("Returning to main menu")
    else:
        print("")
        print("Invalid choice")

def set_file_tree_directory():
    global fileTreePath
    print("Current file tree directory path: " + fileTreePath)
    print("")
    choice = input("Change current file directory path (y/n)? ")
    if choice == 'y' or choice == 'Y':
        path = input("Enter file tree directory path: ")
        if os.path.isdir(path):
            fileTreePath = path
            save_data(fileTreePath, 'pkl/file_tree_path.pkl')
            print("File tree directory set to:", fileTreePath)
        else:
            print("")
            print("Invalid directory path.")
    elif choice == 'n' or choice == 'N':
        print("")
        print("Returning to main menu")
    else:
        print("")
        print("Invalid choice")

def set_incoming_submissions_directory():
    global incomingDirectory
    print("Current incoming submissions directory path: " + incomingDirectory)
    print("")
    choice = input("Change current incoming submissions directory path (y/n)? ")
    if choice == 'y' or choice == 'Y':
        path = input("Enter incoming submissions directory path: ")
        if os.path.isdir(path):
            incomingDirectory = path
            save_data(incomingDirectory, 'pkl/incoming_directory.pkl')
            print("Incoming submissions directory set to:", incomingDirectory)
        else:
            print("")
            print("Invalid directory path.")
    elif choice == 'n' or choice == 'N':
        print("")
        print("Returning to main menu")
    else:
        print("")
        print("Invalid choice")

def reset_defaults():
    global incomingDirectory, fileTreePath, shotNameFormat, fileTreeStructureFormat
    print("Current incoming submissions directory path: " + incomingDirectory)
    print("Current file tree directory path: " + fileTreePath)
    print("Current shot name format: " + shotNameFormat)
    print("Current file tree structure format: " + fileTreeStructureFormat)
    print("")
    choice = input("Reset ALL the above to their default values (y/n)? ")
    if choice == 'y' or choice == 'Y':
        confirm = input("Type RESET to confirm reset of all values: ")
        if confirm == 'RESET' or confirm == 'reset':
            current_location = os.path.dirname(os.path.abspath(__file__))

            if not os.path.exists(os.path.join(current_location, "incoming")):
                os.makedirs(os.path.join(current_location, "incoming"))
            incomingDirectory = os.path.join(current_location, "incoming")
            save_data(incomingDirectory, 'pkl/incoming_directory.pkl')
            print("Incoming submissions directory path set to:", incomingDirectory)

            if not os.path.exists(os.path.join(current_location, "filetree")):
                os.makedirs(os.path.join(current_location, "filetree"))
            fileTreePath = os.path.join(current_location, "filetree")
            save_data(fileTreePath, 'pkl/file_tree_path.pkl')
            print("File tree directory path set to:", fileTreePath)

            shotNameFormat = "<SHOW>_<SCN>_<SHOT>"
            save_data(shotNameFormat, 'pkl/shot_name_format.pkl')
            print("Shot name format set to:", shotNameFormat)

            fileTreeStructureFormat = "SHOW/SCN/SHOT"
            save_data(fileTreeStructureFormat, 'pkl/file_tree_structure_format.pkl')
            print("File tree structure format set to:", fileTreeStructureFormat)
            print("")
            print("All settings set to their default values.")
        else:
            print("Reset cancelled")
    elif choice == 'n' or choice == 'N':
        print("")
        print("Returning to main menu")
    else:
        print("")
        print("Invalid choice")
    

def print_menu():
    print("-------------------------")
    print("VFX Shot Filetree Menu")
    print("-------------------------")
    print("1. Copy new submissions to file tree (AUTO)")
    print("2. Select submission to copy to file tree (MANUAL)")
    print("4. Choose shot naming format")
    print("5. Choose file tree directory structure")
    print("6. Choose incoming submissions directory path")
    print("7. Choose file tree directory path")
    print("8. Reset Defaults")
    print("9. Quit")
    print("")

# Load saved data if available
fileTreePath = load_data('pkl/file_tree_path.pkl')
incomingDirectory = load_data('pkl/incoming_directory.pkl')
shotNameFormat = load_data('pkl/shot_name_format.pkl')
fileTreeStructureFormat = load_data('pkl/file_tree_structure_format.pkl')
processed_subfolders = load_data('pkl/processed_subfolders.pkl')

while True:
    print_menu()
    choice = input("Select an option: ")
    print("")
    if choice == '1':
        copy_new_shots()
    elif choice == '4':
        set_shot_name_format()
    elif choice == '5':
        set_file_tree_structure_format()
    elif choice == '6':
        set_incoming_submissions_directory()
    elif choice == '7':
        set_file_tree_directory()
    elif choice == '8':
        reset_defaults()
    elif choice == '9':
        break
    else:
        print("Invalid choice")
    print("")
