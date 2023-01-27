# Welcome to Clipmaster!
<i>Last update: 2023.1.26</i>

Clipmaster scrapes and formats the title, outlet, author and text content of a news article when given its url. 

Clipmaster is a developing project so it needs your contributions to support more sites and clip more accurately. Configuration is easy - no previous coding experience required.

# Features
* Extracts the desired text content from news websites; <b>blocks ads, subscription messages, and captions</b>
* Extracts title, author, outlet
* <b>Automatically formats the info for distribution</b>
  * Formats outlet into shorthands
  * Generates email headline
  * Detects "Adams" => generates [MEA] label
  * Detects "opinion" in link or title => generates "Opinion:" before title
* Possible to <b>configure and add new sites with html knowledge</b> - no coding required

## Supported sites

* <i>Clipmaster vanilla</i> (can't login to subscription sites) supports all the priority outlets on [our media monitoring sheet](https://docs.google.com/spreadsheets/d/18mKdQzu_WDidZIYGT-Ga2HxpudCyLBTFIYQvnVMYt8E/edit#gid=0) except for those with paywalls: <b>Wall Street Journal, Bloomberg, Politico Pro, Crain's NY; sometimes NY daily news (creates a paywall after too many visits).</b>
* <i>Clipmaster service</i> can clip from the priority outlets including the 5 paywall-ed ones, but I don't know how to set that up on another computer so far.

# How to Use

## Clipping an article

1. Make sure chrome is installed
2. Click the exe file in the folder; When prompted paste article link into the window
3. After a short wait an automated window will pop up; Wait for the clip to load.

## Let's demo

* GOTHAMIST [https://gothamist.com/news/nyc-mayor-dishes-on-gas-stoves-and-says-hes-a-fan-as-governor-considers-statewide-ban](https://gothamist.com/news/nyc-mayor-dishes-on-gas-stoves-and-says-hes-a-fan-as-governor-considers-statewide-ban)

* NY TIMES [https://www.nytimes.com/2023/01/25/nyregion/composting-garbage-nyc.html?searchResultPosition=2](https://www.nytimes.com/2023/01/25/nyregion/composting-garbage-nyc.html?searchResultPosition=2)

* Paywalled examples: NY DAILY NEWWS [https://www.nydailynews.com/new-york/nyc-crime/ny-nypd-commander-ousted-from-his-precinct-being-promoted-20230124-edcpsyew6bgujpfksftn6az4eq-story.html](https://www.nydailynews.com/new-york/nyc-crime/ny-nypd-commander-ousted-from-his-precinct-being-promoted-20230124-edcpsyew6bgujpfksftn6az4eq-story.html)

* WSJ [https://www.wsj.com/articles/a-charter-school-test-for-eric-adams-new-york-teachers-union-standards-discipline-education-students-11674408280?mod=Searchresults_pos2&page=1](https://www.wsj.com/articles/a-charter-school-test-for-eric-adams-new-york-teachers-union-standards-discipline-education-students-11674408280?mod=Searchresults_pos2&page=1)

* Not supported site example: ASTORIA POST [https://astoriapost.com/city-council-rejects-rezoning-application-for-auto-dealership-on-northern-boulevard](https://astoriapost.com/city-council-rejects-rezoning-application-for-auto-dealership-on-northern-boulevard)

## Set up extraction for a site

1. Open 'site_configurations.xlsx'. You will see five sheets. Usually for outlet and text extraction to work for a site you must fill in the rules in the 'generalRules' sheet.
2. In the first column add the host name of the outlet's website, which is usually what comes after "https://" and ends at ".com", '.org", etc. For example: "nytimes.com"
3. Open an article, highlight some of the text that you want to extract. Right click and select inspect. 
   
    <i>[Users with prior HTML knowledge can skip to the next point]</i> In the inspection panel you'll see your desired text under an element which may look like any of these:

    ````
    <h1>Your title</h1>
    <p class="formattedText">your text</p>
    <p>some text <a class='abcd' href="https://thisisalink.com">has links<a> in them</p>
    <p><span>some other texts have double tags outside</span></p>
    ````

    Each piece of text enclosed between <> and </> is an element, and 'class="abcd"' is its class, which determines how it's formatted. So usually the content of the article will have one or some classes in common. We use that to extract article content and rule out other text.
4. Clipmaster extracts an element when: 
   * it has text in it;
   * it or any of its parent elements has the 'identifier' class defined for this outlet;
   * neither it or any of its parent elements has any of the 'banned' classes defined for this outlet.
   
   So we need to find one class shared only by all the desired text, or one shared by all the desired plus some unwanted text, and fill it in the 2nd column. 

    Then, find the classes of the elements (or those of their parents) that need to be ruled out. Fill them in the 3rd column, separate them by a comma ",". DO NOT ADD EXTRA SPACE AFTER THE COMMA.

# Issues / plans
1. Get paywall version to work for other computers
    
    Simplest solution would be manually set it up on the office's computers
    
2. Simplify - copy clip to clipboard?
3. Improve format accuracy - using the excel, or someone with python knowledge