import tkinter as tk
from subprocess import Popen
import os
import sys

os.chdir(sys.path[0])

try:
    with open("creds" , "r")as f:
        creds = f.read().split("\n")
except FileNotFoundError:
    creds = None

def next_action():
    if chkbtn.get():
        with open("creds","w") as f:
            f.write(f"{chkbtn.get()}\n{username.get()}\n{clientid.get()}\n{clientsecret.get()}")
    Popen("python loadui.py") #opening the scripts that shows downloaded files
    os.system(f"python SpotifyToMp3.py {url.get()} {False} {username.get()} {clientid.get()} {clientsecret.get()}")

window = tk.Tk()
window.title("Spotify > Mp3")
window.geometry("200x150")
window.resizable(0,0)

username = tk.StringVar()
clientid = tk.StringVar()
clientsecret  = tk.StringVar()
url = tk.StringVar()
chkbtn = tk.IntVar()

User_Label = tk.Label(window , text = "Username:").grid(row = 0)
User_entry = tk.Entry(window , textvariable = username)

client_id_label = tk.Label(window , text = "Client_id:").grid(row = 1)
client_id_entry = tk.Entry(window , textvariable = clientid)

client_secret_label = tk.Label(window , text = "Client_secret").grid(row = 2)
client_secret_entry = tk.Entry(window , textvariable = clientsecret)

url_label = tk.Label(window , text = "Url :").grid(row = 3)
url_entry = tk.Entry(window , textvariable = url)
url_entry.insert(tk.INSERT,"Liked")
url_entry.grid(row = 3 , column = 1)

Save_check = tk.Checkbutton(window , variable = chkbtn , text = "Remember me")

if creds != None:
    try:
        User_entry.insert(tk.INSERT , creds[1])
        client_id_entry.insert(tk.INSERT , creds[2])
        client_secret_entry.insert(tk.INSERT , creds[3])
        Save_check.select()
    except IndexError:
        pass

User_entry.grid(row = 0 , column = 1)
client_id_entry.grid(row = 1 , column = 1)
client_secret_entry.grid(row = 2 , column = 1)
url_entry.grid(row = 3 , column = 1)
Save_check.place(relx = 0.25, rely = 0.55)

Next_button = tk.Button(window , text = "Next" , command = next_action).place(relx = 0.4, rely = 0.75)

window.mainloop()