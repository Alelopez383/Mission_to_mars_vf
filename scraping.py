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
    hemisphere_image_urls=hemispheres(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
          "news_title": news_title,
          "news_paragraph": news_paragraph,
          "featured_image": featured_image(browser),
          "facts": mars_facts(),
          "hemispheres": hemisphere_image_urls,
          "last_modified": dt.datetime.now()
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


def hemispheres(browser):
        # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)
    # Parse the data
    hemi_html = browser.html
    hemi_soup = soup(hemi_html, 'html.parser')

    # Retrieve items for hemispheres information
    items = hemi_soup.find_all('div', class_='item')
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    main_url = "https://marshemispheres.com/"

    # Create loop to scrape through all hemisphere information

    for url in items:
        hemispheres = {}
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
        hemispheres['img_url'] = img_url
        hemispheres['title'] = titles
        hemisphere_image_urls.append(hemispheres)
        browser.back()

        return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

