
# Scrapes an npr.org show page and creates a CSV file playlist of all the music interludes.
# only works one page at a time at the moment which you must pass as an argument
# example $> python youtubePlaylistMaker.py https://www.npr.org/programs/morning-edition/2018/12/06/674001736/morning-edition-for-december-6-2018?showDate=2018-12-06
# Author: Adam Harris
# Date 11/27/2018


#   How it do...
# 1. Open a particular NPR show archive page and Scrape the music tags from the HTML to get artist and song names
# 2. Sanitize (remove special characters) Reference: https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
# 3. Search youtube for each artist/song and grab first result
# 4. Create custom shareable temporary youtube playlist with top results


# Most of this code is referenced form :https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
# and https://codeburst.io/scraper-b82146396249

# import libraries
import urllib2
from bs4 import BeautifulSoup
import requests
import re
from sys import argv  # used for catching arguments on the command line

# specify the url
quote_page = str(argv[1]) #argument should be morning edition episode webpage.

# query the website and return the html to the variable "page"
page = urllib2.urlopen(quote_page)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, "html.parser")

#reference: https://stackoverflow.com/questions/48484463/how-to-python-scrape-text-in-span-class 

# GET Band Names
bands = []
for band in soup.find_all ('span', {'class': 'song-meta-artist'}):
    bands.append(re.sub('[^\w\s]','',band.text))

titles = []
for title in soup.find_all ('span', {'class': 'song-meta-title'}):
    titles.append(re.sub('[^\w\s]','',title.text))# Sanitize (remove special characters) Reference: https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string

# 4. Search youtube for each artist/song and grab first result

# Make youtube playlists without logging in using just URLs
# Reference: https://www.labnol.org/internet/create-youtube-playlists/28827/
url = "https://www.youtube.com/results?search_query="

playlistUrl = 'http://www.youtube.com/watch_videos?video_ids='
for index, item in enumerate(bands):  #go through each song/band and search youtube for the first result
   # print bands[index] +' '+ titles[index]
    r = requests.get(url+bands[index] +' '+ titles[index])
    html = r.text
    soup=BeautifulSoup(html,'html.parser')
    vid = soup.find('a',attrs={'class':'yt-uix-tile-link'})  # get all the <a> tags from the html
# 5. Create custom shareable temporary youtube playlist with top results for each song
   # print vid
    playlistUrl += vid['href'][9:]+',' #Strip off the "/watch?v=" from the link and add a comma to form a list


print playlistUrl.rstrip(',') #remove the last comma since I did no check for it in the list to speed it up

