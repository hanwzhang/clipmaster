# libraries
from bs4 import BeautifulSoup
from bs4.element import Comment
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# setup outlet shorthands
shorthand = {'nytimes.com':('NY TIMES','css-at9mc1 evys1bk0',[]),
'nypost.com':('NY POST', 'single__content entry-content m-bottom', ['single__inline-module alignleft','comments-inline-cta__wrap','credit']),
'nymag.com':('NY MAGAZINE', 'article-content inline',['credit','container','text-form-wrapper']),
'nydailynews.com':('DAILY NEWS','default__StyledText-sc-1wxyvyl-0 hnShxL body-paragraph',[]),
'subscriber.politicopro.com':('POLITICO', 'media-article__text', []),
'wsj.com':('WSJ','css-xbvutc-Paragraph e3t0jlg0',[]),
'bloomberg.com':('BLOOMBERG','body-content',[]),
'washingtonpost.com':('WAPO', 'wpds-c-cYdRxM wpds-c-cYdRxM-iPJLV-css font-copy', ['font--article-body font-copy hide-for-print ma-0 pb-md db italic interstitial']),
'gothamist.com':('GOTHAMIST','streamfield-paragraph rte-text mb-5',[]),
'silive.com':('SI ADVANCE','entry-content',[]),
'thecity.nyc':('THE CITY','RichTextArticleBody RichTextBody',['HTLAds-with-background','Form-newsletter-breaker-wrapper']),
'amny.com':('AMNY','article-content',['promo-oneliner newsletter','image-credit']),
'crainsnewyork.com':("CRAIN'S NY",'field--name-field-paragraph-body',['']),
'gothamgazette.com':('GOTHAM GAZETTE','art-article',[]),
'hellgatenyc.com':('HELL GATE','PostContent_wrapper__5uSJk',[]),
'citylimits.org':('CITY LIMITS','elementor-element elementor-element-670ff5a2 post-content elementor-widget elementor-widget-theme-post-content',['hatley-campaign Campaign CampaignType--inline']),
'ny.chalkbeat.org':('CHALKBEAT','RichTextArticleBody RichTextBody',['Page-articleBody-TagData','GoogleDfpAd-background is_filled']),
'nyc.streetsblog.org':('STREETSBLOG','entry-content',['wp-caption-text','css-1dbjc4n r-13awgt0 r-12vffkv','share-bottom']),
'cityandstateny.com':('CITY AND STATE','js-content',['advert-tag-text']),
'foxnews.com':('FOX','article-body',['caption'])}

subject_shorthand = {'nytimes.com':'NYT',
'nypost.com':'NYP',
'nydailynews.com':'DN',
'nymag.com':'NY MAG'}

byline_pos = {}

def get_website(link):
    site = link.split('https://')[-1].split('www.')[-1].split('/')[0]
    short = shorthand[site][0]
    contentIdentifier = shorthand[site][1]
    banList = shorthand[site][2]
    return short, contentIdentifier, banList

def tag_content(link, element):
    if element.parent.name not in ['p','a','em','i','strong','span','h2','h3']: judge = False
    elif isinstance(element, Comment): judge = False
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

f = open('clip.txt', 'w')
f.write(get_info(url, result_soup)+text_from_html(url, result_soup))
print('▬▬▬▬▬▬▬▬▬▬▬▬DONE▬▬▬▬▬▬▬▬▬▬▬▬')

# Issues:
# DN get author
# AMNY, GG: because the text is <p><span>Text</span></p> and this affects previous_p & previous_a judgements
# CRAIN'S, POLITICO PRO: use credentials?
# FOX: remove read mores
# STREETSBLOG cannot remove embedded twitter
# CITY limits: headline is h2, byline is not called byline
# maybe block 'read more's by removing lines in '[]'
    # and remove lines that's all link
# if it's just <a>,<i>,<em> inside <p>, there's no line break

# create a little script to test where the bylines are, create that as the new item in the dict
# one universal fix for many issues: create a dict for parent.name, byline, etc. chosen, set current values to default and define ones that are different