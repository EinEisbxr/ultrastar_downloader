import os
import re
import unicodedata
from pytube import *
from moviepy.editor import *
from youtubesearchpython import VideosSearch


def extract_view_count(video):
    """
    Extract the view count of a video from its search result.
    Returns the view count as an integer.
    """
    vc = video.get('viewCount')
    if isinstance(vc, dict) and 'text' in vc:
        text = vc['text']
        digits = re.sub(r'[^\d]', '', text)
        try:
            return int(digits) if digits else 0
        except Exception:
            return 0
    try:
        return int(vc)
    except Exception:
        return 0


def delete_lines_with_prefix(file_path, prefix_list):
    """Delete all lines from a file that start with any prefix in prefix_list."""
    with open(file_path, 'r+', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()
        for line in lines:
            if not any(line.startswith(prefix) for prefix in prefix_list):
                file.write(line)


def get_link_to_youtube(search_query, song_length):
    """
    Search YouTube for videos matching search_query and select the video whose duration 
    is closest to song_length. If two videos are within a 3-second difference of the target,
    the one with the higher view count is chosen.
    """
    try:
        videos_search = VideosSearch(search_query, limit=100)
        result = videos_search.result()

        # Ensure we have some results.
        if not result.get('result'):
            print(f"No results found for query: {search_query}")
            return None

        best_candidate = None
        best_diff = float('inf')

        for video in result['result']:
            duration_str = video.get('duration', '')
            duration_seconds = parse_duration(duration_str)
            if duration_seconds is None:
                continue

            diff = abs(duration_seconds - song_length)
            # print(f"Video: {video.get('title')}, Duration: {duration_seconds}, Diff: {diff}, song_length: {song_length}")
            # Check if this video is a better candidate.
            if best_candidate is None or diff < best_diff:
                best_candidate = video
                best_diff = diff
            # If the difference is nearly the same (within 3 seconds), choose the one with more views.
            elif abs(diff - best_diff) <= 3:
                current_views = extract_view_count(video)
                best_views = extract_view_count(best_candidate)
                if current_views > best_views:
                    best_candidate = video

        if best_candidate:
            return best_candidate.get('link')
        else:
            print(f"No suitable video found for query: {search_query}")
            return None
    except Exception as e:
        print(f"An error occurred in get_link_to_youtube: {e}")
        return None


def parse_duration(duration_str):
    """Parse a duration string in the format M:SS or H:MM:SS into seconds."""
    try:
        parts = duration_str.split(':')
        parts = [int(p) for p in parts]
        if len(parts) == 2:
            minutes, seconds = parts
            return minutes * 60 + seconds
        elif len(parts) == 3:
            hours, minutes, seconds = parts
            return hours * 3600 + minutes * 60 + seconds
        else:
            return None
    except Exception as e:
        print(f"Failed to parse duration '{duration_str}': {e}")
        return None


def get_title_artist_from_file(folder_path, prefix_list):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            artist_line = title_line = gap_line = bpm_line = song_beats = None
            co_part = None

            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()

            for idx, line in enumerate(lines):
                if line.startswith('#ARTIST'):
                    artist_line = line.strip().replace("#ARTIST:", "").strip()
                    print(f"Found Artist: {artist_line}")
                elif line.startswith("#TITLE"):
                    title_line = line.strip().replace("#TITLE:", "").strip()
                    print(f"Found Title: {title_line}")
                elif line.startswith('#GAP'):
                    # Replace comma with dot for decimal conversion.
                    gap_line = line.strip().replace("#GAP:", "").replace(",", ".").strip()
                elif line.startswith('#BPM'):
                    bpm_line = line.strip().replace("#BPM:", "").replace(",", ".").strip()
                elif line.startswith("#VIDEO") and not line.startswith("#VIDEOGAP:"):
                    x1 = line.find("co=")
                    if x1 != -1:
                        co_part = line[x1:].strip()
                # Assuming song_beats is on the penultimate line
                if idx == len(lines) - 2:
                    song_beats = line.split(" ")[1]
                    print(f"Found Song Beats: {song_beats}")
                    last_line_beats = line.split(" ")[2]
                    print(f"Found Last Line Beats: {last_line_beats}")

            if not (artist_line and title_line and gap_line and bpm_line and song_beats):
                print(f"Missing required tags in file: {filename}")
                continue

            try:
                song_length = (((float(song_beats) + float(last_line_beats)) / (float(bpm_line) * 4)) * 60) + (float(gap_line) / 1000) 
            except Exception as e:
                print(f"Error calculating song length for {filename}: {e}")
                continue

            search_query = f"{artist_line} {title_line}"
            print(f"Searching for: {search_query}")

            delete_lines_with_prefix(file_path, prefix_list)
            link = get_link_to_youtube(search_query, song_length)
            if link:
                # Remove the base URL
                video_id_part = link.replace("https://www.youtube.com/watch?", "")
                rename_file_and_add_line(video_id_part, file_path, filename, folder_path, co_part)
            else:
                print(f"Could not obtain a YouTube link for {filename}.")


def rename_file_and_add_line(video_id_part, file_path, filename, folder_path, co_part):
    """
    Prepend the file with a #VIDEO: line containing the video id part.
    If the original #VIDEO: line had an 'a=' parameter and video_id_part does not include it,
    the 'a=' parameter is appended.
    Then move the file back to the main directory (if it was in NoYoutubeLink subfolder).
    """
    print(f"Changing file {filename} with video id {video_id_part}")
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as old_file:
        old_content = old_file.read()

    # Extract any existing ',a=...' part from the old #VIDEO: line.
    a_param = ""
    for line in old_content.splitlines():
        if line.startswith("#VIDEO:"):
            match = re.search(r'a=([^,\s\n]+)', line)
            if match and "a=" not in video_id_part:
                a_param = match.group(1)
            break

    with open(file_path, 'w', encoding='utf-8', errors='ignore') as new_file:
        new_video_line = f"#VIDEO:{video_id_part}{a_param}"
        if co_part:
            new_video_line += f" {co_part}"
        new_video_line += "\n"
        new_file.write(new_video_line + old_content)

    # Move file to the main folder if needed.
    main_folder = folder_path.replace("NoYoutubeLink", "")
    src = os.path.join(folder_path, filename)
    dst = os.path.join(main_folder, filename)
    try:
        os.replace(src, dst)
        print(f"File {filename} moved to {dst}")
    except Exception as e:
        print(f"Error moving file {filename} to {dst}: {e}")

def replace_non_ascii(text):
    """
    Remove non-ascii characters and special symbols from text.
    """
    text = ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')
    text = re.sub(r'[^a-zA-Z0-9_\s]', '', text)  # remove special characters
    text = text.replace(' ', '_')  # replace spaces with underscores
    return text


def add_youtube_links(folder_path, prefix_list):
    get_title_artist_from_file(folder_path, prefix_list)