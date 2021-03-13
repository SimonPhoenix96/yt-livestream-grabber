from bs4 import BeautifulSoup
import requests
import subprocess
import sys
import os
from re import sub, finditer
from datetime import datetime

channel = sys.argv[1]
username = sys.argv[2]
stream_folder = sys.argv[3]
filename = channel + "_" + str(datetime.now().today()).replace(" ", "_")
live_video_link = " "
url = "https://www.youtube.com/channel/" + channel

s = requests.session()
page = s.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
spec = soup.find_all("script")

live = False

# SHOWS THAT USER IS LIVE YTT CHANGES THIS I THINK
# {"text":"LIVE"}
# {"iconType":"LIVE"}
for i in range(0, len(spec)):
    # print(str(spec[i]))
    # print(str(spec[i].find('{"iconType":"LIVE"}')))
    if (str(spec[i]).find('{"iconType":"LIVE"}') or str(spec[i]).find('{"iconType":"LIVE"}')) != -1: 
        live = True
        break

if os.path.isfile(stream_folder + username + "_LIVE") == False:

    if live:
        
        print(username + " is live!")
        
        live_video_page = s.get('https://www.youtube.com/channel/' + channel + '/live')
        live_video_page_soup = BeautifulSoup(live_video_page.text, 'html.parser')
        filename = live_video_page_soup.find_all("title")[0].text.replace(" - YouTube" , "")  
        
        # print(filename[0].text)

        potential_link = live_video_page_soup.find_all("link")
        # print(str(live_video_id).find("https://www.youtube.com/watch?v="))

        for indice in potential_link:
            # print(indice['href'])
            if indice['href'].find('watch?v=') != -1: 
                # add index where teaser html attribute starts to index where specific thread id starts
                live_video_link = indice['href']
                break
        # print(filename + " " + live_video_link)    
        #command = '"/usr/bin/streamlink ' + '--hls-live-restart ' + '-o "' +  stream_folder + 'carliii' + '.ts" "' + live_video_link + '" best"'
        #filename
#        print(str(command))
        command = '/usr/bin/streamlink -Q  --hls-live-restart -o "' + stream_folder + filename + '.ts" "' + live_video_link + '" best'
        subprocess.run(command, shell=True)
#        print(str(command))
        f = open(stream_folder + username + "_LIVE", "w")
        f.close()
    else: 
        print(username + " is not live!")    

if live != True and os.path.isfile(stream_folder + username + "_LIVE"):
    print(username + " is not live so delete LIVE Marker file!")
    os.remove(stream_folder + username + "_LIVE")

if live == True and os.path.isfile(stream_folder + username + "_LIVE"):
    print(username + "'s stream is currently being downloaded!")
