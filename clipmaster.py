# libraries
from bs4 import BeautifulSoup
from bs4.element import Comment
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# setup outlet general rules, format as follows:
# 'site':('SHORTHAND', 'classWeWantAsText', ['blockedClass1','blockedClass2', ...])
generalRule = {'nytimes.com':('NY TIMES','css-at9mc1 evys1bk0',[]),
'nypost.com':('NY POST', 'single__content entry-content m-bottom', ['inline-module__heading widget-heading widget-heading--underline','social-icons__icon--comments__count','single__inline-module alignleft','comments-inline-cta__wrap','credit']),
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
specialBylinePos = {'nypost.com':('[class*=byline]',1),
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
    except: short = "____"
    contentIdentifier = generalRule[site][1]
    bannedClass = generalRule[site][2]
    try: bylinePos = specialBylinePos[site]
    except: bylinePos = ('[class*=byline]',0) # default byline extraction
    try: titleTag = specialTitleTag[site]
    except: titleTag = 'h1'
    try: bannedTag = specialBannedTag[site]
    except: bannedTag = []
    return short, contentIdentifier, bannedClass, bylinePos, titleTag, bannedTag

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

def generate_info(link, soup): # create formatted title, site, author and link
    try: title = soup.find(get_site_info(link)[4]).string.split(' - ')[0].strip() #remove outlet at the end
    except: title = ''
    byLine = soup.select(get_site_info(link)[3][0])
    try: 
        auth = byLine[get_site_info(link)[3][1]].get_text().strip()
        for x in ['\t','|','New York Daily News']: auth = auth.split(x)[0]
        for x in ['By ','By','by ']: auth = auth.replace(x, '')
    except: auth = ''
    info = title +'\n'+ get_site_info(link)[0] +' - '+ auth +'\n'+ link
    return info

def text_from_html(link, soup): # created formatted text
    texts = soup.findAll(text=True)
    resultText = ''
    previous_a = False
    previous_p = True
    # append text
    for t in texts:
        if tag_content(link, t) == False: continue
        elif t.parent.name in ('a','strong','em','i'):
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

url = input('Paste URL here:')
driver = webdriver.Chrome()
driver.get(url)
result_soup = BeautifulSoup(driver.page_source, 'html.parser')
f = open('clip.txt', 'w', encoding="utf-8")
f.write(generate_info(url, result_soup)+text_from_html(url, result_soup))
print('▬▬▬▬▬▬▬▬▬▬▬▬DONE▬▬▬▬▬▬▬▬▬▬▬▬')

# Issues:
# AMNY, GG: because the text is <p><span>Text</span></p> and this affects previous_p & previous_a judgements
# STREETSBLOG cannot remove embedded twitter
# if it's just <a>,<i>,<em> inside a <p> or starting right after a <p>, there's no line break
# need to adjust the way we concatenate none <p> text

# NYP: write a specific override for multiple authors

# Need to use credentials: CRAIN'S, POLITICO PRO, WSJ, DN, bloomberg
#   but if you close the tab before the paywall loads you can get the whole thing for DN
# build opinion detector by checking if there's 'opinion' between the first & second '/'