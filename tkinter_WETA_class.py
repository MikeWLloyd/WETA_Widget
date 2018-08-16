#https://stackoverflow.com/questions/38229857/how-to-avoid-attributeerror-tkinter-tkapp-object-has-no-attribute-passcheck
#https://stackoverflow.com/questions/2400262/how-to-create-a-timer-using-tkinter

#from Tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import datetime
import WETA


def get_time():
    return datetime.datetime.now().strftime('%H:%M')
def refresh_piece(cur_piece, cur_composer, cur_piece_time, next_time, next_piece, next_composer):
    cur_printout = ('The current piece: %s\nComposed by: %s\nStarted at %s and will end at %s' % (cur_piece, cur_composer, cur_piece_time, next_time))
    next_printout = ('The next piece is: %s\nComposed by: %s\nWill start at %s' % (next_piece, next_composer, next_time))
    return(cur_printout, next_printout)



class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    # def clicked(self):
    #     time=get_time()
    #     self.txt.delete(1.0,tk.END)
    #     cur_piece, cur_composer, cur_piece_time, next_time, next_piece, next_composer = WETA.current_track(full_playlist, time)
    #     cur_printout, next_printout = refresh_piece(cur_piece, cur_composer, cur_piece_time, next_time, next_piece, next_composer)
    #     self.txt.insert(tk.INSERT, cur_printout)
    #     self.txt.insert(tk.INSERT, '\n\n')
    #     self.txt.insert(tk.INSERT, next_printout)
    #     tk.Label(self, text=("Current time is: %s" % time)).grid(column=0, row=6)
    # Uncomment to turn on the refresh button functionality; however, this is not needed given the 'onUpdate' function below. 

    def createWidgets(self):
        self.txt = ScrolledText(self,width=65,height=10)
        #self.ok = tk.Button(self, text="Refresh", command=self.clicked)
        #uncomment to turn on the "refresh" button
        self.cancel = tk.Button(self, text="Quit", command=root.destroy)

        self.txt.insert(tk.INSERT, cur_printout)
        self.txt.insert(tk.INSERT, '\n\n')
        self.txt.insert(tk.INSERT, next_printout)
        self.txt.grid(column=0,row=3, columnspan=8, rowspan=1)
        tk.Label(self, text=("Current time is: %s (updated every 10s)" % current_time)).grid(column=0, row=6)
        #self.ok.grid(column=3, row=6)
        #uncomment to turn on the "refresh" button
        self.cancel.grid(column=6, row=6)

        self.onUpdate()

    def onUpdate(self):
        time=get_time()
        self.txt.delete(1.0,tk.END)
        cur_piece, cur_composer, cur_piece_time, next_time, next_piece, next_composer = WETA.current_track(full_playlist, time)
        cur_printout, next_printout = refresh_piece(cur_piece, cur_composer, cur_piece_time, next_time, next_piece, next_composer)
        self.txt.insert(tk.INSERT, cur_printout)
        self.txt.insert(tk.INSERT, '\n\n')
        self.txt.insert(tk.INSERT, next_printout)
        tk.Label(self, text=("Current time is: %s (updated every 10s)" % time)).grid(column=0, row=6)

        self.after(10000, self.onUpdate)

if __name__ == "__main__":

    full_playlist = WETA.getpage()
    
    current_time=get_time()
    cur_piece, cur_composer, cur_piece_time, next_time, next_piece, next_composer = WETA.current_track(full_playlist, current_time)
    cur_printout, next_printout = refresh_piece(cur_piece, cur_composer, cur_piece_time, next_time, next_piece, next_composer)

    root = tk.Tk()
    root.title("WETA Playlist")
    app = Application(master=root)
    root.mainloop()


# import tkinter as tk
# import time

# def current_iso8601():
#     """Get current date and time in ISO8601"""
#     # https://en.wikipedia.org/wiki/ISO_8601
#     # https://xkcd.com/1179/
#     return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

# class Application(tk.Frame):
#     def __init__(self, master=None):
#         tk.Frame.__init__(self, master)
#         self.pack()
#         self.createWidgets()

#     def createWidgets(self):
#         self.now = tk.StringVar()
#         self.time = tk.Label(self, font=('Helvetica', 24))
#         self.time.pack(side="top")
#         self.time["textvariable"] = self.now

#         self.QUIT = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
#         self.QUIT.pack(side="bottom")

#         # initial time display
#         self.onUpdate()

#     def onUpdate(self):
#         # update displayed time
#         self.now.set(current_iso8601())
#         # schedule timer to call myself after 1 second
#         self.after(1000, self.onUpdate)

# root = tk.Tk()
# app = Application(master=root)
# root.mainloop()