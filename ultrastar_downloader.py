import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from pytube import *
from moviepy.editor import *
import unicodedata
import requests
from threading import *
from time import *


def download_youtube_video(link, FOLDER_PATH, file_path, link_picture):
    print("downloading video!")
    #download from YT
    print(link)
    yt = YouTube(link)
    yt.streams.get_highest_resolution().download(FOLDER_PATH)


    title = yt.title
    print("download completed: " + title)

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


def get_title_artist_from_file(FOLDER_PATH, YOUTUBE, prefix_list):
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

            while active_count() >= 16:
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
    # Normalize the text into NFKD form
    normalized = unicodedata.normalize('NFKD', text)

    # Replace any non-ASCII characters with underscores
    ascii_text = ''
    for c in normalized:
        if ord(c) < 128:
            ascii_text += c
        else:
            ascii_text += ''
        
    ascii_text = ascii_text.replace(".", "")
    return ascii_text


#configure Threads
t1 = Thread()



# Set your API key
API_KEY = 'AIzaSyBzx67b_K2Jzw85r18SPnddYoIAfSvKP_Q'

#Select Folder
FOLDER_PATH = "C:\Texte"

prefix_list = ['#VIDEO', '#MP3', "#COVER"]

# Build the YouTube API client
YOUTUBE = build('youtube', 'v3', developerKey=API_KEY)

#get search query out of file
get_title_artist_from_file(FOLDER_PATH, YOUTUBE, prefix_list)
