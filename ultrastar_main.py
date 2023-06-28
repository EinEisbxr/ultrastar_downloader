global FOLDER_PATH, FOLDER_PATH2,start, name, execute, number_of_threads, search_results, progress

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
progress = 0

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
            
        with open("config.txt","r") as f:
            configlines = f.readlines()
        with open("config.txt","w") as f:
            for line in configlines:
                if line.startswith("DEFAULT_THREADS="):
                    f.write(f"DEFAULT_THREADS={number_of_threads}\n")
                else:
                    f.write(line + "\n")
        
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
        search_results.delete(0,tk.END)
        path_label['text'] = name
        path_label['bg'] = "white"
        FOLDER_PATH = name
        FOLDER_PATH2 = f"{name}/NoYoutubeLink"
        with open("config.txt","r") as f:
            configlines = f.readlines()
        with open("config.txt","w") as f:
            for line in configlines:
                if line.startswith("DEFAULT_DIRECTORY="):
                    f.write(f"DEFAULT_DIRECTORY={name}\n")
                else:
                    f.write(line + "\n")
        count = 0
        start_button_all3["bg"] = "white"
        start_button_label_all['bg'] = "white"
        start_button['bg'] = "white"
        start_button_label['bg'] = "white"
        for file_name in os.listdir(FOLDER_PATH):
            if file_name.endswith(".txt"):
                search_results.insert(tk.END, f"{count+1}# {file_name}\n")
                count += 1
                #print("added")

def programm():
    global start, name, progress
    if start == 0 and name != "":
        start = 1
        
        path_label['bg'] = "grey"
        file_open_button['bg'] = "gray"
        
        if progress < 1:
            progress = 1
        start_button["bg"] = "grey"
        start_button_label["bg"] = "grey"
        start_button2["bg"] = "grey"
        start_button_label2["bg"] = "grey"
        start_button3["bg"] = "grey"
        start_button_label3["bg"] = "grey"
        start_button_label_all['bg'] = "grey"
        start_button_all3['bg'] = "grey"
        root.update_idletasks()
        
        run_checker(FOLDER_PATH)

        print("#########Finished#########")
        
        start_button["bg"] = "white"
        start_button_label["bg"] = "red"
        start_button_label["text"] = "FINISHED"
        start_button_label_all['bg'] = "white"
        start_button_all3['bg'] = "white"
        path_label['bg'] = "white"
        file_open_button['bg'] = "white"
        if progress == 1:
            start_button2["bg"] = "white"
            start_button_label2["bg"] = "white"
        elif progress >= 2:
            start_button2["bg"] = "white"
            start_button_label2["bg"] = "white"
            start_button3["bg"] = "white"
            start_button_label3["bg"] = "white"
        root.update_idletasks()
        sleep(0.5)
        
        start_button_label["bg"] = "white"
        start_button_label["text"] = "Run Checker"
        root.update_idletasks()
        start = 0
        
        
def programm1():
    global start, name, progress
    if start == 0 and name != "" and progress >= 1:
        start = 1
        
        path_label['bg'] = "grey"
        file_open_button['bg'] = "gray"
        
        if progress < 2:
            progress = 2
        start_button["bg"] = "grey"
        start_button_label["bg"] = "grey"
        start_button2["bg"] = "grey"
        start_button_label2["bg"] = "grey"
        start_button3["bg"] = "grey"
        start_button_label3["bg"] = "grey"
        start_button_label_all['bg'] = "grey"
        start_button_all3['bg'] = "grey"
        root.update_idletasks()
        
        add_youtube_links(FOLDER_PATH2, prefix_list2)

        print("#########Finished#########")
        
        start_button2["bg"] = "white"
        start_button_label2["bg"] = "red"
        start_button_label2["text"] = "FINISHED"
        start_button["bg"] = "white"
        start_button_label["bg"] = "white"
        start_button_label_all['bg'] = "white"
        start_button_all3['bg'] = "white"
        path_label['bg'] = "white"
        file_open_button['bg'] = "white"
        
        if progress == 3:
            
            start_button3["bg"] = "white"
            start_button_label3["bg"] = "white"
        root.update_idletasks()
        sleep(0.5)
        
        start_button_label2["bg"] = "white"
        start_button_label2["text"] = "Add Youtube Links"
        root.update_idletasks()
        start = 0
        

def programm2():
    global start, name, progress
    if start == 0 and name != "" and progress >= 2:
        start = 1
        
        path_label['bg'] = "grey"
        file_open_button['bg'] = "gray"
        
        if progress < 3:
            progress = 3
        start_button["bg"] = "grey"
        start_button_label["bg"] = "grey"
        start_button2["bg"] = "grey"
        start_button_label2["bg"] = "grey"
        start_button3["bg"] = "grey"
        start_button_label3["bg"] = "grey"
        start_button_label_all['bg'] = "grey"
        start_button_all3['bg'] = "grey"
        root.update_idletasks()
        
        run_ultrastar_downloader(FOLDER_PATH, prefix_list1, number_of_threads)
        
        while active_count() > 1:
            sleep(0.5)
            #print(active_count())

        print("#########Finished#########")
        
        start_button_label3["text"] = "FINISHED"
        start_button["bg"] = "white"
        start_button_label["bg"] = "white"
    
        start_button2["bg"] = "white"
        start_button_label2["bg"] = "white"
        start_button3["bg"] = "white"
        start_button_label3["bg"] = "red"
        path_label['bg'] = "white"
        file_open_button['bg'] = "white"
        root.update_idletasks()
        sleep(1)
        
        start_button_label3["bg"] = "white"
        start_button_label3["text"] = "Download Videos and Images"
        root.update_idletasks()
        start = 0
        

def programmall():
    global start, name, start_button, start_button_label, progress
    if start == 0 and name != "":
        start = 1
        progress = 3
        path_label['bg'] = "grey"
        file_open_button['bg'] = "gray"
        start_button_label['bg'] = "grey"
        start_button['bg'] = "grey"
        start_button_label2['bg'] = "grey"
        start_button2['bg'] = "grey"
        start_button_label3['bg'] = "grey"
        start_button3['bg'] = "grey"
        start_button_label_all['bg'] = "grey"
        start_button_all3['bg'] = "grey"
        root.update_idletasks()
        start_button_label_all["text"] = "Running Checker"
        root.update_idletasks()
        
        run_checker(FOLDER_PATH)
        print("#########Finished#########")
        start_button_label_all["text"] = "Adding Youtube Links"
        root.update_idletasks()
    
        add_youtube_links(FOLDER_PATH2, prefix_list2)
        print("#########Finished#########")
        start_button_label_all["text"] = "Downloading Videos and Images"
        start_button_label_all.place(relx=0.6/4, rely=0.93, anchor=tk.S, y=-padding*3)
        root.update_idletasks()
        
    
        run_ultrastar_downloader(FOLDER_PATH, prefix_list1, number_of_threads)
        while active_count() > 1:
            sleep(0.5)
            #print(active_count())
        print("#########Finished#########")
        
        start_button_label_all.place(relx=0.37/4, rely=0.93, anchor=tk.S, y=-padding*3)
        start_button_label_all["text"] = "Finished"
        start_button_all3["text"] = "Finished"
        coollabel["text"] = "FinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinishedFinished"
        coollabel["bg"] = "red"
        coollabel["fg"] = "white"
        start_button_label_all["bg"] = "red"
        start_button_all3["bg"] = "red"
        root.update_idletasks()
        sleep(3)
        
        coollabel["bg"] = "#026873"
        coollabel["fg"] = "white"
        coollabel["text"] = "Ultrastar Deluxe Song Downloader"
        start_button_all3["bg"] = "white"
        start_button_all3["text"] = "START"
        start_button_label['bg'] = "white"
        start_button['bg'] = "white"
        start_button_label2['bg'] = "white"
        start_button2['bg'] = "white"
        start_button_label3['bg'] = "white"
        start_button3['bg'] = "white"
        start_button_label_all['bg'] = "white"
        start_button_all3['bg'] = "white"

        start_button_label_all["text"] = "Execute All"
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

global path_label, file_open_button, thread_entry_label, thread_entry_label2, thread_entry, coollabel

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
# Create a frame for the listbox and set its background color
listbox_frame = tk.Frame(root, bg='#026873')
listbox_frame.pack(side=tk.TOP, padx=padding, pady=padding, fill=tk.BOTH, expand=True)
search_results = tk.Listbox(listbox_frame, height=1, font=('Arial', 23), bg='#04BF8A', selectmode='none')
search_results.pack(side=tk.LEFT, padx=padding, pady=padding, fill=tk.BOTH, expand=True)

global start_button_label, start_button, start_button_label2, start_button2, start_button_label3, start_button3, start_button_label_all, start_button_all3

start_button_label = tk.Label(root, text='Run Checker 1', font=('Arial', 28), bg="gray")
start_button_label.place(relx=1.3/4, rely=0.93, anchor=tk.S, y=-padding*3)

start_button = tk.Button(root, text='START', command=programm, font=('Arial', 30), bg="gray")
start_button.place(relx=1.3/4, rely=1, anchor=tk.S, y=-padding)

# Create the second label and button
start_button_label2 = tk.Label(root, text='Add Youtube Links', font=('Arial', 28),bg="gray")
start_button_label2.place(relx=2.3/4, rely=0.93, anchor=tk.S, y=-padding*3)

start_button2 = tk.Button(root, text='START', command=programm1, font=('Arial', 30), bg="gray")
start_button2.place(relx=2.3/4, rely=1, anchor=tk.S, y=-padding)

# Create the third label and button
start_button_label3 = tk.Label(root, text='Download Videos and Images', font=('Arial', 28) , bg="gray")
start_button_label3.place(relx=3.3/4, rely=0.93, anchor=tk.S, y=-padding*3)

start_button3 = tk.Button(root, text='START', command=programm2, font=('Arial', 30), bg="gray")
start_button3.place(relx=3.3/4, rely=1, anchor=tk.S, y=-padding)

start_button_label_all = tk.Label(root, text='Execute all', font=('Arial', 28), bg="gray")
start_button_label_all.place(relx=0.37/4, rely=0.93, anchor=tk.S, y=-padding*3)

start_button_all3 = tk.Button(root, text='START', command=programmall, font=('Arial', 30), bg="gray")
start_button_all3.place(relx=0.37/4, rely=1, anchor=tk.S, y=-padding)

with open("config.txt","r") as f:
            configlines = f.readlines()

for line in configlines:
    
    if line.startswith("DEFAULT_THREADS="):
        line = line.replace("DEFAULT_THREADS=","")
        line = line.replace("\n","")
        if not line == "" and not line == "\n":
            number_of_threads = int(line)
            thread_entry.insert(tk.END,number_of_threads)
        
    elif line.startswith("DEFAULT_DIRECTORY="):
        line = line.replace("\n","")
        line = line.replace("DEFAULT_DIRECTORY=","")
        if not line == "" and not line == "\n":
            name = line
            path_label['text'] = name
            path_label['bg'] = "white"
            FOLDER_PATH = name
            FOLDER_PATH2 = f"{name}/NoYoutubeLink"
            count = 0
            start_button_all3["bg"] = "white"
            start_button_label_all['bg'] = "white"
            start_button['bg'] = "white"
            start_button_label['bg'] = "white"
            for file_name in os.listdir(FOLDER_PATH):
                if file_name.endswith(".txt"):
                    search_results.insert(tk.END, f"{count+1}# {file_name}\n")
                    count += 1
                    #print("added")


root.mainloop()
