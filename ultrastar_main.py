global FOLDER_PATH, FOLDER_PATH2,start, name, execute, number_of_threads, search_results

from ultrastar_downloader import *
from ultrastar_checker import *
from ultrastar_add_YouTube_links import *
import tkinter as tk
import tkinter.messagebox
from time import *
from tkinter import filedialog as fd 
import os
from threading import *

FOLDER_PATH = "C:/Texte"
FOLDER_PATH2 = "C:/Texte/NoYoutubeLink"
start = 0
name = ""
execute = 0
number_of_threads = 10

prefix_list1 = ['#VIDEO', '#MP3', "#COVER"]
prefix_list2 = ['#VIDEO']




def changethreads():
    
    global number_of_threads,thread_entry_label
    number_of_threads = thread_entry.get()

    #print(number_of_threads)
    if number_of_threads != "" and number_of_threads != None and number_of_threads.isnumeric():
        number_of_threads = int(number_of_threads)
        thread_entry_label2["text"] = ""
        root.update_idletasks()
        if number_of_threads > 16:
            number_of_threads = 16
            thread_entry.delete(0,tk.END)
            thread_entry.insert(tk.END,number_of_threads)
        
        if number_of_threads < 2:
            number_of_threads = 2
            thread_entry.delete(0,tk.END)
            thread_entry.insert(tk.END,number_of_threads)
            
        
        number_of_threads = str(number_of_threads)
        thread_entry_label2["text"] = "Updated to: " + number_of_threads
        thread_entry_label2["bg"] = "red"
        root.update_idletasks()
        sleep(2)
        thread_entry_label2["text"] = "Change"
        thread_entry_label2["bg"] = "gray"
        
    


def callback():
    global FOLDER_PATH, FOLDER_PATH2, start, name, start_button, start_button_label
    if start == 0:
        name= fd.askdirectory() 
        #print(name)
        path_label['text'] = name
        path_label['bg'] = "white"
        FOLDER_PATH = name
        FOLDER_PATH2 = f"{name}/NoYoutubeLink"
        count = 0
        for file_name in os.listdir(FOLDER_PATH):
            if file_name.endswith(".txt"):
                search_results.insert(tk.END, f"{count+1}# {file_name}\n")
                count += 1
                #print("added")

   

def programm():
    global start, name, start_button, start_button_label, execute
    if start == 0 and name != "":
        start = 1
        path_label['bg'] = "grey"
        file_open_button['bg'] = "gray"
        start_button_label['bg'] = "grey"
        start_button['bg'] = "grey"
        root.update_idletasks()
        
        if execute == 0:
            run_checker(FOLDER_PATH)
            print("#########Finished#########")
            start_button_label["text"] = "Add Youtube Links"
        if execute == 1:
            add_youtube_links(FOLDER_PATH2, prefix_list2)
            print("#########Finished#########")
            start_button_label["text"] = "Download Videos and Images"
            
        if execute == 2:
            run_ultrastar_downloader(FOLDER_PATH, prefix_list1, number_of_threads, search_results)
            while active_count() > 1:
                sleep(1)
                #print(active_count())
            print("#########Finished#########")
            start_button_label["text"] = "Finished"
            start_button["text"] = "Finished"
            coollabel["text"] = "FinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinished"
            coollabel["bg"] = "red"
            coollabel["fg"] = "white"
            start_button_label["bg"] = "red"
            start_button["bg"] = "red"
            root.update_idletasks()
            sleep(2)
            
            coollabel["bg"] = "#026873"
            coollabel["fg"] = "white"
            coollabel["text"] = "Ultrastar Deluxe Song Downloader"
            start_button["bg"] = "white"
            start_button["text"] = "START"
            execute += 1
            
        
        if execute == 3:
            execute = 0
            start_button_label["text"] = "Run Checker"

        
        execute += 1
        path_label['bg'] = "white"
        file_open_button['bg'] = "white"
        start_button_label['bg'] = "white"
        start_button['bg'] = "white"
        start = 0
        
# Create tkinter window
global root
root = tk.Tk()
root.title("Ultrastar Deluxe Song Downloader")
root.attributes('-fullscreen', True)
padding = 10
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width - (2*padding)
window_height = screen_height - (2*padding)
window_x = padding
window_y = padding
root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
root.configure(bg='#026873')

global path_label, file_open_button, start_button_label, start_button, thread_entry_label, thread_entry_label2, thread_entry, coollabel

# Create search bar
coollabel = tk.Label(text="Ultrastar Deluxe Song Downloader", font=('Helvetica', 48, 'bold'), bg='#026873', fg='white')
coollabel.pack(side=tk.TOP, pady=20)
    

errmsg = 'Error!'
file_open_button = tk.Button(text='Select Folder with txt Files', command=callback,  font=('Arial', 30))
file_open_button.pack(side=tk.TOP, pady=padding, padx=(window_width/4, window_width/4))

path_label = tk.Label(text='',  font=('Arial', 28))
path_label.pack(side=tk.TOP, pady=padding, padx=(window_width/4, window_width/4))
path_label['bg'] = "#026873"

thread_entry_label = tk.Label(text='',  font=('Arial', 24), bg="#026873", fg="white")
thread_entry_label.pack(side=tk.TOP, anchor=tk.NE, pady=padding, padx=padding)
thread_entry_label["text"] = "Number of Threads"

thread_entry = tk.Entry(root,  font=('Arial', 24), bg="grey", fg="white")
thread_entry.pack(side=tk.TOP, anchor=tk.NE, padx=padding)

thread_entry_label2 = tk.Button(text='Change',command=changethreads,  font=('Arial', 21), bg="gray", fg="white")
thread_entry_label2.pack(side=tk.TOP, anchor=tk.NE, pady=padding, padx=padding)


# Create listbox
listbox_frame = tk.Frame(root, bg='#026873')
listbox_frame.pack(side=tk.TOP, padx=padding, pady=padding, fill=tk.BOTH, expand=True)
search_results = tk.Listbox(listbox_frame, height=10, font=('Arial', 23), bg='#04BF8A', selectmode='none')
search_results.pack(side=tk.LEFT, padx=padding, pady=padding, fill=tk.BOTH, expand=True)


start_button_label = tk.Label(text='Run Checker',  font=('Arial', 28))
start_button_label.pack(side=tk.BOTTOM, pady=padding, padx=(window_width/4, window_width/4))
start_button_label['bg'] = "white"

start_button = tk.Button(text='START', command=lambda: [programm()],  font=('Arial', 30))
start_button.pack(side=tk.BOTTOM, pady=padding, padx=(window_width/4, window_width/4))


root.mainloop()
