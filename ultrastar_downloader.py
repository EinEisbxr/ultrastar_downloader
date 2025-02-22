import threading
import os
import shutil
import time
import requests
from threading import Thread, active_count
from time import sleep
import re
import unicodedata
import yt_dlp

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

def download_youtube_video(link, FOLDER_PATH, file_path, link_picture, video_id, audio_link):
    print("Downloading video!")
    print(link)
    try:
        # Step 1: Extract video info without downloading
        with yt_dlp.YoutubeDL({'cachedir': False}) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            title = replace_non_ascii(info_dict.get('title', 'video'))
            extension = 'mp4'
            # Step 2: Remove special characters from title
            safe_title = re.sub(r'[^\w\s-]', '', title).strip()
            # Step 3: Define the desired filename
            desired_filename = f"{safe_title}.{extension}"
            desired_file_path = os.path.join(FOLDER_PATH, desired_filename)

        # Step 4: Set ydl_opts with desired outtmpl
        ydl_opts = {
            'outtmpl': desired_file_path,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'merge_output_format': 'mp4',
            'cachedir': False,
        }

        # Download the video with the desired filename
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print(f"Video downloaded and saved as: {desired_filename}")
    except Exception as e:
        print(f"Error downloading video: {e}")
        with lock:
            processed_videos.discard(video_id)
        return

    if not os.path.exists(desired_file_path):
        print(f"Downloaded file not found: {desired_file_path}")
        return

    if link_picture != 1:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(link_picture, headers=headers)
            if response.status_code == 200:
                image_filename = f"{safe_title}.jpg"
                with open(os.path.join(FOLDER_PATH, image_filename), 'wb') as file:
                    file.write(response.content)
                print("Image downloaded successfully as", image_filename)
            else:
                print("Failed to download the image")
        except Exception as e:
            print(f"Website not reachable: {e}")
            
    if audio_link != 1:
        try:
            # Step 1: Extract video info without downloading
            with yt_dlp.YoutubeDL({'cachedir': False}) as ydl:
                info_dict = ydl.extract_info(audio_link, download=False)
                extension_audio = 'mp3'

                desired_filename = f"{safe_title}.{extension_audio}"
                desired_file_path = os.path.join(FOLDER_PATH, desired_filename)

            # Step 4: Set ydl_opts with desired outtmpl
            ydl_opts = {
                'outtmpl': desired_file_path,
                'format': 'bestaudio',
                'cachedir': False,
            }

            # Download the video with the desired filename
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([audio_link])
            print(f"Audio downloaded and saved as: {desired_filename}")
        except Exception as e:
            print(f"Error downloading audio: {e}")
            with lock:
                processed_videos.discard(video_id)
            return
    else:
        extension_audio = extension

    rename_file_and_add_line(safe_title, file_path, FOLDER_PATH, extension, extension_audio)
    with lock:
        processed_videos.discard(video_id)

def delete_lines_with_prefix(file_path, prefix_list):
    with open(file_path, 'r+', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()
        for line in lines:
            if not any(line.startswith(prefix) for prefix in prefix_list):
                file.write(line)
    return

processed_videos = set()
lock = threading.Lock()

def get_title_artist_from_file(FOLDER_PATH, prefix_list):
    for filename in os.listdir(FOLDER_PATH):
        if filename.endswith('.txt'):
            file_path = os.path.join(FOLDER_PATH, filename)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
            for line in lines:
                if line.startswith("#VIDEO") and not line.startswith("#VIDEOGAP:"):
                    print(f"Processing line: {line}")
                    x1 = line.find("co=")
                    if x1 != -1:
                        co_part = line[x1 + 3:].strip()
                        comma_index = co_part.find(',')
                        if comma_index != -1:
                            link_picture = co_part[:comma_index].strip()
                        else:
                            link_picture = co_part

                        if not link_picture.startswith("https://"):
                            link_picture = "https://" + link_picture
                    else:
                        link_picture = 1

                    # Extract video_id using regex to capture the text after "v=" until a comma, space or line end.
                    match = re.search(r'v=([^,\s\n]+)', line)
                    if match:
                        video_id = match.group(1).strip()
                        link = "https://www.youtube.com/watch?v=" + video_id
                    else:
                        print(f"No valid video ID found in line: {line}")
                        continue
                    
                    # if there is an "a=" part in the line, extract the audio_id
                    match = re.search(r'a=([^,\s\n]+)', line)
                    if match:
                        audio_id = match.group(1).strip()
                        audio_link = "https://www.youtube.com/watch?v=" + audio_id
                    else:
                        audio_link = 1

                    # Check if the video has already been processed
                    with lock:
                        if video_id in processed_videos:
                            print(f"Video {video_id} is already being processed.")
                            continue
                        else:
                            processed_videos.add(video_id)

                    delete_lines_with_prefix(file_path, prefix_list)

                    while active_count() > int(number_of_threads):
                        sleep(0.01)
                    x = Thread(target=download_youtube_video, args=(link, FOLDER_PATH, file_path, link_picture, video_id, audio_link))
                    print(f"Link Picture: {link_picture}")
                    x.start()

def rename_file_and_add_line(title, file_path, FOLDER_PATH, extension, extension_audio):
    print("Changing file")
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as old_file:
        old_content = old_file.read()
    with open(file_path, 'w', encoding='utf-8') as new_file:
        new_file.write(
            "#VIDEO:" + title + f".{extension}" + '\n' +
            "#MP3:" + title + f".{extension_audio}" + '\n' +
            "#COVER:" + title + ".jpg" + '\n' +
            old_content
        )

def replace_non_ascii(text):
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = re.sub(r'[^a-zA-Z0-9_\s]', '', text)
    text = text.replace(' ', '_')
    return text

def run_ultrastar_downloader(FOLDER_PATH, prefix_list, number_of_threads2):
    global number_of_threads
    number_of_threads = number_of_threads2
    get_title_artist_from_file(FOLDER_PATH, prefix_list)