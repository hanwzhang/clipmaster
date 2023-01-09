#libraries
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

#ignore SSL certificate errors, setting up url
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
dn = 'https://nydailynews.search.yahoo.com/search?p=adams'

# scrape every 20 seconds
sched = BlockingScheduler()
@sched.scheduled_job('interval', seconds=20)
def timed_job():

    fhand = urllib.request.urlopen(dn, context = ctx) #similar to fhand = open('...') for a local file
    file = fhand.read() #decode if necessary
    x = BeautifulSoup(file, 'html.parser') #the object 'x' is a sorted/parsed version of the html file
    anchortags = x('a') #a list of anchortags

    #create dataframe of titles and links
    titles = []
    links = []
    for tag in anchortags:
        y = tag.get('class', None)
        if isinstance(y, list) == True:
            if 'thmb' in y[0]:
                titles.append(tag.get('title', None))
                links.append(tag.get('href', None))
            else: continue
        else: continue
    d = {'Titles': titles, 'Links': links}
    df = pd.DataFrame(d)

    #write results into an excel file
    df.to_excel("dn_"+str(datetime.datetime.now())+".xlsx", sheet_name="sheet", index=False)
    print('DN is scraped at:', datetime.datetime.now())
sched.start()
