### -------------------- ###
### Tunnel Chat v4.0     ###
### Made by @iaa2005     ###
### -------------------- ###

import random
import string
import dweepy
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
import threading
import binascii
import time
from sys import platform
import ntpath
import os


if platform == "linux" or platform == "linux2": # Linux
    pass
elif platform == "darwin": # OS X
    design = {
        "textCons-width": 48,
        "textCons-height": 22,
        "labelMadeBy-fontsize": 12,
        "labelMadeBy-x": 10,
        "labelMadeBy-y": 37,
    }
elif platform == "win32": # Windows
    design = {
        "textCons-width": 42,
        "textCons-height": 19,
        "labelMadeBy-fontsize": 10,
        "labelMadeBy-x": 12,
        "labelMadeBy-y": 40,
    }

DARK_GREY = "#171717"
WHITE_01 = "white"
WHITE_02 = "#f5f5f5"
WHITE_03 = "#808080"

CHAT_ID = ""

CHAT = []
USERNAME = "alexivanov"
CAN_SEND_FILE = False
FILES = {}
UPDATES_CHECK = True


def send_msg(msg):
    msg_web = dweepy.dweet_for(CHAT_ID, {'text': msg})


window = tk.Tk()
window.geometry("400x650")
window.configure(bg=DARK_GREY)
window.title("Tunnel Chat v4.0")
window.resizable(height=False, width=False)

labelTunnel = tk.Label(text="Tunnel Chat v4.0", bg=DARK_GREY, fg=WHITE_02,
                       font=tkFont.Font(family="Helvetica", size=20, weight="bold"))
labelTunnel.place(x=10, y=10)

labelMadeBy = tk.Label(text="Made by @iaa2005", bg=DARK_GREY, fg=WHITE_03,
                       font=tkFont.Font(family="Helvetica", size=design["labelMadeBy-fontsize"], weight="normal"))
labelMadeBy.place(x=design["labelMadeBy-x"], y=design["labelMadeBy-y"])

Copied = tk.Label(text="Copied", bg=DARK_GREY, fg=DARK_GREY,
                  font=tkFont.Font(family="Helvetica", size=12, weight="normal"))
Copied.place(x=235, y=60)

ChatIDText = tk.Label(text="", bg=DARK_GREY, fg=WHITE_02,
                      font=tkFont.Font(family="Helvetica", size=18, weight="normal"))
ChatIDText.place(x=160, y=75)


def genChatID():
    global CHAT_ID
    if CHAT_ID == "":
        CHAT_ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        ChatIDText.configure(text=CHAT_ID)
        window.clipboard_clear()
        window.clipboard_append(CHAT_ID)
        Copied.configure(fg=WHITE_03)
        # print(CHAT_ID)


genBtn = tk.Button(text="Generate ChatID", width=14, command=genChatID, bd=0)
genBtn.place(x=15, y=75)

labelTunnel = tk.Label(text="Or enter ChatID", bg=DARK_GREY, fg=WHITE_02,
                       font=tkFont.Font(family="Helvetica", size=16, weight="normal"))
labelTunnel.place(x=10, y=105)

EntryChatID = tk.Entry(bd=0, highlightthickness=2, highlightbackground="white")
EntryChatID.place(x=15, y=137)

def connect():
    global CHAT_ID
    if CHAT_ID == "":
        CHAT_ID = EntryChatID.get()
        ChatIDText.configure(text=CHAT_ID)
    input_user.set("")

connectBtn = tk.Button(text="Connect", width=10, command=connect)
connectBtn.place(x=220, y=137)

input_user = tk.StringVar()
input_field = tk.Entry(text=input_user, highlightthickness=2, highlightbackground="white", bd=0, width=32)
input_field.place(x=15, y=587)

textCons = tk.Text(window, width=design["textCons-width"], height=design["textCons-height"], bd=0, wrap="word", spacing1=5, padx=15,
                   fg=WHITE_01, highlightthickness=1, highlightbackground=WHITE_03, bg=DARK_GREY)
textCons.place(x=15, y=175)
textCons.config(cursor="arrow")
# create a scroll bar
scrollbar = tk.Scrollbar(textCons)
# place the scroll bar into the gui window
scrollbar.place(relheight=1, relx=1.01)
scrollbar.config(command=textCons.yview)
textCons.config(state=tk.DISABLED, yscrollcommand=scrollbar.set)


def get_history_chat():
    while CHAT_ID == "":
        pass
    if CHAT_ID != "":
        history = dweepy.get_dweets_for(CHAT_ID)
        for msg in history:
            try:
                date = msg["created"][12:17]
                type = msg["content"]["type"]
                username = msg["content"]["username"]
                if type == "file":
                    for index in int(msg["content"]["data"]["count"]):
                        filename = msg["content"]["data"][str(index)]["name"]
                        text_cons = date + " " + username + ": sent file " + filename
                        textCons.config(state=tk.NORMAL)
                        textCons.insert(tk.END, text_cons + "\n")
                        textCons.config(state=tk.DISABLED)
                        textCons.see(tk.END)
                elif type == "text":
                    data = msg["content"]["data"]
                    data = str(data)[1:]
                    data = bytes.fromhex(data).decode("utf-8")
                    text_cons = date + " " + username + ": " + data
                    textCons.config(state=tk.NORMAL)
                    textCons.insert(tk.END, text_cons + "\n")
                    textCons.config(state=tk.DISABLED)
                    textCons.see(tk.END)
            except:
                pass


def send_msg(input_get):
    data = "x" + binascii.hexlify(input_get.encode("utf-8")).decode("utf-8")
    msg_web = dweepy.dweet_for(CHAT_ID, {'username': USERNAME, 'type': 'text', 'data': data})


def send_text():
    input_get = str(input_field.get())
    if not input_get.isspace() and input_get != "" and CHAT_ID != "":
        send_msg(input_get)
    input_user.set("")
    return "break"


def send_files():
    global CAN_SEND_FILE, FILES, CHAT_ID
    if CAN_SEND_FILE == True and FILES != {} and CHAT_ID != "":
        dweepy.dweet_for(CHAT_ID, {"username": USERNAME, "type": "file", "data": FILES})

def choose_file():
    filenames = filedialog.askopenfilenames(initialdir="/", title="Select a file",
                                            filetype=(("All Files", "*.*"), ("jpeg", "*.jpeg")))
    count = 1
    text_type_files = {}
    for file_name in filenames:
        name, ext = os.path.splitext(file_name)
        name = ntpath.basename(file_name)
        text_type_files[str(count)] = {
            "name": "x" + binascii.hexlify(str(name).encode("utf-8")).decode("utf-8"),
            "ext": "x" + binascii.hexlify(str(ext[1:]).encode("utf-8")).decode("utf-8"),
            "data": "x" + str(open(file_name, 'rb').read().hex())
        }
        count += 1

    text_type_files["value"] = count
    
    if text_type_files != {}:
        global CAN_SEND_FILE, FILES
        FILES = text_type_files
        CAN_SEND_FILE = True
        # print filenames in program
    else:
        pass

    # import pprint
    # pprint.pprint(text_type_files)


sendBtn = tk.Button(text="Send", width=6, command=send_text, bd=0)
sendBtn.place(x=325, y=587)

chooseFile = tk.Button(text="Choose file", width=10, command=choose_file, bd=0)
chooseFile.place(x=220, y=615)

sendFileBtn = tk.Button(text="Send file", width=10, command=send_files, bd=0)
sendFileBtn.place(x=305, y=615)


def loop():
    window.mainloop()


def check_updates():
    global CHAT, CHAT_ID, UPDATES_CHECK
    while CHAT_ID == "" and UPDATES_CHECK:
        pass
    while UPDATES_CHECK:
        try:
            if CHAT == []:
                CHAT = dweepy.get_dweets_for(CHAT_ID)
                for dweet in CHAT:
                    date = dweet["created"][12:17]
                    type = dweet["content"]["type"]
                    username = dweet["content"]["username"]
                    if type == "text":
                        data = dweet["content"]["data"]
                        data = str(data)[1:]
                        data = bytes.fromhex(data).decode("utf-8")
                        text_cons = date + " " + username + ": " + data
                        print(text_cons)
                        textCons.config(state=tk.NORMAL)
                        textCons.insert(tk.END, text_cons + "\n")
                        textCons.config(state=tk.DISABLED)
                        textCons.see(tk.END)
                    elif type == "file":
                        text_cons = newdate[12:17] + " " + username + ": sent file "
                        for index in int(newdweet["content"]["data"]["count"]):
                            filename = newdweet["content"]["data"][str(index)]["name"]
                            filename = bytes.fromhex(filename[1:]).decode("utf-8")
                            text_cons += " " + filename
                        textCons.config(state=tk.NORMAL)
                        textCons.insert(tk.END, text_cons + "\n")
                        textCons.config(state=tk.DISABLED)
                        textCons.see(tk.END)
            else:
                newchat = dweepy.get_dweets_for(CHAT_ID)
                print(newchat)
                print('')
                for newdweet in newchat:
                    newdate = newdweet["created"]
                    checkIS = False
                    for olddweet in CHAT:
                        if olddweet["created"] == newdate:
                            checkIS = True
                    if checkIS == False:
                        type = olddweet["content"]["type"]
                        username = olddweet["content"]["username"]
                        if type == "text":
                            data = olddweet["content"]["data"]
                            data = str(data)[1:]
                            data = bytes.fromhex(data).decode("utf-8")
                            text_cons = newdate[12:17] + " " + username + ": " + data
                            print(text_cons)
                            textCons.config(state=tk.NORMAL)
                            textCons.insert(tk.END, text_cons + "\n")
                            textCons.config(state=tk.DISABLED)
                            textCons.see(tk.END)
                        elif type == "file":
                            text_cons = newdate[12:17] + " " + username + ": sent file "
                            for index in int(newdweet["content"]["data"]["count"]):
                                filename = newdweet["content"]["data"][str(index)]["name"]
                                filename = bytes.fromhex(filename[1:]).decode("utf-8")
                                if username != USERNAME:
                                    data = newdweet["content"]["data"][str(index)]["data"]
                                    with open(filename, 'wb') as file_:
                                        file_.write(bytes.fromhex(data[1:]))
                                        file_.close()
                                text_cons += " " + filename
                            textCons.config(state=tk.NORMAL)
                            textCons.insert(tk.END, text_cons + "\n")
                            textCons.config(state=tk.DISABLED)
                            textCons.see(tk.END)
                CHAT = newchat
        except Exception as e:
            print(e)
        time.sleep(5)
        

# mainloop = threading.Thread(target=loop)
updates = threading.Thread(target=check_updates)

# mainloop.start()
updates.start()

def ask_quit():
    window.destroy()
    global UPDATES_CHECK
    UPDATES_CHECK = False
    exit(0)

window.protocol("WM_DELETE_WINDOW", ask_quit)
window.mainloop()
