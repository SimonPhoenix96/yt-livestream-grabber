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
streamlink_initiated = False

# UNIQUE LIVE INDICATION THAT USER IS LIVE YT CHANGES THIS I THINK
# {"text":"Live"}
# {"iconType":"LIVE"}
for i in range(0, len(spec)):
    if (str(spec).find('{"text":"Live"}') + str(spec).find('{"iconType":"LIVE"}') != -2):
        live = True
        break
if os.path.isfile(stream_folder + username + "_LIVE") == False:

    if live:

        msg_streamer_live = username + " is live!"

        live_video_page = s.get('https://www.youtube.com/channel/' + channel + '/live')
        live_video_page_soup = BeautifulSoup(live_video_page.text, 'html.parser')
        filename = live_video_page_soup.find_all("title")[0].text.replace(" - YouTube" , "").replace("/", "_")

        potential_link = live_video_page_soup.find_all("link")

        for indice in potential_link:
            if indice['href'].find('watch?v=') != -1:
                # add index where teaser html attribute starts to index where specific thread id starts
                live_video_link = indice['href']
                break
        


        f = open(stream_folder + username + "_LIVE", "w")
        f.close()
        streamlink_initiated = True

        command = '/usr/bin/streamlink --force --hls-live-restart -o "' + stream_folder + filename + '.ts" "' + live_video_link + '" 720p'

        subprocess.Popen(command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        print(msg_streamer_live)
    else:
        print(username + " is not live!")

if live != True and os.path.isfile(stream_folder + username + "_LIVE"):
    print(username + " is not live so delete LIVE Marker file!")
    os.remove(stream_folder + username + "_LIVE")

if streamlink_initiated == False and live == True and os.path.isfile(stream_folder + username + "_LIVE"):
    print(username + "'s stream is currently being downloaded!")
