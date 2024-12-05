import os
from pytube import *
from moviepy.editor import *
import unicodedata
from youtubesearchpython import VideosSearch
import re
import unicodedata


def delete_lines_with_prefix(file_path, prefix_list):
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()

        for line in lines:
            if not any(line.startswith(prefix) for prefix in prefix_list):
                file.write(line)

    return


def get_link_to_youtube(search_query1, song_length):
    try:
        videosSearch = VideosSearch(search_query1, limit = 5)
        result = videosSearch.result()
        # print(result)

        link = result['result'][0]['link']
        duration = result['result'][0]['duration']
        # print(duration)

        x = duration.find(":")

        x2 = x + 1

        time = float(duration[:x]) * 60 + float(duration[x2:])
        # print(time)

        time2 = song_length * 60

        if time > time2:
            videosSearch = VideosSearch(search_query1, limit = 5)
            result = videosSearch.result()

            link = result['result'][0]['link']
            duration = result['result'][0]['duration']

            time = float(duration[:x]) * 60 + float(duration[x2:])

            if time > time2:
                link = result['result'][1]['link']

        return link

    except Exception as e:
        print('An error occurred:', str(e))
        return None


def get_title_artist_from_file(FOLDER_PATH, prefix_list):
    for filename in os.listdir(FOLDER_PATH):
        if filename.endswith('.txt'):
            file_path = os.path.join(FOLDER_PATH, filename)
            x = 1
            artist_line = title_line = gap_line = bpm_line = song_beats = None
            co_part = None
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            for line in lines:
                if line.startswith('#ARTIST'):
                    artist_line = line.strip().replace("#ARTIST:", "")
                    print("found Artist: " + artist_line)

                if line.startswith("#TITLE"):
                    title_line = line.strip().replace("#TITLE:", "")
                    print("found Title: " + title_line)

                if line.startswith('#GAP'):
                    gap_line = line.strip().replace("#GAP:", "").replace(",", ".")

                if line.startswith('#BPM'):
                    bpm_line = line.strip().replace("#BPM:", "").replace(",", ".")

                if line.startswith("#VIDEO"):
                    x1 = line.find("co=")
                    if x1 != -1:
                        co_part = line[x1:].strip()

                if len(lines) - x == 1:
                    song_beats = line[2:6]
                    print(song_beats)

                x = x + 1

            if not (artist_line and title_line and gap_line and bpm_line and song_beats):
                print(f"Missing required tags in file: {filename}")
                continue

            song_length = (float(song_beats) + float(gap_line)) / float(bpm_line) / 10
            search_query = artist_line + " " + title_line
            print("searching for: " + search_query)
                    
            delete_lines_with_prefix(file_path, prefix_list)
            link = get_link_to_youtube(search_query, song_length)
            rename_file_and_add_line(link.replace("https://www.youtube.com/watch?", ""), file_path, filename, FOLDER_PATH, co_part)
            

def rename_file_and_add_line(title, file_path, filename, FOLDER_PATH, co_part):
    print("Changing file", title)
    with open(file_path, 'r') as old_file:
        old_content = old_file.read()
    
    with open(file_path, 'w') as new_file:
        new_file.write("#VIDEO:" + title)
        if co_part:
            new_file.write(" " + co_part)
        new_file.write("\n" + old_content)

    main_folder = FOLDER_PATH.replace("NoYoutubeLink", "")
    os.replace(FOLDER_PATH + "/" + filename, main_folder + filename)


def replace_non_ascii(text):
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = re.sub(r'[^a-zA-Z0-9_\s]', '', text)  # remove special characters
    text = text.replace(' ', '_')  # replace spaces with underscore
    return text


def add_youtube_links(FOLDER_PATH, prefix_list):
    get_title_artist_from_file(FOLDER_PATH, prefix_list)
