from ultrastar_downloader import *
from ultrastar_checker import *
from ultrastar_add_YouTube_links import *
from time import *

FOLDER_PATH = "C:\Texte"
FOLDER_PATH2 = "C:\Texte/NoYoutubeLink"

prefix_list1 = ['#VIDEO', '#MP3', "#COVER"]
prefix_list2 = ['#VIDEO']


run_checker(FOLDER_PATH)

sleep(1)

add_youtube_links(FOLDER_PATH2, prefix_list2)

sleep(1)

run_ultrastar_downloader(FOLDER_PATH, prefix_list1)
