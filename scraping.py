# Import our scraping tools

from splinter import Browser
from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = hemispheres ()
    
    # Run all scraping functions and store results in dictionary
    data = {
          "news_title": news_title,
          "news_paragraph": news_paragraph,
          "featured_image": featured_image(browser),
          "facts": mars_facts(),
          "last_modified": dt.datetime.now(),
          "hemispheres": hemispheres()
    }    
    
    # Stop webdriver and return data
    
    browser.quit()
    return data

    
def mars_news(browser):
    
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set up the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
 # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('div.list_text')


        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()


        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        
        return None, None
    
    return news_title, news_p
   

def featured_image(browser):
    
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

     # Add try/except for error handling
    try:
        
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        
    except AttributeError:
        
        return None


    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    
    return img_url



def mars_facts():
    
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


def hemispheres():
    
    #Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    #visit
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
        
    
# 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

