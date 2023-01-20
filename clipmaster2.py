# libraries
from bs4 import BeautifulSoup
from bs4.element import Comment
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import re

# setup outlet general rules, format as follows:
# 'site':('SHORTHAND', 'classWeWantAsText', ['blockedClass1','blockedClass2', ...])
generalRule = {'nytimes.com':('NY TIMES','css-at9mc1 evys1bk0',[]),
'nypost.com':('NY POST', 'single__content entry-content m-bottom', ['inline-module__inner','social-icons__icon--comments__count','single__inline-module alignleft','comments-inline-cta__wrap','credit']),
'nymag.com':('NY MAGAZINE', 'article-content inline',['credit','container','text-form-wrapper']),
'nydailynews.com':('DAILY NEWS','default__StyledText-sc-1wxyvyl-0 hnShxL body-paragraph',[]),
'subscriber.politicopro.com':('POLITICO', 'media-article__text', []),
'wsj.com':('WSJ','css-xbvutc-Paragraph e3t0jlg0',[]),
'bloomberg.com':('BLOOMBERG','body-content',[]),
'washingtonpost.com':('WAPO', 'wpds-c-cYdRxM wpds-c-cYdRxM-iPJLV-css font-copy', ['font--article-body font-copy hide-for-print ma-0 pb-md db italic interstitial']),
'gothamist.com':('GOTHAMIST','streamfield-paragraph rte-text mb-5',[]),
'silive.com':('SI ADVANCE','entry-content',[]),
'thecity.nyc':('THE CITY','RichTextArticleBody RichTextBody',['HTLAds-with-background','Form-newsletter-breaker-wrapper']),
'amny.com':('AMNY','article-content',['syndicated-embedded-player','promo-oneliner newsletter','image-credit']),
'crainsnewyork.com':("CRAIN'S NY",'field--name-field-paragraph-body',[]),
'gothamgazette.com':('GOTHAM GAZETTE','art-article',[]),
'hellgatenyc.com':('HELL GATE','PostContent_wrapper__5uSJk',[]),
'citylimits.org':('CITY LIMITS','elementor-element elementor-element-670ff5a2 post-content elementor-widget elementor-widget-theme-post-content',['hatley-campaign Campaign CampaignType--inline','wp-media-credit']),
'ny.chalkbeat.org':('CHALKBEAT','RichTextArticleBody RichTextBody',['Page-articleBody-TagData','GoogleDfpAd-background is_filled']),
'nyc.streetsblog.org':('STREETSBLOG','entry-content',['wp-caption-text','css-1dbjc4n r-13awgt0 r-12vffkv','share-bottom']),
'cityandstateny.com':('CITY AND STATE','js-content',['advert-tag-text']),
'foxnews.com':('FOX','article-body',['caption'])}

specialSubjectShort = {'nytimes.com':'NYT',
'nypost.com':'NYP',
'nydailynews.com':'DN',
'nymag.com':'NY MAG'}
specialBylinePos = {'nypost.com':('[class*=byline]',0),
'gothamist.com':('[class*=byline]',1),
'thecity.nyc':('[class*=AuthorByline-InPage]',0),
'nytimes.com':('[class*=e1jsehar1]',0),
'gothamgazette.com':('[class*=art-postauthoricon]',0),
'citylimits.org':('[class*=fn]',0)}
specialTitleTag = {'citylimits.org':'title',
'gothamgazette.com':'title'}
specialBannedTag = {'foxnews.com':['strong']}

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
            allParentClasses.append(pClass)
        if get_site_info(link)[1] not in allParentClasses: judge = False
        elif any(x in get_site_info(link)[2] for x in allParentClasses): judge = False
        else: judge = True
    return judge

def format_author(byLine):
    auth = byLine.get_text().strip()
    # nyp multiple authors workaround
    stringL = auth.split('\n')
    removeWords = ['Social Links','Author','author','required','Submit','Δ']
    for x in stringL: 
        if any(y in x for y in removeWords): stringL.remove(x)
    auth = re.sub('\s+',' ',''.join(stringL))
    # end of nyp multiple authors workaround
    for x in ['|','New York Daily News','Updated','Published']: auth = auth.split(x)[0]
    for x in ['By ','By','by ']: auth = auth.lstrip(x)
    return auth

def generate_info(link, soup): # create formatted title & site & author & link
    try: title = soup.find(get_site_info(link)[4]).string.split(' - ')[0].strip()
    except: title = ''
    if get_site_info(link)[7] >= 0: title = 'Opinion: ' + title
    try: auth = format_author(soup.select(get_site_info(link)[3][0])[get_site_info(link)[3][1]])
    except: auth = ''
    info = title +'\n'+ get_site_info(link)[0] +' - '+ auth +'\n'+ link
    return info

def text_from_html(link, soup): # created formatted text
    texts = soup.findAll(text=True)
    resultText = ''
    previous = 'para'
    for t in texts:
        if tag_content(link, t) == False: continue
        elif t.parent.name in ['p', 'li','h2','h3','h4']: # this tag is a paragraph
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
    resultText = resultText.replace(' \n\n', ' ').replace('\n\n\n','\n\n').replace('\t','') # in case line break issues remain
    return resultText

def generate_emailSubject(link, text):
    subjectShort = get_site_info(link)[6] + ': '
    title = text.split('\n')[0] + '\n'
    if text.find('Adams') < 0: subject = subjectShort + title
    else: subject = subjectShort + '[MEA] ' + title
    return subject

url = input('Paste URL here:')
driver = webdriver.Chrome()
driver.get(url)
result_soup = BeautifulSoup(driver.page_source, 'html.parser')
text = generate_info(url, result_soup)+ text_from_html(url, result_soup)
f = open('clip.txt', 'w', encoding="utf-8")
f.write(generate_emailSubject(url, text) + text)
try: print(get_site_info(url)[8])
except: print('▬▬▬▬▬▬▬▬▬▬CLIP SUCCESSFUL!▬▬▬▬▬▬▬▬▬▬')

# Issues:

# Need to use credentials: CRAIN'S, POLITICO PRO, WSJ, DN, bloomberg
#   but if you close the tab before the paywall loads you can get the whole thing for DN

# STREETSBLOG cannot remove embedded twitter
# opinion detector does not support NYP, becuz they don't differentiate it in the link
# needs chrome
# a better way to add/edit site-specific parameters, maybe an excel