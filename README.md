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
Now that the web app is looking good and functioning well, we want to scrape Full-Resolution Mars Hemisphere Images so we can add after in the web application. To do so, we use https://marshemispheres.com/ to extract the images with their titles and urls, and for loop to get the list.

```
#Browser to visit url
url = 'https://marshemispheres.com/'
browser.visit(url)

hemi_html = browser.html
hemi_soup = soup(hemi_html, 'html.parser')

items = hemi_soup.find_all('div', class_='item')

#Create a list to hold the info
hemisphere_image_urls = []

#Write code to retrieve the image urls and titles for each hemisphere.

main_url = "https://marshemispheres.com/"

for url in items:
    hemisphere = {}
    titles = url.find('h3').text
    
    # create link for full image
    link_ref = url.find('a', class_='itemLink product-item')['href']
    
    # Use the base URL to create an absolute URL and browser visit
    browser.visit(main_url + link_ref)
    
    # parse the data
    image_html = browser.html
    image_soup = soup(image_html, 'html.parser')
    download = image_soup.find('div', class_= 'downloads')
    img_url = download.find('a')['href']
    
    # append list
    hemisphere['img_url'] = img_url
    hemisphere['title'] = titles
    hemisphere_image_urls.append(hemisphere)
    browser.back()
    
 #Print the list that holds the dictionary of each image url and title.
 hemisphere_image_urls
 
 ##Quit the browser
browser.quit()
```
![image](https://user-images.githubusercontent.com/43974872/200751458-3951d883-3f0c-4536-87a4-cc9f6fee2e85.png)
