# Welcome to Clipmaster!
<i>Last update: 2023.1.23</i>

Clipmaster scrapes and formats the title, outlet, author and text content of a news article when given its url. 

Clipmaster is a developing project so it needs your contributions to support more sites and clip more accurately. Configuration is easy - no previous coding experience required.

## Clipping an article

1. Make sure google chrome is installed
2. Get the link of the article


## Configuring extraction for sites

1. Open 'site_configurations.xlsx'. You will see five sheets. Usually for outlet and text extraction to work for a site you must fill in the rules in the 'generalRules' sheet.
2. In the first column add the host name of the outlet's website, which is usually what comes after "https://" and ends at ".com", '.org", etc. For example: "nytimes.com"
3. Open an article, highlight some of the text that you want to extract. Right click and select inspect.

* [Users with prior HTML knowledge can skip to the next point] In the inspection panel you'll see your desired text under an element which may look like any of these:
        <h1>Your title</h1>
        <p class="formattedText">your text</p>
        <p>some text <a class='abcd' href="https://thisisalink.com">has links<a> in them</p>
        <p><span>some other texts have double tags outside</span></p>
    Each piece of text enclosed between <> and </> is an element, and 'class="abcd"' is its class, which determines how it's formatted. So usually the content of the article will have one or some classes in common. We use that to extract article content and rule out other text.

* Clipmaster extracts an element when: 
   1. it has text in it;
   2. it or any of its parent elements has the 'identifier' class defined for this outlet;
   3. neither it or any of its parent elements has any of the 'banned' classes defined for this outlet.
   
   So we need to find one class shared only by all the desired text, or one shared by all the desired plus some unwanted text, and fill it in the 2nd column. 

   Then, find the classes of the elements (or those of their parents) that need to be ruled out. Fill them in the 3rd column, separate them by a comma ",". DO NOT ADD EXTRA SPACE AFTER THE COMMA.
   
* For example, for NY Times, 

