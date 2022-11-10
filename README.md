# Mission_to_mars
Robin, who loves astronomy and wants to work for NASA one day, has decided to use a specific method of gathering the latest data: web scraping. Using this technique, she has the ability to pull data from multiple websites, store it in a database, then present the collected data in a central location: a webpage. We are helping Robin to write a Python script using BeautifulSoup and Splinter to automate web browsers and extract data; then store the data using MongoDB; build and app using Flask; and last, creating a portafolio using Boostrap (a HTML on CSS framework).

What we need to do:

We need to explore the design of the webpage so that we can write a script that knows what it's looking at when it interacts with a webpage. Robin wants to be kept up to date with different Mars news, and she's enjoyed the articles published on the NASA news website Mars https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest; images from https://spaceimages-mars.com, and some more data from https://galaxyfacts-mars.com/


We helped Robin to automate visiting a website to scrape the top news article (title and summary) and, with just a few lines of code, we have automated the task of visiting a website and navigating through it to find a full-size image, and then we've extracted a link based on its location on the page. Our app will always pull the full-size featured image.

- Scrapping title and summary

```
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

```
- Scrapping images
```
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

```
https://spaceimages-mars.com/image/featured/mars2.jpg

- Scrapping table
```
#Create a new DataFrame using Pandas from the HTML table

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df
```
![image](https://user-images.githubusercontent.com/43974872/200367777-854193d9-aba7-4656-b6f8-bdb436645d48.png)

```
#Turn the DataFrame back to html
df.to_html()

```
![image](https://user-images.githubusercontent.com/43974872/200367858-4edacfae-045f-49a8-bf15-d04f6f8efb37.png)

# After creating a web application with Flask, MongoDB and Boostrap we got the shell:

![image](https://user-images.githubusercontent.com/43974872/200478022-10a7c6b6-dc9c-478e-9df4-4c45dfd29db3.png)

# When Flask, MongoDB and the Python script are connected, we got:
![image](https://user-images.githubusercontent.com/43974872/200483460-a0d6d877-8d11-440b-9ccc-fbaaae66a8e6.png)

# After scraping the newest data:
![image](https://user-images.githubusercontent.com/43974872/200483283-5cfac232-49f8-46ea-882a-e9cf277c7668.png)

# Hemispheres images
Now that the web app is looking good and functioning well, we want to scrape Full-Resolution Mars Hemisphere Images so we can add after in the web application. To do so, we use https://marshemispheres.com/ to extract the images with their titles and urls, and for loop to get the list. After having the correct script, the scrapin with all the mars_data (titles, url, images for the latests news, hemispheres images), also we need to have MongoD open, Flask running, Mongosh with the database functioning, the index.html and just run the Python code, app.py.

```
-------------------------------- 
# Hemispheres images and titles #
---------------------------------
# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
img_soup = soup(html, 'html.parser')

# find the relative image url
h_img_url_p=img_soup.find('a',class_="itemLink product-item").get('href')

#Complete url
h_img_url= f'https://marshemispheres.com/{h_img_url_p}'
#we want to find all, not only one
h_img_url_p=img_soup.find_all('a',class_="itemLink product-item")

#parse and use for loop to have all the links complete
html=browser.html
img_soup = soup(html,'html.parser')
complete_links=[]
for line in img_soup.find_all('a',class_="itemLink product-item"):
    h_img_url= f"https://marshemispheres.com/{line.get('href')}"
    if h_img_url not in complete_links:
        complete_links.append(h_img_url)
complete_links.pop()

#list to put the urls
hemisphere_image_urls = []

for link in complete_links:
    #empty dictionary
    hemispheres={}
    #browse through each one
    browser.visit(link)
    #parse
    im_html=browser.html
    he_img_soup = soup(im_html,'html.parser')
    #scrape
    he_title=he_img_soup.find('h2', class_='title').get_text()
    he_img_url_p=he_img_soup.find('a', target="_blank", string='Sample').get('href')
    #complete links
    he_img_url= f'https://marshemispheres.com/{he_img_url_p}'
    #append
    hemispheres={'img_url': he_img_url, 'title':he_title}
    hemisphere_image_urls.append(hemispheres)
        
    # Browse back to repeat
    browser.back()
```
- URL list
![image](https://user-images.githubusercontent.com/43974872/201003654-0200ba2d-1f87-4a77-803d-4aa7704a5b5a.png)

# Updating web application
![image](https://user-images.githubusercontent.com/43974872/201003267-998f09cd-d7e3-4aa6-a664-ab0c9ddf9836.png)

# To make the app mobile responsive
We can use the DevTools to check if any web application is mobile responsive 

![image](https://user-images.githubusercontent.com/43974872/201009160-d6de6c2e-608e-4d2b-a922-52f422c77a3f.png)

- For tablets, we would use col-sm-12. 
- For mobile phones, col-xs-12 is ideal. 
- For larger screens as well: col-lg-12.

# Code:
To see the code:

- App script: app.py
- HTML code: index_starter.html
- Scraping script: scraping.py
