# libraries
from bs4 import BeautifulSoup
from bs4.element import Comment
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# setup outlet shorthands
shorthand = {'nytimes.com':('NY TIMES','css-at9mc1 evys1bk0',[]),
'nypost.com':('NY POST', 'single__content entry-content m-bottom', ['single__inline-module alignleft','comments-inline-cta__wrap']),
'nymag.com':'NY MAGAZINE',
'nydailynews.com':'DAILY NEWS',
'politico.com':'POLITICO',
'wsj.com':'WSJ',
'bloomberg.com':'BLOOMBERG',
'washingtonpost.com':'WAPO',
'gothamist.com':'GOTHAMIST',
'silive.com':'SI ADVANCE',
'thecity.nyc':'THE CITY',
'amny.com':'AMNY',
'crainsnewyork.com':"CRAIN'S NY",
'gothamgazette.com':'GOTHAM GAZETTE',
'hellgatenyc.com':'HELL GATE',
'citylimits.org':'CITY LIMITS',
'ny.chalkbeat.org':'CHALKBEAT',
'nyc.streetsblog.org':'STREETSBLOG',
'cityandstateny.com':'CITY AND STATE',
'foxnews.com':'FOX'}

subject_shorthand = {'nytimes.com':'NYT',
'nypost.com':'NYP',
'nydailynews.com':'DN',
'nymag.com':'NY MAG'}

def get_website(link):
    site = link.split('https://')[-1].split('www.')[-1].split('/')[0]
    short = shorthand[site][0]
    contentIdentifier = shorthand[site][1]
    banList = shorthand[site][2]
    return short, contentIdentifier, banList

def tag_content(link, element):
    if element.parent.name not in ['p','span','a', 'h2']: judge = False
    else:
        allParentClasses = []
        for parent in element.parents:
            pClassL = parent.get('class')
            try: pClass = ' '.join(pClassL)
            except: pClass = 'NA'
            allParentClasses.append(pClass)
        #eClassL = element.parent.parent.get('class')
        if get_website(link)[1] not in allParentClasses: judge = False
        elif any(x in get_website(link)[2] for x in allParentClasses): judge = False
        else: judge = True
    return judge

def get_info(link, soup):# create title, site & author, and link
    try: title = soup.find('h1').string.split(' - ')[0].strip() #remove outlet at the end
    except: title = ''
    try: sitesh = get_website(link)[0]
    except: sitesh = "____"
    byLine = soup.select('[class*=byline]')
    try: auth = byLine[1].get_text().split('\t')[0].strip().split('By ')[-1]
    except:
        try: auth = byLine[0].get_text().split('\t')[0].strip().split('By ')[-1]
        except: auth = ''
    info = title +'\n'+ sitesh +' - '+ auth +'\n'+ link
    return info

def text_from_html(link, soup): 
    texts = soup.findAll(text=True)
    resultText = ''
    previous_a = False
    previous_p = True
    # append text
    for t in texts:
        if tag_content(link, t) == False: continue
        elif t.parent.name == 'a': 
            if previous_p == True: 
                resultText = resultText + t.string # if it's <a> after <p> (usually text with a hyperlink), do not add additional \n
            else: resultText = resultText # cuts out <a> if it doesn't come after <p>
            previous_a = True
            previous_p = False
        elif previous_a == True:
            print(type(t.parent.parent.get('class')))
            resultText = resultText + t.string # if it's <p> following <a> with a hyperlink, do not add extra \n
            previous_a = False
            previous_p = True
        else: # if it's a new <p> (new paragraph)
            resultText = resultText + '\n\n'+t.string
            previous_a = False
            previous_p = True
    return resultText.replace('\t','')

#def get_emailsubject(text)
#    try: subject_line = subject_shorthand[sitesh]
#    except: subject_line = sitesh

url = input('Paste URL here:')
driver = webdriver.Chrome()
driver.get(url)
result_soup = BeautifulSoup(driver.page_source, 'html.parser')
print(get_info(url, result_soup)+text_from_html(url, result_soup))

# Issues:
# because the text is <p><span>Text</span></p> and this affects previous_p & previous_a judgements
# use credentials?