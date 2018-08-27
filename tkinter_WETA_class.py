#https://stackoverflow.com/questions/38229857/how-to-avoid-attributeerror-tkinter-tkapp-object-has-no-attribute-passcheck
#https://stackoverflow.com/questions/2400262/how-to-create-a-timer-using-tkinter
#https://tkdocs.com/tutorial/firstexample.html#code
#http://effbot.org/tkinterbook/

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import datetime
import re
import unicodedata
import WETA

def get_time():
    return datetime.datetime.now().strftime('%H:%M')
def refresh_piece(cur_piece, cur_composer, cur_piece_time, next_time, next_piece, next_composer):
    cur_printout = ('The current piece: %s\nComposed by: %s\nStarted at %s and will end at %s' % (cur_piece, cur_composer, cur_piece_time, next_time))
    next_printout = ('The next piece is: %s\nComposed by: %s\nWill start at %s' % (next_piece, next_composer, next_time))
    return(cur_printout, next_printout)
def strip_accents(text):
    #https://stackoverflow.com/questions/44431730/how-to-replace-accented-characters-in-python
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.comp = None
        self.datedlist = None
        self.window = None
        self.createWidgets()

    def createWidgets(self):
        self.playlist = tk.Button(self, text="Today's Playlist", command=self.display_playlist).grid(column=2, row=1)
        self.dateplaylist = tk.Button(self, text="Playlist Lookup", command=self.dated_playlist).grid(column=2, row=2)
        self.composer_find = tk.Button(self, text="Find Composer", command=self.search_composer).grid(column=1, row=1)
        self.exit = tk.Button(self, text="Quit", command=root.destroy).grid(column=3, row=6, sticky=tk.E)

        self.txt = tk.Text(self,width=65,height=7,background='snow2',wrap=tk.WORD)
        #width and height is number of charecters or carriage returns. 
        self.txt.insert(tk.INSERT, cur_printout)
        self.txt.insert(tk.INSERT, '\n\n')
        self.txt.insert(tk.INSERT, next_printout)
        self.txt.grid(column=0,row=3, columnspan=8, rowspan=1)
        tk.Label(self, text=("Current time is: %s (updated every 10s)" % current_time)).grid(column=1, row=6)
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

        tk.Label(self, text=("Current time is: %s (updated every 10s)" % time)).grid(column=1, row=6)
        #update the current time

        self.after(10000, self.onUpdate)
        #do this every ~10 seconds

    def display_playlist(self):
        if self.window == None or not tk.Toplevel.winfo_exists(self.window):
        #checks if the window exists. If it does, don't open another one. 
        #https://stackoverflow.com/questions/45066228/open-tkniter-toplevel-only-if-it-doesnt-already-exist
            self.window = tk.Toplevel(root)
            self.window.title("Today's Playlist")
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
            if composer == '':
                self.results.configure(state='normal')
                self.results.delete(1.0,tk.END)
                self.results.insert(tk.INSERT, 'Search box empty. No results to display')
                self.results.configure(state='disabled')
                return
            print_composer = composer
            composer = re.compile(composer.upper())
            #this is what we are searching for

            self.results.configure(state='normal')
            self.results.delete(1.0,tk.END)
            found = 0
            count = 0
            #clear the pannel and reset counts/tracker

            for track in todays_list:
                clean_name = strip_accents(track[1])
                #clean off accents to make matching easier. 
                if  composer.search(clean_name.upper()):
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
        #function for finding the composer

        if self.comp == None or not tk.Toplevel.winfo_exists(self.comp):
            #checks if the window exists. If it does, don't open another one. 
            self.comp = tk.Toplevel(root)    
            self.comp.title("Composer Lookup")
            x = root.winfo_x()
            y = (root.winfo_y()+root.winfo_height()+30)
            self.comp.resizable(width=False, height=False)
            self.comp.geometry("+%d+%d" % (x, y))
            #create the window and move it to not overlap with the root window.
            self.comp.bind('<Return>', find_composer)
            self.grid()

        self.comp_entry = tk.Entry(self.comp, width=7, textvariable=self.composer).grid(column=1, row=1, sticky=tk.E)
        tk.Label(self.comp, text='Composer Name (first/last/partial)').grid(column=2, row=1, sticky=tk.W)
        self.find_comp = tk.Button(self.comp, text="Find", command=find_composer).grid(column=3, row=1, sticky=tk.E)
        
        self.results = ScrolledText(self.comp,width=90,height=5,wrap=tk.WORD)
        self.results.grid(column=0,row=3, columnspan=6, rowspan=1)
        tk.Label(self.comp, textvariable=self.found_print).grid(column=1, row=6)

        self.exit = tk.Button(self.comp, text="Close Window", command=self.comp.destroy).grid(column=2, row=6)
        #widget makers and placement

    def dated_playlist(self):
        self.date=tk.StringVar()
      
        def get_date_playlist(*args):
            date = self.date.get()
            if date == '':
                self.datelist.configure(state='normal')
                self.datelist.delete(1.0,tk.END)
                self.datelist.insert(tk.INSERT, 'Search box empty. No results to display')
                self.datelist.configure(state='disabled')
                return
            try:
                datetime.datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                self.datelist.configure(state='normal')
                self.datelist.delete(1.0,tk.END)
                self.datelist.insert(tk.INSERT, 'Incorrect data format, should be YYYY-MM-DD')
                self.datelist.configure(state='disabled')
                return
            #https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python

            datedata = WETA.getpagefordate(date)
            date_playlist = WETA.today_playlist(datedata)
            self.datelist.configure(state='normal')
            self.datelist.delete(1.0,tk.END)
            for track in date_playlist:
                printout='%s : %s composed by, %s\n' % (track[2],track[0],track[1])
                self.datelist.insert(tk.INSERT, printout)
            self.datelist.configure(state='disabled')    

        if self.datedlist == None or not tk.Toplevel.winfo_exists(self.datedlist):
            self.datedlist = tk.Toplevel(root)
            self.datedlist.title("Playlist Lookup")
            x = (root.winfo_x()+root.winfo_width()+10)
            y = root.winfo_y()
            self.datedlist.resizable(width=False, height=False)
            self.datedlist.geometry("+%d+%d" % (x, y))
            self.datedlist.bind('<Return>', get_date_playlist)
        #create the window and move it to not overlap with the root window.

        self.exit = tk.Button(self.datedlist, text="Close Window", command=self.datedlist.destroy)
        self.datelist = ScrolledText(self.datedlist,width=125,height=50,wrap=tk.WORD)
        self.datelist.grid(column=0,row=3, columnspan=8, rowspan=1)
        #widget maker

        self.comp_entry = tk.Entry(self.datedlist, width=7, textvariable=self.date).grid(column=1, row=1, sticky=tk.E)
        tk.Label(self.datedlist, text='Date (e.g., 2018-08-23)').grid(column=2, row=1, sticky=tk.W)
        self.find_comp = tk.Button(self.datedlist, text="Find", command=get_date_playlist).grid(column=3, row=1, sticky=tk.E)
        #### NEED TO CATCH IF THIS IS EMPTY OR IN THE WRONG FORMAT...

        self.exit.grid(column=6, row=8)
        #exit button


if __name__ == "__main__":
    full_playlist = WETA.getpage()
    
    current_time=get_time()
    cur_piece, cur_composer, cur_piece_time, next_time, next_piece, next_composer = WETA.current_track(full_playlist, current_time)
    cur_printout, next_printout = refresh_piece(cur_piece, cur_composer, cur_piece_time, next_time, next_piece, next_composer)

    root = tk.Tk()
    root.title("WETA Information")
    root.resizable(width=False, height=False)
    app = Application(master=root)
    root.mainloop()