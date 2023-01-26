# libraries
print('Welcome. Loading...')
from bs4 import BeautifulSoup
from bs4.element import Comment
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import pandas as pd
import os
# dictionaries - rules for text extraction
Rules = pd.ExcelFile('site_configurations.xlsx')
generalRule = pd.read_excel(Rules, sheet_name='generalRule',index_col = 0).fillna('').to_dict(orient = 'index')
specialSubjectShort = pd.read_excel(Rules, sheet_name='specialSubjectShort',index_col = 0).fillna('').to_dict(orient = 'index')
specialBylinePos = pd.read_excel(Rules, sheet_name='specialBylinePos',index_col = 0).fillna('').to_dict(orient = 'index')
specialTitleTag = pd.read_excel(Rules, sheet_name='specialTitleTag',index_col = 0).fillna('').to_dict(orient = 'index')
specialBannedTag = pd.read_excel(Rules, sheet_name='specialBannedTag',index_col = 0).fillna('').to_dict(orient = 'index')
for x in generalRule.keys(): generalRule[x] = (generalRule[x][0], generalRule[x][1], str(generalRule[x][2]).split(',')) # may need to strip spaces at beginning at end in case someone adds it
for x in specialBylinePos: specialBylinePos[x] = (specialBylinePos[x][0], specialBylinePos[x][1])
for x in [specialSubjectShort,specialTitleTag]:
    for y in x.keys(): x[y] = x[y][0]
for x in specialBannedTag: specialBannedTag[x] = str(specialBannedTag[x][0]).split(',')

def get_site_info(link):
    site = link.split('https://')[-1].split('www.')[-1].split('/')[0]
    try: short = generalRule[site][0]
    except: 
        short = site.split('.')[0].upper()
        subjectShort = short
        contentIdentifier = 'article'
        bannedClass = []
        bylinePos = ('[class*=byline]',0)
        titleTag = 'h1'
        bannedTag = []
        opEd = link.find('opinion')
        message = '▬▬▬▬▬▬▬▬▬▬Site not supported yet :( We suggest clipping by hand but heres what we can find:▬▬▬▬▬▬▬▬▬▬'
        return short, contentIdentifier, bannedClass, bylinePos, titleTag, bannedTag, subjectShort, opEd, message
    try: subjectShort = specialSubjectShort[site]
    except: subjectShort = short
    contentIdentifier = generalRule[site][1]
    bannedClass = generalRule[site][2]
    try: bylinePos = specialBylinePos[site]
    except: bylinePos = ('[class*=byline]',0) # default byline extraction
    try: titleTag = specialTitleTag[site]
    except: titleTag = 'h1' # default title extraction
    try: bannedTag = specialBannedTag[site]
    except: bannedTag = [] # refer to default list of tag types allowed
    opEd = link.find('opinion')
    return short, contentIdentifier, bannedClass, bylinePos, titleTag, bannedTag, subjectShort, opEd

def tag_content(link, element): # testing if a line is part of the text
    generalTags = ['p','a','em','i','strong','b','span','li','h2','h3','h4']
    siteTags = [x for x in generalTags if x not in get_site_info(link)[5]]
    if element.parent.name not in siteTags: judge = False
    elif isinstance(element, Comment): judge = False
    else:
        allParentClasses = []
        for parent in element.parents:
            pClassList = parent.get('class')
            try: pClass = ' '.join(pClassList)
            except: pClass = 'NA'
            if pClass == '': pClass = 'NA'
            allParentClasses.append(pClass)
        if get_site_info(link)[1] not in allParentClasses: judge = False
        elif any(x in get_site_info(link)[2] for x in allParentClasses): judge = False
        else: judge = True
    return judge

def format_author(link,byLine):
    auth = byLine.get_text().strip()
    if get_site_info(link)[0] == 'POLITICO': auth = re.sub('\s+',' ',re.sub(' Close.*?\n.*?bio page', '', auth)).replace(' ,',',') # political multiple authors workaround
    if get_site_info(link)[0] == 'NY POST': # nyp multiple authors workaround
        stringL = auth.split('\n')
        removeWords = ['Social Links','Author','author','required','Submit','Δ','follow']
        for x in stringL: 
            if any(y in x for y in removeWords): stringL.remove(x)
        auth = re.sub('\s+',' ',''.join(stringL))
        auth = re.sub(' \S*@\S*','', auth) # end of nyp multiple authors workaround
    for x in ['|','New York Daily News','Updated','Published', 'Police']: auth = auth.split(x)[0]
    for y in ['By ','By','by ',': ']:
        if auth.startswith(y) == True: auth = auth.replace(y, '', 1)
    return auth

def generate_info(link, soup): # create formatted title & site & author & link
    try: title = soup.find(get_site_info(link)[4]).string.split(' - ')[0].split(' | ')[-1].strip()
    except: title = ''
    if get_site_info(link)[7] >= 0: title = 'Opinion: ' + title
    try: auth = format_author(link,soup.select(get_site_info(link)[3][0])[get_site_info(link)[3][1]])
    except: auth = ''
    info = title +'\n'+ get_site_info(link)[0] +' - '+ auth +'\n'+ link
    return info

def text_from_html(link, soup): # created formatted text
    texts = soup.findAll(text=True)
    resultText = ''
    previous = 'para'
    for t in texts:
        if tag_content(link, t) == False: continue
        elif t.parent.name in ['p','li','h2','h3','h4']: # this tag is a paragraph
            if previous == 'para':
                if any(t.string.find(x) == 0 for x in [',','.','!','?']): resultText = resultText + t.string # screen out line break issues
                else: resultText = resultText + '\n\n'+ t.string
            else: resultText = resultText + t.string # previous = 'inline'
            previous = 'para'
        else: # this tag may be inline special tags or special tags that take up a line
            if t.parent.parent.get_text().startswith(t.parent.get_text()) == True: resultText = resultText + '\n\n'+ t.string # inline at beginning of para
            else: resultText = resultText + t.string # inline in the middle/end of para
            if t.parent.parent.get_text().endswith(t.parent.get_text()) == True: previous = 'para' # special tag takes up a line 
            else: previous = 'inline' # special tag is inline
    #resultText = re.sub('[A-Za-z] \n\n', ' ',resultText).replace('\n\n\n','\n\n').replace('\t','') # in case line break issues remain
    resultText = re.sub('\n\n\n*', '\n\n', re.sub('[A-Za-z] \n\n', ' ',resultText)).replace('\t','') # in case line break issues remain
    if get_site_info(link)[0] == 'SI ADVANCE': # SI ADVANCE remove related content
        for x in ['\n\nADDITIONAL','\n\nMORE','\n\nRELATED']: resultText = resultText.split(x)[0]
    return resultText

def generate_emailSubject(link, text):
    subjectShort = get_site_info(link)[6] + ': '
    title = text.split('\n')[0] + '\n'
    if text.find('Adams') < 0: subject = subjectShort + title
    else: subject = subjectShort + '[MEA] ' + title
    return subject

cont = True
clipperprofile = 'user-data-dir=' + os.path.abspath('Clipper')
options = webdriver.ChromeOptions()
options.add_argument(clipperprofile)
options.add_argument("--window-size=720,1080")
while cont == True:
    url = input('Paste URL here:')
    #driver = webdriver.Chrome("chromedriver.exe", options=options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    try:
        driver.get(url)
        print('\nLoading clip......\n')
        result_soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close()
        text = generate_info(url, result_soup) + text_from_html(url, result_soup)
        print('▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬CLIP STARTS HERE▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n')
        print(generate_emailSubject(url, text) + text)
        try: print(get_site_info(url)[8])
        except: print('\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬CLIP SUCCESSFUL!▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬')
    except:
        driver.close() 
        print('Error: Link format not recognized')
    contmsg = input('Keep clipping? y/n')
    if contmsg == 'y':
        cont = True
    else: cont = False
print('Thank you for using Clipmaster.')

# Issues:

# STREETSBLOG cannot remove embedded twitter - but now it's an independent paragraph

# opinion detector does not support NYP, becuz they don't differentiate it in the link

# NYT opinion author's bio is not included because it's separated from main text by 'follow us on twitter' messages