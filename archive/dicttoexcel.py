import pandas as pd

generalRule = {'nytimes.com':('NY TIMES','css-53u6y8',['css-79elbk']),
'nypost.com':('NY POST', 'single__content entry-content m-bottom', ['inline-slideshow','inline-module__inner','social-icons__icon--comments__count','single__inline-module alignleft','comments-inline-cta__wrap','credit']),
'nymag.com':('NY MAGAZINE', 'article-content inline',['credit','container','text-form-wrapper']),
'nydailynews.com':('DAILY NEWS','default__ArticleBody-sc-1wxyvyl-2 hEvcgL article-body-wrapper-custom',['ts-share-bar','ad_wrapper','figContainer']),
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
'foxnews.com':('FOX','article-body',['close','video-container','caption'])}

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

# y1 = pd.DataFrame.from_dict(generalRule, orient = 'index')

# y2 = pd.DataFrame.from_dict(specialSubjectShort, orient = 'index')

# y3 = pd.DataFrame.from_dict(specialBylinePos, orient = 'index')

# y4 = pd.DataFrame.from_dict(specialTitleTag, orient = 'index')

# y5 = pd.DataFrame.from_dict(specialBannedTag, orient = 'index')

# with pd.ExcelWriter('site_configurations.xlsx') as writer:
#     y1.to_excel(writer, sheet_name = 'generalRule', index = 'False')
#     y2.to_excel(writer, sheet_name = 'specialSubjectShort', index = 'False')
#     y3.to_excel(writer, sheet_name = 'specialBylinePos', index = 'False')
#     y4.to_excel(writer, sheet_name = 'specialTitleTag', index = 'False')
#     y5.to_excel(writer, sheet_name = 'specialBannedTag', index = 'False')
