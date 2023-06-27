import os
from pytube import *
from moviepy.editor import *
import unicodedata
from youtubesearchpython import VideosSearch



def delete_lines_with_prefix(file_path, prefix_list):
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()

        for line in lines:
            if not any(line.startswith(prefix) for prefix in prefix_list):
                file.write(line)

    return


def get_link_to_youtube(search_query):
    try:
        videosSearch = VideosSearch(search_query, limit = 1)
        result = videosSearch.result()
        link = result['result'][0]['link']

        return link

    except Exception as e:
        print('An error occurred:', str(e))
        return None


def get_title_artist_from_file(FOLDER_PATH, prefix_list):
    for filename in os.listdir(FOLDER_PATH):
        if filename.endswith('.txt'):
            file_path = os.path.join(FOLDER_PATH, filename)
            
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            for line in lines:
                
                if line.startswith('#ARTIST'):
                    artist_line = line.strip().replace("#ARTIST:", "")
                    print("found Artist: " + artist_line)

                if line.startswith("#TITLE"):
                    title_line = line.strip().replace("#TITLE:", "")
                    print("found Title: " + title_line)
                

            search_query = artist_line + " " + title_line
            print("searching for: " + search_query)
                    
            delete_lines_with_prefix(file_path, prefix_list)
            link = get_link_to_youtube(search_query)
            rename_file_and_add_line(link.replace("https://www.youtube.com/watch?", ""), file_path, filename, FOLDER_PATH)
            

def rename_file_and_add_line(title, file_path, filename, FOLDER_PATH):
    print("Changing file")
    title = replace_non_ascii(title)
    with open(file_path, 'r') as old_file:
        old_content = old_file.read()
    

    # Open the file in write mode
    with open(file_path, 'w') as new_file:
        # Write the new line followed by the existing content
        new_file.write("#VIDEO:" + title + "\n" + old_content)

    main_folder = FOLDER_PATH.replace("NoYoutubeLink", "")

    os.replace(FOLDER_PATH + "/" + filename, main_folder + filename)


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


def add_youtube_links(FOLDER_PATH, prefix_list):
    get_title_artist_from_file(FOLDER_PATH, prefix_list)
