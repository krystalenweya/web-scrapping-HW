#!/usr/bin/env base
# coding: utf-8

# In[78]:


from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser 
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# In[79]:

def scrape():
    executable_path= {'executable_path':ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html

    soup = BeautifulSoup(html, "html.parser")
    print(soup.prettify())

# find the first news title
    
    news_title = soup.body.find("div", class_="content_title").text

# find the paragraph associated with the first title

    news_p = soup.body.find("div", class_="article_teaser_body").text

    print(f"The title is: \n{news_title}")
    print()
    print(f"The descriptive paragraph is:  \n{news_p}")


    url_image= "https://spaceimages-mars.com"
    browser.visit(url_image)
    html = browser.html



    soup = BeautifulSoup(html, "html.parser")
    print(soup.prettify())

    image_mars= soup.body.find("img", class_="headerimage")["src"]

    image_mars_url= url + image_mars

    print(f"{image_mars_url}")



    url = "https://galaxyfacts-mars.com"
    facts_mars = pd.read_html(url)

    facts_mars[0]
    
    df_facts_mars= facts_mars[0]
    
    df_facts_mars.columns = df_facts_mars.iloc[0]
    df_facts_mars=df_facts_mars.drop (facts_mars[0].index[0])
    df_facts_mars


    df_facts_mars= df_facts_mars.set_index("Mars - Earth Comparison")
    df_facts_mars

    html_facts_mars = df_facts_mars.to_html()
    html_facts_mars
    
    hemisphere_url = "https://marshemispheres.com/"
    browser.visit(hemisphere_url)
    html = browser.html


    soup = BeautifulSoup(html, "html.parser")
    print(soup.prettify())


    div_list = soup.body.find_all("div", class_="description")


    websites= []
    for div in div_list:
        website= div.find("a", class_="product-item")["href"]
        websites.append(website)
        websites

    # create empty list to store dictionaries
    hemisphere_image_urls = []

    # cycle through each site href
    for website in websites:
        try:
        
        # visit specifichemisphere page and take HTML code
            url = hemisphere_url + website
            browser.visit(url)
            html = browser.html
        
        # convert HTML to BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
        
        # use BeautifulSoup to find image with specified class and access source of image
            img_url_ending = soup.body.find("img", class_="wide-image")["src"]
        
        # add base url to the image source to get full url
            img_url = hemisphere_url + img_url_ending
        
        # use title on page, removing unneeded trailing " Enhanced" to get title
            title = soup.body.find("h2", class_="title").text.strip()[:-9]
        
        # append dictionary of information to list
            hemisphere_image_urls.append({"title": title, "img_url": img_url})
        
        except Exception as e:
            print(e)

    # print dictionary
    print(hemisphere_image_urls)

    browser.quit()

    scraped_data = {"NewsTitle": news_title,
        "NewsParagraph": news_p,
        "FeaturedImage": image_mars_url,
        "MarsFactsTable": html_facts_mars,
        "HemisphereImages": hemisphere_image_urls}
    
    return scraped_data


# %%
