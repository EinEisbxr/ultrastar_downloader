import customtkinter as ctk
from ultrastar_downloader import run_ultrastar_downloader
from ultrastar_checker import run_checker
from ultrastar_add_YouTube_links import add_youtube_links
import tkinter as tk
from tkinter import filedialog as fd
import os
from threading import Thread, active_count as threading_active_count
from time import sleep

# Initialize global variables
FOLDER_PATH = "C:/Texte"
FOLDER_PATH2 = "C:/Texte/NoYoutubeLink"
start = 0
name = ""
execute = 0
number_of_threads = 10
progress = 0

prefix_list1 = ['#VIDEO:', '#MP3:', "#COVER:"]
prefix_list2 = ['#VIDEO:']

# Functions

def busy(madeprogress):
    global progress
    if madeprogress is not None and progress < madeprogress:
        progress = madeprogress
    path_label.configure(fg_color="grey")
    file_open_button.configure(fg_color="grey")
    for button in buttons:
        button.configure(fg_color="grey")
    root.update_idletasks()
    start = 1

def unbusy():
    path_label.configure(fg_color="white")
    file_open_button.configure(fg_color="white")
    for button in buttons:
        button.configure(fg_color="white")
    root.update_idletasks()
    start = 0

def eisbxrerror(e):
    print("An error occurred:", e)
    coollabel.configure(text="ERROR", text_color="white", fg_color="red")
    path_label.configure(text="Blame Eisbxr", text_color="white", fg_color="red")
    file_open_button.configure(text="ERROR", text_color="white", fg_color="red")
    root.update_idletasks()

def refresh_search_results():
    count = 0
    search_results.delete('1.0', tk.END)  # Use '1.0' to indicate the start of the text
    for file_name in os.listdir(FOLDER_PATH):
        if file_name.endswith(".txt"):
            search_results.insert(tk.END, f"{count + 1}# {file_name}\n")
            count += 1

def changethreads():
    global number_of_threads
    number_of_threads = thread_entry.get()
    if number_of_threads.isdigit():
        number_of_threads = int(number_of_threads)
        thread_entry_label2.configure(text="")
        if number_of_threads > 30:
            number_of_threads = 30
        elif number_of_threads < 2:
            number_of_threads = 2
        thread_entry.delete(0, tk.END)
        thread_entry.insert(tk.END, number_of_threads)
        with open("config.txt", "r", encoding='utf-8', errors='ignore') as f:
            configlines = f.readlines()
        with open("config.txt", "w") as f:
            for line in configlines:
                if line.startswith("DEFAULT_THREADS="):
                    f.write(f"DEFAULT_THREADS={number_of_threads}\n")
                else:
                    f.write(line)
        thread_entry_label2.configure(text=f"Updated to: {number_of_threads}", fg_color="red")
        root.update_idletasks()
        sleep(1.5)
        thread_entry_label2.configure(text="Change", fg_color="grey")

def callback():
    global FOLDER_PATH, FOLDER_PATH2, start, name, progress
    if start == 0:
        newname = fd.askdirectory()
        if newname:
            name = newname
            progress = 0
            busy(None)
            unbusy()
            search_results.delete('1.0', tk.END)  # Correct index for deleting text in a Text widget
            path_label.configure(text=name, fg_color="white")
            FOLDER_PATH = name
            FOLDER_PATH2 = f"{name}/NoYoutubeLink"
            with open("config.txt", "r", encoding='utf-8', errors='ignore') as f:
                configlines = f.readlines()
            with open("config.txt", "w") as f:
                for line in configlines:
                    if line.startswith("DEFAULT_DIRECTORY="):
                        f.write(f"DEFAULT_DIRECTORY={name}\n")
                    else:
                        f.write(line)
            count = 0
            for file_name in os.listdir(FOLDER_PATH):
                if file_name.endswith(".txt"):
                    search_results.insert(tk.END, f"{count + 1}# {file_name}\n")
                    count += 1

def programm():
    refresh_search_results()
    global start, name, progress
    if start == 0 and name:
        busy(1)
        # try:
        run_checker(FOLDER_PATH)
        # except Exception as e:
        #     eisbxrerror(e)
        #     return
        unbusy()
        start_button_label.configure(fg_color="red", text="FINISHED")
        root.update_idletasks()
        sleep(0.5)
        start_button_label.configure(fg_color="white", text="Run Checker")
        root.update_idletasks()
        start = 0

def programm1():
    refresh_search_results()
    global start, name, progress
    if start == 0 and name and progress >= 1:
        busy(2)
        try:
            add_youtube_links(FOLDER_PATH2, prefix_list2)
        except Exception as e:
            eisbxrerror(e)
            return
        unbusy()
        start_button_label2.configure(fg_color="red", text="FINISHED")
        root.update_idletasks()
        sleep(0.5)
        start_button_label2.configure(fg_color="white", text="Add Youtube Links")
        root.update_idletasks()
        start = 0

def programm2():
    refresh_search_results()
    global start, name, progress
    if start == 0 and name and progress >= 2:
        busy(3)
        try:
            run_ultrastar_downloader(FOLDER_PATH, prefix_list1, number_of_threads)
        except Exception as e:
            eisbxrerror(e)
            return
        while threading_active_count() > 1:
            sleep(0.5)
        unbusy()
        start_button_label3.configure(fg_color="red", text="FINISHED")
        root.update_idletasks()
        sleep(1)
        start_button_label3.configure(fg_color="white", text="Download Videos and Images")
        root.update_idletasks()
        start = 0

def programmall():
    refresh_search_results()
    global start, name, progress
    if start == 0 and name:
        busy(3)
        start_button_label_all.configure(text="Running Checker")
        root.update_idletasks()
        # try:
        run_checker(FOLDER_PATH, number_of_threads)
        # except Exception as e:
        #     eisbxrerror(e)
        #     return
        start_button_label_all.configure(text="Adding Youtube Links")
        root.update_idletasks()
        try:
            add_youtube_links(FOLDER_PATH2, prefix_list2)
        except Exception as e:
            eisbxrerror(e)
            return
        start_button_label_all.configure(text="Downloading Videos and Images")
        root.update_idletasks()
        try:
            run_ultrastar_downloader(FOLDER_PATH, prefix_list1, number_of_threads)
        except Exception as e:
            eisbxrerror(e)
            return
        while threading_active_count() > 2:
            sleep(0.5)
        start_button_label_all.configure(text="Finished", fg_color="red")
        root.update_idletasks()
        sleep(3)
        start_button_label_all.configure(text="Execute All", fg_color="white")
        root.update_idletasks()
        unbusy()

# Create tkinter window
root = ctk.CTk()
root.title("Ultrastar Deluxe Song Downloader")
root.attributes('-fullscreen', True)
padding = 10
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width - (2 * padding)
window_height = screen_height - (2 * padding)
window_x = padding
window_y = padding
root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
root.configure(fg_color='#026873')

# Create UI components
coollabel = ctk.CTkLabel(root, text="Ultrastar Deluxe Song Downloader", font=ctk.CTkFont(size=48, weight="bold"), fg_color='#026873', text_color='white')
coollabel.pack(side=tk.TOP, pady=20)

file_open_button = ctk.CTkButton(root, text='Select Folder with txt Files', command=callback, font=ctk.CTkFont(size=30))
file_open_button.pack(side=tk.TOP, pady=padding, padx=(window_width / 4, window_width / 4))

path_label = ctk.CTkLabel(root, text='', font=ctk.CTkFont(size=28), fg_color='#026873')
path_label.pack(side=tk.TOP, pady=padding, padx=(window_width / 4, window_width / 4))

thread_entry_label = ctk.CTkLabel(root, text='Number of Threads', font=ctk.CTkFont(size=24), fg_color='#026873', text_color='white')
thread_entry_label.pack(side=tk.TOP, anchor=tk.NE, pady=padding, padx=padding)

thread_entry = ctk.CTkEntry(root, font=ctk.CTkFont(size=24), fg_color="grey", text_color="white")
thread_entry.pack(side=tk.TOP, anchor=tk.NE, padx=padding)

thread_entry_label2 = ctk.CTkButton(root, text='Change', command=changethreads, font=ctk.CTkFont(size=21), fg_color="grey", text_color="white")
thread_entry_label2.pack(side=tk.TOP, anchor=tk.NE, pady=padding, padx=padding)

search_results = ctk.CTkTextbox(root, width=window_width / 2, height=window_height / 4, font=ctk.CTkFont(size=22), fg_color="grey", text_color="white")
search_results.pack(side=tk.TOP, pady=padding)

with open("config.txt","r", encoding='utf-8', errors='ignore') as f:
    configlines = f.readlines()

found = False

for line in configlines:
    if line.startswith("DEBUG="):
        line = line.replace("DEBUG=","")
        line = line.replace("\n","")
        if not line == "" and not line == "\n":
            #print(bool(line))
            global debug
            if line == "True":
                debug = 1
                found = True

                start_button_label = ctk.CTkButton(root, text="Run Checker", command=lambda: Thread(target=programm).start(), font=ctk.CTkFont(size=30), fg_color="white", text_color="black")
                start_button_label.pack(side=tk.TOP, pady=padding, padx=(window_width / 4, window_width / 4))

                start_button_label2 = ctk.CTkButton(root, text="Add Youtube Links", command=lambda: Thread(target=programm1).start(), font=ctk.CTkFont(size=30), fg_color="white", text_color="black")
                start_button_label2.pack(side=tk.TOP, pady=padding, padx=(window_width / 4, window_width / 4))

                start_button_label3 = ctk.CTkButton(root, text="Download Videos and Images", command=lambda: Thread(target=programm2).start(), font=ctk.CTkFont(size=30), fg_color="white", text_color="black")
                start_button_label3.pack(side=tk.TOP, pady=padding, padx=(window_width / 4, window_width / 4))

                start_button_label_all = ctk.CTkButton(root, text="Execute All", command=lambda: Thread(target=programmall).start(), font=ctk.CTkFont(size=30), fg_color="white", text_color="black")
                start_button_label_all.pack(side=tk.TOP, pady=padding, padx=(window_width / 4, window_width / 4))

                break

if not found:
    start_button_label = ctk.CTkButton(root, text="Run Checker", command=lambda: Thread(target=programm).start(), font=ctk.CTkFont(size=30), fg_color="white", text_color="black")
    # start_button_label.pack(side=tk.TOP, pady=padding, padx=(window_width / 4, window_width / 4))

    start_button_label2 = ctk.CTkButton(root, text="Add Youtube Links", command=lambda: Thread(target=programm1).start(), font=ctk.CTkFont(size=30), fg_color="white", text_color="black")
    # start_button_label2.pack(side=tk.TOP, pady=padding, padx=(window_width / 4, window_width / 4))

    start_button_label3 = ctk.CTkButton(root, text="Download Videos and Images", command=lambda: Thread(target=programm2).start(), font=ctk.CTkFont(size=30), fg_color="white", text_color="black")
    # start_button_label3.pack(side=tk.TOP, pady=padding, padx=(window_width / 4, window_width / 4))

    start_button_label_all = ctk.CTkButton(root, text="Execute All", command=lambda: Thread(target=programmall).start(), font=ctk.CTkFont(size=30), fg_color="white", text_color="black")
    start_button_label_all.pack(side=tk.TOP, pady=padding, padx=(window_width / 4, window_width / 4))

    with open("config.txt","r", encoding='utf-8', errors='ignore') as f:
            configlines = f.readlines()

for line in configlines:
    
    if line.startswith("DEFAULT_THREADS="):
        line = line.replace("DEFAULT_THREADS=","")
        line = line.replace("\n","")
        if not line == "" and not line == "\n":
            number_of_threads = int(line)
            thread_entry.insert(tk.END,number_of_threads)
        

# Store buttons in a list
buttons = [start_button_label, start_button_label2, start_button_label3, start_button_label_all]

# Run the tkinter main loop
root.mainloop()
