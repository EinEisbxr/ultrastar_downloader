import os
from pytube import *
from moviepy.editor import *
import unicodedata
import requests
from threading import *
from time import *
import shutil


def download_youtube_video(link, FOLDER_PATH, file_path, link_picture):
    print("downloading video!")
    print(link)
    yt = YouTube(link)
    downloaded_file_path = yt.streams.get_highest_resolution().download(FOLDER_PATH)

    title = replace_non_ascii(yt.title)
    print("download completed: " + title)

    # Rename the downloaded file
    new_file_path = os.path.join(FOLDER_PATH, title + '.mp4')
    print("Original file path: ", downloaded_file_path)
    if os.path.exists(downloaded_file_path):
        print("Original file path: ", downloaded_file_path)  # Print the original file path
        shutil.move(downloaded_file_path, new_file_path)

    if link_picture != 1:
        try:
            response = requests.get(link_picture)

            if response.status_code == 200:
                with open(FOLDER_PATH + "/" + title + ".jpg", 'wb') as file:
                    file.write(response.content)
                print("Image downloaded successfully as", FOLDER_PATH + "/" + title + ".jpg")
            else:
                print("Failed to download the image")

        except:
            print("Website not reachable")

    rename_file_and_add_line(title, file_path, FOLDER_PATH)


def delete_lines_with_prefix(file_path, prefix_list):
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()

        for line in lines:
            if not any(line.startswith(prefix) for prefix in prefix_list):
                file.write(line)

    return


def get_title_artist_from_file(FOLDER_PATH, prefix_list):
    for filename in os.listdir(FOLDER_PATH):
        if filename.endswith('.txt'):
            file_path = os.path.join(FOLDER_PATH, filename)
            
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            for line in lines:
                if line.startswith("#VIDEO"):
                    x1 = line.find("co=")
                    if x1 >= 1:
                        x2 = line.find(".jpg")
                        link_picture = line[x1+3:x2+4]
                        print(link_picture)
                        if not link_picture.startswith("https://"):
                            link_picture = "https://" + link_picture
                            print(link_picture)
                    else:
                        link_picture = 1

                    x1 = 9
                    x2 = line.find("co=") - 1
                    if not x2 >= 1:
                        x2 = len(line)

                    link = "https://www.youtube.com/watch?v=" + line[x1:x2]
                    
            delete_lines_with_prefix(file_path, prefix_list)

            while active_count() > int(number_of_threads):
                sleep(0.01)
            x = Thread(target=download_youtube_video, args=(link, FOLDER_PATH, file_path, link_picture))
            x.start()


def rename_file_and_add_line(title, file_path, FOLDER_PATH):
    print("Changing file")
    title = replace_non_ascii(title)
    with open(file_path, 'r') as old_file:
        old_content = old_file.read()
    
        #if old_content[0].startswith("#VIDEO:"):
        #    return
    
    # Open the file in write mode
    with open(file_path, 'w') as new_file:
        # Write the new line followed by the existing content
        new_file.write("#VIDEO:" + title + ".mp4" + '\n' + "#MP3:" + title + ".mp4" + '\n' + "#COVER:" + title + ".jpg" + '\n' + old_content)


def replace_non_ascii(text): 
    text = text.replace("%", "").replace("&", "").replace("{", "").replace("\\", "").replace(":", "").replace("<", "").replace(">", "").replace("*", "").replace("?", "").replace("/", "").replace("$", "").replace("'", "").replace("(", "").replace(")", "").replace("!", "").replace("|", "").replace(" ", "_").replace('"', "").replace("=", "").replace("+", "").replace(",", "").replace(";", "").replace("[", "").replace("]", "").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss").replace("Ä", "Ae").replace("Ö", "Oe").replace("Ü", "Ue").replace("🇳🇱", "").replace("🇨🇭", "")
    return text


def run_ultrastar_downloader(FOLDER_PATH, prefix_list, number_of_threads2):
    global number_of_threads
    number_of_threads = number_of_threads2
    get_title_artist_from_file(FOLDER_PATH, prefix_list)
