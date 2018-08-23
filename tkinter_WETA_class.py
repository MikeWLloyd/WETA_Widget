#https://stackoverflow.com/questions/38229857/how-to-avoid-attributeerror-tkinter-tkapp-object-has-no-attribute-passcheck
#https://stackoverflow.com/questions/2400262/how-to-create-a-timer-using-tkinter
#https://tkdocs.com/tutorial/firstexample.html#code
#http://effbot.org/tkinterbook/

#from Tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import datetime
import re
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

    def create_window(self):
        self.window = tk.Toplevel(root)
        x = (root.winfo_x()+root.winfo_width()+10)
        y = root.winfo_y()
        self.window.resizable(width=False, height=False)
        self.window.geometry("+%d+%d" % (x, y))
        #create the window and move it to not overlap with the root window.

        todays_list = WETA.today_playlist(full_playlist)
        #get todays playlist

        self.exit = tk.Button(self.window, text="Close Window", command=self.window.destroy)
        self.list = ScrolledText(self.window,width=125,height=50,wrap=tk.WORD)
        #widget makers

        self.list.configure(state='normal')
        for track in todays_list:
            printout='%s : %s composed by, %s\n' % (track[2],track[0],track[1])
            self.list.insert(tk.INSERT, printout)
        self.list.configure(state='disabled')    
        self.list.grid(column=0,row=3, columnspan=8, rowspan=1)
        #print out the playlist for the day, and locate the widget

        self.exit.grid(column=6, row=8)
        #exit button

    def search_composer(self):
        self.composer=tk.StringVar()
        self.found_print = tk.StringVar()
        self.found_print.set('Found __ entries in todays playlist for __')

        todays_list = WETA.today_playlist(full_playlist)
        
        def find_composer(*args):
            composer = self.composer.get()
            print_composer = composer
            composer = re.compile(composer.upper())

            self.results.configure(state='normal')
            self.results.delete(1.0,tk.END)
            found = 0
            count = 0
            for track in todays_list:
                if  composer.search(track[1].upper()):
                    #print("Found it", track)
                    printout='%s : %s\t: %s\n' % (track[2],track[0],track[1])
                    self.results.configure(state='normal')
                    self.results.insert(tk.INSERT, printout)
                    self.results.configure(state='disabled')
                    found = 1
                    count += 1
            if found==0:
                self.results.configure(state='normal')
                self.results.insert(tk.INSERT, 'Did not find "%s"\n' % print_composer)
                self.results.configure(state='disabled')
            self.found_print.set('Found %s entries in todays playlist for %s' % (count,print_composer))
        #function for finding the searched for composer

        self.comp = tk.Toplevel(root)
        x = root.winfo_x()
        y = (root.winfo_y()+root.winfo_height()+30)
        self.comp.resizable(width=False, height=False)
        self.comp.geometry("+%d+%d" % (x, y))
        #create the window and move it to not overlap with the root window.

        self.comp_entry = tk.Entry(self.comp, width=7, textvariable=self.composer).grid(column=1, row=1, sticky=tk.E)
        tk.Label(self.comp, text='Composer Name (first/last/partial)').grid(column=2, row=1, sticky=tk.W)

        tk.Label(self.comp, textvariable=self.found_print).grid(column=1, row=6)

        self.results = ScrolledText(self.comp,width=90,height=5,wrap=tk.WORD)
        self.results.grid(column=0,row=3, columnspan=6, rowspan=1)
        self.find_comp = tk.Button(self.comp, text="Find", command=find_composer).grid(column=3, row=1, sticky=tk.E)
        self.exit = tk.Button(self.comp, text="Close Window", command=self.comp.destroy).grid(column=2, row=6)
        #widget makers and placement

    def createWidgets(self):
        self.txt = tk.Text(self,width=65,height=7,background='snow2')
        #width and height is number of charecters or carriage returns. 
        self.exit = tk.Button(self, text="Quit", command=root.destroy).grid(column=6, row=6, sticky=tk.E)
        self.playlist = tk.Button(self, text="Full Playlist", command=self.create_window).grid(column=6, row=2, sticky=tk.W)
        self.composer_find = tk.Button(self, text="Find Composer", command=self.search_composer).grid(column=5, row=2, sticky=tk.W)
        #generate widgets

        self.txt.insert(tk.INSERT, cur_printout)
        self.txt.insert(tk.INSERT, '\n\n')
        self.txt.insert(tk.INSERT, next_printout)
        self.txt.grid(column=0,row=3, columnspan=8, rowspan=1)
        tk.Label(self, text=("Current time is: %s (updated every 10s)" % current_time)).grid(column=0, row=6)
        #print the current song and the next song and place the widget

        self.onUpdate()
        #loop into the auto-update function

    def onUpdate(self):
        time=get_time()
        
        self.txt.configure(state='normal')
        self.txt.delete(1.0,tk.END)
        cur_piece, cur_composer, cur_piece_time, next_time, next_piece, next_composer = WETA.current_track(full_playlist, time)
        cur_printout, next_printout = refresh_piece(cur_piece, cur_composer, cur_piece_time, next_time, next_piece, next_composer)
        self.txt.insert(tk.INSERT, cur_printout)
        self.txt.insert(tk.INSERT, '\n\n')
        self.txt.insert(tk.INSERT, next_printout)
        self.txt.configure(state='disabled')
        #update the text to the current time. There is a slight lag here once the time changes, it take a bit for the piece to catch up...might need to look at that.

        tk.Label(self, text=("Current time is: %s (updated every 10s)" % time)).grid(column=0, row=6)
        #update the current time

        self.after(10000, self.onUpdate)
        #do this every ~10 seconds

if __name__ == "__main__":

    full_playlist = WETA.getpage()
    
    current_time=get_time()
    cur_piece, cur_composer, cur_piece_time, next_time, next_piece, next_composer = WETA.current_track(full_playlist, current_time)
    cur_printout, next_printout = refresh_piece(cur_piece, cur_composer, cur_piece_time, next_time, next_piece, next_composer)

    root = tk.Tk()
    root.title("WETA Playlist")
    root.resizable(width=False, height=False)
    app = Application(master=root)
    root.mainloop()