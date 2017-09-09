import os;

def GetFilePaths(directory):    
    file_paths = []  # List which will store all of the full filepaths.
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename) # Join the two strings in order to form the full filepath.
            file_paths.append(filepath)  # Add it to the list.
    return file_paths  # Self-explanatory.
