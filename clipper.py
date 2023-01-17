# libraries
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from bs4.element import Comment
import ssl
# ignore SSL certificate errors, setting up url
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
# setup outlet shorthands
shorthand = {'nytimes.com':'NY TIMES',
'nypost.com':'NY POST',
'nydailynews.com':'DAILY NEWS',
'politico.com':'POLITICO',
'wsj.com':'WSJ',
'bloomberg.com':'BLOOMBERG',
'washingtonpost.com':'WAPO',
'gothamist.com':'GOTHAMIST',
'silive.com':'SI ADVANCE',
'thecity.nyc':'THE CITY',
'amny.com':'AMNY',
'foxnews.com':'FOX'}

def tag_content(element):
    # eliminate by enclosing parent tags
    for parent in element.parents:
        if parent.name in ['header','footer','nav','figcaption']:
            judge = False
    # by tag type
    if element.parent.name not in ['p', 'a']: judge = False
    elif isinstance(element, Comment): judge = False
    # by text
    elif element.string in ['Advertisement', 'Advertise with us']: judge = False
    # by class
    elif any(x in str(element.parent.get('class')) for x in ['type-fineprint']): judge = False  #Gothamist
    # by a string in the href
    elif any(y in str(element.parent.get('href')) for y in ['#after']): judge = False #NYT
    else:
        judge = True
    return judge

def get_info(link, soup):# create title, site & author, and link
    title = soup.find('h1').string.split(' - ')[0].strip() #remove outlet at the end
    try: sitesh = shorthand[link.split('https://')[-1].split('www.')[-1].split('/')[0]]
    except: sitesh = "____"
    byLine = soup.select('[class*=byline]')
    try: auth = byLine[1].get_text().split('\t')[0].strip().split('By ')[-1]
    except:
        try: auth = byLine[0].get_text().split('\t')[0].strip().split('By ')[-1]
        except: auth = ''
    info = title +'\n'+ sitesh +' - '+ auth +'\n'+ link +'\n\n'
    return info

def text_from_html(soup):
    texts = soup.findAll(text=True)
    content_texts = filter(tag_content, texts)
    # append text
    resultText = ''
    previous_a = False
    previous_p = True
    for t in content_texts:
        if t.parent.name == 'a': # usually if it's a text with a hyperlink
            if previous_p == True: resultText = resultText + t.string
            else: resultText = resultText # leaves out <a> after the last paragraph
            previous_a = True
            previous_p = False
        elif previous_a == True: # if it's normal text following text with a hyperlink
            resultText = resultText + t.string
            previous_a = False
            previous_p = True
        else: # if it's a new paragraph
            resultText = resultText + '\n\n'+t.string
            previous_a = False
            previous_p = True
    return resultText.replace('\t','')

url = input('Paste URL here:')
html = urllib.request.urlopen(url, context = ctx).read()
#html = open('dn.html').read()
result_soup = BeautifulSoup(html, 'html.parser')
print(get_info(url, result_soup)+text_from_html(result_soup))