# Open a particular NPR show archive page
# 1. Go back X number of days before today (they usually hold 5 shows per page)
# 2. Scrape the music tags from the HTML to get artist and song names
# 3. Sanitize (remove special characters) Reference: https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
# 4. Search youtube for each artist/song and grab first result
# 5. Create custom shareable temporary youtube playlist with top results



# 1. Go back X number of days before today (they usually hold 5 shows per page)
# 2. Scrape the music tags from the HTML to get artist and song names

#Scrapes an npr.org show page and creates a CSV file playlist of all the music interludes.
# https://www.npr.org/programs/morning-edition/archive
# Author: Adam Harris
# Date 11/27/2018
#

#now to crawl npr's pages creates a youtube platlist of music from the show for each week.

# Most of this code is referenced form :https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
# and https://codeburst.io/scraper-b82146396249

# import libraries
import urllib2
from bs4 import BeautifulSoup
import re #used for regex to strip special  chars from song and band names
from sys import argv  # used for catching arguments on the command line

#libs for infinite scrolling
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import requests
import unittest, time, re


testing = 1 # If this is set to 1 then it'll only print CSV list of band and song names, setting to any other value queries youtube and creates the playlists.



def scraper(linkToScrape):
    html_source = driver.page_source
    page = html_source.encode('utf-8')
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
    if testing ==1:
        playlistUrl =''
    else:
        splaylistUrl = 'http://www.youtube.com/watch_videos?video_ids='
    for index, item in enumerate(bands):  #go through each song/band and search youtube for the first result

        if testing ==1:  #just testing, only print names of bands and songs
           playlistUrl += bands[index] +','+ titles[index]+'\n'
           
        else: #otherwise query youtube and build the full youtube list.
            r = requests.get(url+bands[index] +' '+ titles[index])
            html = r.text
            soup=bs(html,'html.parser')
            vid = soup.find('a',attrs={'class':'yt-uix-tile-link'})  # get all the <a> tags from the html
    # 5. Create custom shareable temporary youtube playlist with top results for each song
            playlistUrl += vid['href'][9:]+',' #Strip off the "/watch?v=" from the link and add a comma to form a list

    print playlistUrl.rstrip(',') #remove the last comma since I did no check for it in the list to speed it up    






# ==================  Main code below  ====================


#Step 2: Get a ordered list of artists and song titles

#Use chromedriver to load autoscrolling NPR archive page
driver = webdriver.Chrome(executable_path=r'chromedriver') #basic non-headless chrome driver
driver.implicitly_wait(30)
base_url = "https://www.npr.org/programs/morning-edition/archive"
verificationErrors = []
accept_next_alert = True


#delay = 3
driver.get(base_url) #actually open the mainpage here

if len(argv)<2:
    scrollTimes = 1
else:
    scrollTimes = int(argv[1])

for i in range(1,scrollTimes):# scroll down X times
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

#now that this has scrolled to the appropriate amount, open all the "more from this episode" links:
links = driver.find_elements_by_xpath('//article/section/a')#get all links to "more from this episode"
linksBuffer = links
#print 'got all the links'
for index, link in enumerate(linksBuffer):
    newLink = link.get_attribute('href')
    #print 'visiting link '+newLink
    driver.execute_script('window.open('');')
    time.sleep(1)
    #print 'switching to window'
    #print index+1
    driver.switch_to.window(driver.window_handles[index+1])
#here's where we should call the scraper function
    driver.get(newLink) #loads the new page into driver
    scraper(newLink) #pass the new link to the scraper
    #print 'Switch Successful, going back to base URL'
    driver.switch_to.window(driver.window_handles[0])



# kill the chrome window and release from memory:
driver.stop_client()
driver.close() #closes chromedriver browser window
driver.quit() #removes chromedriver cmd window
