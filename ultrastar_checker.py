import os
from threading import *


def run_checker(FOLDER_PATH):
    missing = []
    for filename in os.listdir(FOLDER_PATH):
        missing = get_artist_from_file(FOLDER_PATH, filename, missing)

    move_files(missing, FOLDER_PATH)
          

def get_artist_from_file(FOLDER_PATH, filename, missing):
    link = 1
    link_picture = 1
    if filename.endswith('.txt'):
        file_path = os.path.join(FOLDER_PATH, filename)
        
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        for line in lines:
            if line.startswith("#VIDEO"):
                x1 = line.find("co=")
                if x1 >= 1 and ".jpg" in line:
                    x2 = line.find(".jpg")
                    link_picture = line[x1+3:x2+4]
                    if not link_picture.startswith("https://"):
                        link_picture = "https://" + link_picture
                else:
                    link_picture = 1

                x1 = 9
                x2 = line.find("co=") - 1
                if not x2 >= 1:
                    x2 = len(line)
                    link = "https://www.youtube.com/watch?v=" + line[x1:x2]
                    if not x2 > 8 or not "=" in line:
                        link = 1

                else:
                    link = "https://www.youtube.com/watch?v=" + line[x1:x2]
                                  
        if link_picture == 1:
            print("WARNING: " + filename + ": has no link to a picture!")

        else:
            print(filename + ": foud link to picture: " + link_picture)

        if link == 1:
            print("ERROR: " + filename + ": has no YouTube link!")
            missing.append(filename)

        else:
            print(filename + ": found YouTube link: " + link)

    print(missing)
    return missing


def move_files(missing, FOLDER_PATH):
    file_path = os.path.join(FOLDER_PATH, "NoYoutubeLink")
    isExist = os.path.exists(file_path)
    if not isExist:
        os.makedirs(file_path)
        print("Created directory: " + file_path)
    
    for entry in missing:
        os.replace(FOLDER_PATH + "/" + entry, FOLDER_PATH + "/NoYoutubeLink/" + entry)