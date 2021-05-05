### -------------------- ####
### Tunnel Chat v4.0     ####
### Made by @iaa2005     ####
### -------------------- ####

import random
import string
import dweepy
import tkinter as tk
import tkinter.font as tkFont
import threading

DARK_GREY = "#171717"
WHITE_01 = "white"
WHITE_02 = "#f5f5f5"
WHITE_03 = "#808080"

CHAT_ID = ""

CHAT = []
USERNAME = "alexivanov"


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

labelTunnel = tk.Label(text="Made by @iaa2005", bg=DARK_GREY, fg=WHITE_03,
                       font=tkFont.Font(family="Helvetica", size=12, weight="normal"))
labelTunnel.place(x=10, y=37)

Copied = tk.Label(text="Copied", bg=DARK_GREY, fg=DARK_GREY,
                  font=tkFont.Font(family="Helvetica", size=12, weight="normal"))
Copied.place(x=235, y=60)

ChatIDText = tk.Label(text="", bg=DARK_GREY, fg=WHITE_02,
                      font=tkFont.Font(family="Helvetica", size=18, weight="normal"))
ChatIDText.place(x=160, y=75)


def genChatID():
    global CHAT_ID
    if CHAT_ID != "":
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
    pass


connectBtn = tk.Button(text="Connect", width=10, command=connect, bg=DARK_GREY)
connectBtn.place(x=220, y=137)

input_user = tk.StringVar()
input_field = tk.Entry(text=input_user, highlightthickness=2, highlightbackground="white", bd=0, width=32)
input_field.place(x=15, y=587)

textCons = tk.Text(window, width=48, height=22, bd=0, wrap="word", spacing1=5, padx=15,
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
                    filename = msg["content"]["filename"]
                    fileext = msg["content"]["fileext"]
                    text_cons = date + " " + username + ": sent file " + filename + "." + fileext
                    textCons.config(state=tk.NORMAL)
                    textCons.insert(tk.END, text_cons + "\n")
                    textCons.config(state=tk.DISABLED)
                    textCons.see(tk.END)
                elif type == "text":
                    data = msg["content"]["data"]
                    text_cons = date + " " + username + ": " + data
                    textCons.config(state=tk.NORMAL)
                    textCons.insert(tk.END, text_cons + "\n")
                    textCons.config(state=tk.DISABLED)
                    textCons.see(tk.END)
            except:
                pass


def send_msg(input_get):
    msg_web = dweepy.dweet_for(CHAT_ID, {'username': USERNAME, 'type': 'text', 'data': input_get})
    try:
        date = msg_web["created"][12:17]
        return date + " " + USERNAME + ": " + input_get
    except:
        return ""


def send_text():
    input_get = str(input_field.get())
    if not input_get.isspace() and input_get != "":
        text_cons = send_msg(input_get)
        # if text_cons != "":
        #     textCons.config(state=tk.NORMAL)
        #     textCons.insert(tk.END, text_cons + "\n")
        #     textCons.config(state=tk.DISABLED)
        #     textCons.see(tk.END)
    input_user.set("")
    return "break"


def send_file(file_path):
    pass


sendBtn = tk.Button(text="Send", width=6, command=send_text)
sendBtn.place(x=325, y=587)


def loop():
    window.mainloop()


def check_updates():
    while CHAT_ID == "":
        pass
    for dweet in dweepy.listen_for_dweets_from(CHAT_ID):
        try:
            date = dweet["created"][12:17]
            type = dweet["content"]["type"]
            username = dweet["content"]["username"]
            if type == "text":
                data = dweet["content"]["data"]
                text_cons = date + " " + username + ": " + data
                textCons.config(state=tk.NORMAL)
                textCons.insert(tk.END, text_cons + "\n")
                textCons.config(state=tk.DISABLED)
                textCons.see(tk.END)
            elif type == "file":
                pass
        except:
            pass


mainloop = threading.Thread(target=loop)
updates = threading.Thread(target=check_updates)

mainloop.start()
updates.start()
