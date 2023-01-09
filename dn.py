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

# ** try creating df outside the scheduler and adding scraped data to the df

# scrape every 20 seconds
sched = BlockingScheduler()
@sched.scheduled_job('interval', seconds=20)
def timed_job():

    fhand = urllib.request.urlopen(dn, context = ctx) #similar to fhand = open('...') for a local file
    file = fhand.read() #decode if necessary
    x = BeautifulSoup(file, 'html.parser').find('ul', class_= 'compArticleList') #the object 'x' is a sorted/parsed subset of the html file with only the articles
    articles = x('a') #a list of tags containing article titles and links
    times = x('span') #a list of tags containing time that articles are last updated

    #create dataframe of titles, links, dates
    titles = []
    links = []
    dates = []
    for tag in articles:
        y = tag.get('class', None)
        if isinstance(y, list) == True:
            if 'thmb' in y[0]:
                titles.append(tag.get('title', None))
                links.append(tag.get('href', None))
            else: continue
        else: continue
    for tag in times:
        dates.append(tag.contents[0])
    d = {'Titles': titles, 'Links': links, 'Dates': dates}
    df = pd.DataFrame(d)

    #write results into an excel file
    #df.to_excel("dn_"+str(datetime.datetime.now())+".xlsx", sheet_name="sheet", index=False)
    print(df)
    print('DN is scraped at:', datetime.datetime.now())
sched.start()
