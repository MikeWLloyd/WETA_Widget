# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime

#print datetime.datetime.now().strftime('%I:%M %p')
# 12 hour clock
#print datetime.datetime.now().strftime('%H:%M')
# 24 hour clock. 

def current_track(main_data, current_time):

    for start_time in main_data:
        time_only = start_time.find('div', attrs={'class':'field-start-time'})
        time = time_only.text.strip()

        #datetime_object = datetime.datetime.strptime(time, '%I:%M %p').strftime('%I:%M %p')
        datetime_object = datetime.datetime.strptime(time, '%I:%M %p').strftime('%H:%M')
        

        if datetime_object >= current_time:
            next_time =  datetime.datetime.strptime(datetime_object, '%H:%M').strftime('%I:%M %p')

            #current track
            composer_find = last_entry.find('div', attrs={'class':'field-composer'})
            cur_composer = composer_find.text.strip()

            piece_find = last_entry.find('h4')
            cur_piece = piece_find.text.strip()
            
            time_only = last_entry.find('div', attrs={'class':'field-start-time'})
            time = time_only.text.strip()
            cur_piece_time = datetime.datetime.strptime(time, '%I:%M %p').strftime('%I:%M %p')
            
            #print('The current piece: %s composed by %s started at %s and will end at %s' % (cur_piece, cur_composer, cur_piece_time, next_time))

            #next track
            composer_find = start_time.find('div', attrs={'class':'field-composer'})
            next_composer = composer_find.text.strip()
            
            piece_find = start_time.find('h4')
            next_piece = piece_find.text.strip()

            #print('The next piece is: %s composed by %s will start at %s' % (next_piece, next_composer, next_time))

            return(cur_piece, cur_composer, cur_piece_time, next_time, next_piece, next_composer)
            
            break

        last_entry = start_time

def getpage():
    

    # specify the url
    quote_page = 'https://weta.org/fm/playlists'

    # query the website and return the html to the variable page
    page = urlopen(quote_page)

    # parse the html using beautiful soup and store in variable soup
    soup = BeautifulSoup(page, 'html.parser')

    # get the index start-time
    main_data = soup.findAll('div', attrs={'class':'ds-1col node node-fm-playlist node-promoted view-mode-full clearfix'})

    return(main_data)


if __name__ == "__main__":
    current_time = datetime.datetime.now().strftime('%H:%M')
    full_playlist = getpage()
    current_track(full_playlist, current_time)

# time = '11:54 pm'
# datetime_object = datetime.datetime.strptime(time, '%I:%M %p').strftime('%I:%M %p')

# print(datetime_object)



# from bs4 import BeautifulSoup
# doc = ['<html><head><title>Page title</title></head>',
#        '<body><p id="firstpara" align="center">This is paragraph <b>one</b>.',
#        '<p id="secondpara" align="blah">This is paragraph <b>two</b>.',
#        '</html>']
# soup = BeautifulSoup(''.join(doc))
# print soup.prettify()


# bTag = soup.find('b')

# [tag.name for tag in bTag.findParents()]
# # [u'p', u'body', u'html', '[document]']
# # NOTE: "u'[document]'" means that that the parser object itself matched.

# bTag.findParent('body').name
# u'body'

# <html>
#  <head>
#   <title>
#    Page title
#   </title>
#  </head>
#  <body>
#   <p id="firstpara" align="center">
#    This is paragraph
#    <b>
#     one
#    </b>
#    .
#   </p>
#   <p id="secondpara" align="blah">
#    This is paragraph
#    <b>
#     two
#    </b>
#    .
#   </p>
#  </body>
# </html>