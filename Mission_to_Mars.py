#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars

# In[16]:


# Import our scraping tools

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd


# In[17]:


#Set your executable path in the next cell, then set up the URL
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[18]:


# Assign the url and instruct the browser to visit it
# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# With the following line, browser.is_element_present_by_css('div.list_text', wait_time=1), we are accomplishing two things.
# 
# One is that we're searching for elements with a specific combination of tag (div) and attribute (list_text). 
# 
# As an example, ul.item_list would be found in HTML as ul class="item_list".
# 
# Secondly, we're also telling our browser to wait one second before searching for components. 
# 
# The optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.

# In[19]:


# set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# Notice how we've assigned slide_elem as the variable to look for the "div /" tag and its descendent (the other tags within the "div /" element) This is our parent element. This means that this element holds all of the other elements within it, and we'll reference it when we want to filter search results even further. The . is used for selecting classes, such as list_text, so the code 'div.list_text' pinpoints the "div /" tag with the class of list_text. CSS works from right to left, such as returning the last item on the list instead of the first. Because of this, when using select_one, the first matching element returned will be a "li /" element with a class of slide and all nested elements within it.
# 
# The data Robin wants to collect from this particular website is the most recent news article along with its summary. Remember, the code for this will eventually be used in an application that will scrape live data with the click of a button—this site is dynamic and the articles will change frequently, which is why Robin is removing the manual task of retrieving each new article.
# 
# 

# opening the page in a new browser, right-click to inspect and activate your DevTools. Then search for the HTML components you'll use to identify the title and paragraph you want.
# 
# We are using class='content_title'

# In[20]:


#Begin the scrapping
slide_elem.find('div', class_='content_title')


# In this line of code, we chained .find onto our previously assigned variable, slide_elem. When we do this, we're saying, "This variable holds a ton of information, so look inside of that information to find this specific data." The data we're looking for is the content title, which we've specified by saying, "The specific data is in a div / with a class of 'content_title'."
# 
# The output should be the HTML containing the content title and anything else nested inside of that div /.

# In[21]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# We've added something new to our .find() method here: .get_text(). When this new method is chained onto .find(), only the text of the element is returned. 

# # Methods to use find in BS4
# 
# - .find() is used when we want only the first class and attribute we've specified.
# - .find_all() is used when we want to retrieve all of the tags and attributes.
# 
# 
# For example, if we were to use .find_all() instead of .find() when pulling the summary, we would retrieve all of the summaries on the page instead of just the first one.
# 

# In[22]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# # Scrape the featured image from another Mars website
# 
# - https://spaceimages-mars.com/

# In[23]:


# First, check out the webpage
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[24]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[25]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# Now we need to find the relative image URL. In our browser (make sure you're on the same page as the automated one), activate your DevTools again. This time, let's find the image link for that image. This is a little more tricky. Remember, Robin wants to pull the most recently posted image for her web app. If she uses the image URL below, she'll only ever pull that specific image when using her app.

# In[26]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# - An img tag is nested within this HTML, so we've included it.
# - .get('src') pulls the link to the image.
# 
# What we've done here is tell BeautifulSoup to look inside the img / tag for an image with a class of fancybox-image. Basically we're saying, "This is where the image we want lives—use the link that's inside these tags."
# 
# We were able to pull the link to the image by pointing BeautifulSoup to where the image will be, instead of grabbing the URL directly. This way, when JPL updates its image page, our code will still pull the most recent image.
# 
# #### But if we copy and paste this link into a browser, it won't work. 
# 
# This is because it's only a partial link, as the base URL isn't included. If we look at our address bar in the webpage, we can see the entire URL up there already; we just need to add the first portion to our app.

# In[27]:


# Add the base URL to our code
# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# # Scrapping Mars facts
# 
# - https://galaxyfacts-mars.com/
# 
# Tables in HTML are basically made up of many smaller containers. The main container is the table / tag. Inside the table is tbody /, which is the body of the table—the headers, columns, and rows.
# 
# tr / is the tag for each table row. Within that tag, the table data is stored in td / tags. This is where the columns are established.
# 
# #### Instead of scraping each row, or the data in each td /, we're going to scrape the entire table with Pandas' .read_html() function.

# In[28]:


#Create a new DataFrame using Pandas from the HTML table

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# - The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. 
# - By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list.
# - Then, it turns the table into a DataFrame.
# - df.columns=['description', 'Mars', 'Earth'] Here, we assign columns to the new DataFrame for additional clarity.
# - df.set_index('description', inplace=True) By using the .set_index() function, we're turning the Description column into the DataFrame's index. 
# - inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable

# ### Now we add the DataFrame to a web application (into an actual webpage). For that we use Pandas to convert our DataFrame back into HTML-ready code using the .to_html() function. 

# In[29]:


df.to_html()


# # End the automated browsing session. 
# 
# This is an important line to add to our web app also. Without it, the automated browser won't know to shut down—it will continue to listen for instructions and use the computer's resources (it may put a strain on memory or a laptop's battery if left on). We really only want the automated browser to remain active while we're scraping data.
# 
# Also, Live sites are a great resource for fresh data, but the layout of the site may be updated or otherwise changed. When this happens, there's a good chance your scraping code will break and need to be reviewed and updated to be used again.
# 
# For example, an image may suddenly become embedded within an inaccessible block of code because the developers switched to a new JavaScript library. It's not uncommon to revise code to find workarounds or even look for a different, scraping-friendly site all together.

# In[30]:


browser.quit()


# In[ ]:





# In[ ]:




