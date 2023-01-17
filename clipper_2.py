# libraries
from bs4 import BeautifulSoup
from bs4.element import Comment
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# setup outlet shorthands
shorthand = {'nytimes.com':'NY TIMES',
'nypost.com':'NY POST',
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

subject_shorthand = {'NY TIMES':'NYT',
'NY POST':'NYP',
'DAILY NEWS':'DN',
'NY MAGAZINE':'NY MAG'}

def tag_content(element):
    # eliminate by enclosing parent tags
    for parent in element.parents:
        if parent.name in ['header','footer','nav','figcaption']:
            judge = False
    # by tag type
    if element.parent.name not in ['p', 'a', 'h2']: judge = False
    elif isinstance(element, Comment): judge = False
    # by text
    elif element.string in ['Advertisement', 'Advertise with us']: judge = False
    # by class
    elif any(x in str(element.parent.get('class')) for x in ['type-fineprint','Subscribe','subscribe']): judge = False  #Gothamist
    # by a string in the href
    elif any(y in str(element.parent.get('href')) for y in ['#after']): judge = False #NYT
    else:
        judge = True
    return judge

def get_info(link, soup):# create title, site & author, and link
    try: title = soup.find('h1').string.split(' - ')[0].strip() #remove outlet at the end
    except: title = ''
    try: sitesh = shorthand[link.split('https://')[-1].split('www.')[-1].split('/')[0]]
    except: sitesh = "____"
    byLine = soup.select('[class*=byline]')
    try: auth = byLine[1].get_text().split('\t')[0].strip().split('By ')[-1]
    except:
        try: auth = byLine[0].get_text().split('\t')[0].strip().split('By ')[-1]
        except: auth = ''
    info = title +'\n'+ sitesh +' - '+ auth +'\n'+ link +'\n\n'
    return info, sitesh

def text_from_html(soup): 
    texts = soup.findAll(text=True)
    content_texts = filter(tag_content, texts)
    # append text
    resultText = ''
    previous_a = False
    previous_p = True
    for t in content_texts:
        if t.parent.name == 'a': 
            if previous_p == True: 
                resultText = resultText + t.string # if it's <a> after <p> (usually text with a hyperlink), do not add additional \n
            else: resultText = resultText # cuts out <a> if it doesn't come after <p>
            previous_a = True
            previous_p = False
        elif previous_a == True:
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
f = open('clip.txt', 'w')
f.write(get_info(url, result_soup)[0]+text_from_html(result_soup))
print('---DONE---')

# Issues:
# need to develop different content screener and text to html for AMNY 
# because the text is <p><span>Text</span></p> and this affects previous_p & previous_a judgements
# use credentials?