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

# scrape immediately
fhand = urllib.request.urlopen(dn, context = ctx) #fhand = open('dnpracticefile.html')
file = fhand.read() #decode if necessary
x = BeautifulSoup(file, 'html.parser').find('ul', class_= 'compArticleList') #the object 'x' is a sorted/parsed subset of the html file with only the articles
articles = x('a') #a list of tags containing article titles and links
date = x('span') #a list of tags containing time that articles are last updated
#create dataframe of titles, links, dates
titles = []
links = []
dates = []
timeCollected = []
for tag in articles:
    y = tag.get('class', None)
    if isinstance(y, list) == True:
        if 'thmb' in y[0]:
            titles.append(tag.get('title', None))
            links.append(tag.get('href', None))
        else: continue
    else: continue
for tag in date:
    dates.append(tag.contents[0])
    timeCollected.append(str(datetime.datetime.now()))
d = {'Titles': titles, 'Links': links, 'Dates': dates, 'Time Collected': timeCollected}
df = pd.DataFrame(d)
#write results into an excel file
df.to_excel("dn.xlsx", sheet_name="sheet", index=False)
print(df)
print('DN is scraped at:', datetime.datetime.now())

# scrape every 10 seconds after this
sched = BlockingScheduler()
@sched.scheduled_job('interval', minutes=15)
def timed_job():
    fhand = urllib.request.urlopen(dn, context = ctx) #fhand = open('dnpracticefile.html')    
    file = fhand.read() #decode if necessary
    x = BeautifulSoup(file, 'html.parser').find('ul', class_= 'compArticleList') #the object 'x' is a sorted/parsed subset of the html file with only the articles
    articles = x('a') #a list of tags containing article titles and links
    date = x('span') #a list of tags containing time that articles are last updated

    titles = []
    links = []
    dates = []
    timeCollected = []
    for tag in articles:
        y = tag.get('class', None)
        if isinstance(y, list) == True:
            if 'thmb' in y[0]:
                titles.append(tag.get('title', None))
                links.append(tag.get('href', None))
            else: continue
        else: continue
    for tag in date:
        dates.append(tag.contents[0])
        timeCollected.append(str(datetime.datetime.now()))
    d = {'Titles': titles, 'Links': links, 'Dates': dates, 'Time Collected': timeCollected}
    df2 = pd.DataFrame(d)
    print(df2)
    scrapes = pd.read_excel('dn.xlsx', sheet_name='sheet1')
    df3 = pd.concat([scrapes,df2])
    #print(df3)
    #write results into an excel file
    df3.to_excel("dn.xlsx", sheet_name="sheet", index=False)
    print('DN is scraped at:', datetime.datetime.now())
sched.start()