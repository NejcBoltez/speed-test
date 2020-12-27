import os
import re
import subprocess
import time
import tkinter as tk
from tkinter import *
import requests 
class Window:
    def __init__(self):
        self.tk=tk.Tk()
        self.tk.configure(background='black')
        #self.tk.title("Pozdravljeni")
        #self.tk.geometry("100x100")
        self.tk.attributes('-fullscreen', True)  
        self.fullScreenState = False
        self.Frame=Frame(self.tk, background='Black')
        self.Frame.pack(fill=BOTH, expand=YES)
        self.NoInternet=Label(self.Frame, background="yellow")
        self.NoInternet.pack()
        self.Ping=Label(self.Frame,font=('Helvetica', 17), background='black', fg="white", text="\n\n\n\n\nPing Value  \n")
        self.Ping.pack(side = LEFT, fill=BOTH, expand = YES)
        self.Down=Label(self.Frame,font=('Helvetica', 17), background='black', fg="white", text="\n\n\n\n\nDownloand Value  \n")
        self.Down.pack(side = LEFT, fill=BOTH, expand = YES)
        self.Up=Label(self.Frame,font=('Helvetica', 17), background='black', fg="white", text="\n\n\n\n\nUpload Value  \n")
        self.Up.pack(side = LEFT, fill=BOTH, expand = YES)
        #self.getDivs()
        self.checkConnection()
    def checkConnection(self):
        url = "https://www.google.si/"
        timeout = 5
        self.NoInternet.config(text="Test internet connection.")
        try:
            request = requests.get(url, timeout=timeout)
            self.NoInternet.config(text="Connected to the Internet")
            self.getDivs()
        except (requests.ConnectionError, requests.Timeout) as exception:
            self.NoInternet.config(text="No internet connection.")
            self.Ping.config(text="\n\n\n\n\nPing Value   \n")
            self.Down.config(text="\n\n\n\n\nDownloand Value   \n")
            self.Up.config(text="\n\n\n\n\nUpload Value   \n")
            self.NoInternet.after(1000, self.checkConnection)# call every second. Tested on RPI3 B+ But you can easily adjust it on your specs.
        
    def getDivs(self):
        
        response = subprocess.Popen('/usr/local/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

        ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
        download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
        upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)
        
        ping = ping[0].replace(',', '.')
        download = download[0].replace(',', '.')
        upload = upload[0].replace(',', '.')
        #textPing=self.Ping.cget("text")
        self.Ping.config(text="\n\n\n\n\nPing Value  \n"+str(ping))
        self.Down.config(text="\n\n\n\n\nDownloand Value  \n"+str(download))
        self.Up.config(text="\n\n\n\n\nUpload Value  \n"+str(upload))
        self.Ping.after(30000, self.checkConnection) # call every 40 seconds. Tested on RPI3 B+ But you can easily adjust it on your specs.
       

monitor=Window()
monitor.tk.mainloop()
