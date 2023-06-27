import os
from threading import *

def get_title_artist_from_file(FOLDER_PATH, YOUTUBE):
    for filename in os.listdir(FOLDER_PATH):
        while active_count() >= 10:
            x = Thread(target=get_artist_from_file, args=(FOLDER_PATH, YOUTUBE, filename))
            x.start
          

def get_artist_from_file(FOLDER_PATH, YOUTUBE, filename):
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
                    if not x2 >= 6:
                        link = 1
                      
                link = "https://www.youtube.com/watch?v=" + line[x1:x2]

        if link_picture == 1:
            print(filename + ": has no link to a picture!"

        else:
            print(filename + ": foud link to picture: " + link_picture)

        if link == 1:
            print(filename + ": has no YouTube link!")

        else:
            print(filename + ": found YouTube link: " + link)
      
