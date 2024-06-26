import os
import shutil
import time
from pytube import YouTube
import requests
from threading import Thread, active_count
from time import sleep
import re
import unicodedata

def safe_move(src, dst, max_retries=10, delay=5):
    for attempt in range(max_retries):
        try:
            if os.path.exists(src):
                shutil.move(src, dst)
                print(f"Moved file from {src} to {dst} on attempt {attempt+1}")
                return True
            else:
                print(f"Source file not found: {src}")
                return False
        except PermissionError as e:
            print(f"PermissionError on attempt {attempt+1}: {e}")
            time.sleep(delay)
    print(f"Failed to move file from {src} to {dst} after {max_retries} attempts")
    return False

def download_youtube_video(link, FOLDER_PATH, file_path, link_picture):
    print("Downloading video!")
    print(link)
    try:
        yt = YouTube(link)
    except Exception as e:
        print(f"Error initializing YouTube object: {e}")
        return
    
    available_streams = yt.streams.filter(progressive=True)
    if not available_streams:
        available_streams = yt.streams.filter(adaptive=True)

    print("Available streams:")
    for stream in available_streams:
        print(f"{stream.resolution}, progressive={stream.is_progressive}, type={stream.mime_type}")

    try:
        # Prioritize highest resolution
        stream = yt.streams.get_highest_resolution()
        downloaded_file_path = stream.download(FOLDER_PATH, max_retries=10)
    except Exception as e:
        print(f"Error downloading highest resolution: {e}")
        # Try alternative resolution if highest resolution fails
        try:
            stream = max(available_streams, key=lambda x: x.resolution)
            downloaded_file_path = stream.download(FOLDER_PATH, max_retries=10)
        except Exception as e:
            print(f"Error downloading alternative resolution: {e}")
            return
    
    title = replace_non_ascii(yt.title)
    print("Download completed: " + title)

    new_file_path = os.path.join(FOLDER_PATH, title + '.' + stream.mime_type.split('/')[-1])
    print("Original file path: ", downloaded_file_path)
    if os.path.exists(downloaded_file_path):
        if not safe_move(downloaded_file_path, new_file_path):
            print("Failed to move the downloaded file after multiple attempts.")
            return
    else:
        print(f"File does not exist: {downloaded_file_path}")
        return

    if link_picture != 1:
        try:
            response = requests.get(link_picture)
            if response.status_code == 200:
                with open(FOLDER_PATH + "/" + title + ".jpg", 'wb') as file:
                    file.write(response.content)
                print("Image downloaded successfully as", FOLDER_PATH + "/" + title + ".jpg")
            else:
                print("Failed to download the image")
        except Exception as e:
            print(f"Website not reachable: {e}")

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
                        if not link_picture.startswith("https://"):
                            link_picture = "https://" + link_picture
                    else:
                        link_picture = 1

                    x1 = 9
                    x2 = line.find("co=") - 1
                    if not x2 >= 1:
                        x2 = len(line)

                    video_id = line[x1:x2]
                    if len(video_id) == 11:
                        link = "https://www.youtube.com/watch?v=" + video_id
                    else:
                        print(f"Invalid video ID: {video_id}")
                        continue
            
            delete_lines_with_prefix(file_path, prefix_list)

            while active_count() > int(number_of_threads):
                sleep(0.01)
            if 'link' in locals():
                x = Thread(target=download_youtube_video, args=(link, FOLDER_PATH, file_path, link_picture))
                x.start()

def rename_file_and_add_line(title, file_path, FOLDER_PATH):
    print("Changing file")
    title = replace_non_ascii(title)
    with open(file_path, 'r') as old_file:
        old_content = old_file.read()
    with open(file_path, 'w') as new_file:
        new_file.write("#VIDEO:" + title + ".mp4" + '\n' + "#MP3:" + title + ".mp4" + '\n' + "#COVER:" + title + ".jpg" + '\n' + old_content)

def replace_non_ascii(text):
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = re.sub(r'[^a-zA-Z0-9_\s]', '', text)
    text = text.replace(' ', '_')
    return text

def run_ultrastar_downloader(FOLDER_PATH, prefix_list, number_of_threads2):
    global number_of_threads
    number_of_threads = number_of_threads2
    get_title_artist_from_file(FOLDER_PATH, prefix_list)
