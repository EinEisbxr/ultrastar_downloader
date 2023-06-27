# ultrastar_downloader
A tool to download the song and image data to an UltraStar Deluxe text file.


# How to use
1. Download UltraStar Deluxe text files from: https://usdb.animux.de/ or https://usdb.eu/ (this rarely adds a link after #VIDEO:) . In the text file at #VIDEO: this part of the youtube link has to be supplied: v=???????????

2. Move them all into a folder and in the code change the FOLDER_PATH

3. Run the programm and wait a bit

4. Copy everything into your UltraStar Deluxe song folder

test
# How it works:
1. The programm extracts the link and downloads the video from Youtube

2. It tries to download a picture to the video as a Cover
  
3. It renames the downloaded files and it adds the names of them in the text file
