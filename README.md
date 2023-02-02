# Welcome to Clipmaster!
***Last update: 2023.2.2 V.5***

<img src="/images/cover.png" width="100%">

Clipmaster scrapes and formats the title, outlet, author and text content of a news article when given its url. 

Clipmaster is a developing project so it needs your contributions to support more sites and clip more accurately. Configuration is easy - no previous coding experience required.

# Features
Supports all the outlets put into its ***'site_configurations.xlsx'*** except for *Bloomberg (detects bot activity very well)*.

* Extracts the desired text content; blocks ads, subscription messages, and multi-media
* Extracts title, author, outlet
* Automatically formats the info for distribution
  * Formats outlet into shorthands
  * Generates email headline
  * Detects "Adams" => generates [MEA] label
  * Detects "opinion / op-ed" in link or title => generates "Opinion:" before title
* Copies the formatted clip to clipboard
* Possible to configure and add new sites with html knowledge - no coding required

# How to Use

## Installation

1. [Download](https://drive.google.com/file/d/1VNW1G4KeiD8Fhhi1yaxTQHQ8x9Z_4wAo/view?usp=share_link) ***'clipmaster.zip'*** and unzip the file.
2. Make sure Microsoft Edge is installed and you're logged in to the paywall-ed websites on Edge.
3. Open a new tab in Edge and go to ***'edge://version'***. Copy your 'Profile Path'.
   
   <img src="/images/profilepath.png" width="70%">
4. Find ***'clipperprofile.txt'*** in Clipmaster's folder, replace the text in there with your profile path and save.
   
   <img src="/images/profileloc.png" width="70%">
5. Close Edge completely and **use ANOTHER browser to monitor news**.
6. This is because Clipmaster starts Edge automatically, and running it manually at the same time will interfere with that.

## Clipping an article

Click ***'clipmaster.exe'***; When prompted paste article link into the window and hit Enter.

<img src="/images/startup.png" width="70%">

Wait for the clip to load. The first clip can take up to 2 mins, and error messages are normal; Each clip after that takes about 10-15 seconds.

<img src="/images/clipped.png" width="70%">

## Set up extraction for a site

1. Open ***'site_configurations.xlsx'***. You will see five sheets. Usually for outlet and text extraction to work for a site you must fill in the rules in the 'generalRules' sheet.
2. In the first column add the host name of the outlet's website, which is usually what comes after "https://" and ends at ".com", '.org", etc. For example: "nytimes.com". Fill the abbreviated shorthand you want for the site in the 2nd column (0).
   
   <img src="/images/siteconfig.png" width="70%">
3. Open an article, highlight some of the text that you want to extract. Right click and select inspect. 
   
    **[Users with prior HTML knowledge can skip to the next point]** In the inspection panel you'll see your desired text under an element which may look like any of these:

    ````
    <h1>Your title</h1>
    <p class="formattedText">your text</p>
    <p>some text <a class='abcd' href="https://thisisalink.com">has links<a> in them</p>
    <p><span>some other texts have double tags outside</span></p>
    ````

    Each piece of text enclosed between <> and </> is an element, and 'class="abcd"' is its class, which determines how it's formatted. So usually the content of the article will have one or some classes in common. We use that to extract article content and exclude other text.

4. Clipmaster extracts an element when: 
   * it has text in it;
   * it or any of its parent elements has the 'identifier' class defined for this outlet;
   * neither it nor any of its parent elements has any of the 'banned' classes defined for this outlet.
   
   So we need to find a class shared only by all the desired text, or a class shared by all the desired plus some unwanted text, and fill it in the 3rd column (1).

   <img src="/images/include.png" width="70%">
   <img src="/images/includecell.png" width="70%">

   Then, find the classes of the elements (or classes of their parents) that need to be excluded. Fill them in the 4th column (2) and separate them by a comma ",". **DO NOT ADD EXTRA SPACE AFTER THE COMMA**.

   <img src="/images/exclude.png" width="70%">
   <img src="/images/excludecell.png" width="70%">

5. The other sheets are optional and they improve extraction accuracy for other parts of the article:
   * *specialSubjectShort*: define a shorthand for the subject line if you want it to be different from the shorthand before the author. E.g. NYT vs. NY TIMES.
   * *specialBylinePos*: define how to locate the article's byline using 1. class name; 2. which among all the elements with that class name to choose (0 means the first one)
   * *specialTitleTag*: define tag type of the article's title, it's \<h1> by default
   * *specialBannedTag*: ban one or more (connect with comma) types of tag for an outlet. For example, if an outlet uses and only uses bold text for "Also Read" messages, type 'b,strong' here to ban them.
