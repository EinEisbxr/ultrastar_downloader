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
                content = line[len("#VIDEO:"):].strip()
                co_index = content.find("co=")

                if co_index != -1:
                    video_part = content[:co_index].strip()
                    co_part = content[co_index + 3:].strip()
                    comma_index = co_part.find(',')

                    if comma_index != -1:
                        link_picture = co_part[:comma_index].strip()
                    else:
                        link_picture = co_part

                    if not link_picture.startswith("https://"):
                        link_picture = "https://" + link_picture
                else:
                    video_part = content
                    link_picture = 1

                comma_index = video_part.find(',')
                if comma_index != -1:
                    video_id = video_part[:comma_index].strip()
                else:
                    video_id = video_part

                if video_id:
                    link = "https://www.youtube.com/watch?v=" + video_id
                else:
                    link = 1

                if link_picture == 1:
                    print("WARNING: " + filename + ": has no link to a picture!")
                else:
                    print(filename + ": found link to picture: " + link_picture)

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