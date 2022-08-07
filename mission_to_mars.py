#!/usr/bin/env python
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


# In[80]:


url = "https://redplanetscience.com/"
browser.visit(url)
html = browser.html


# In[81]:


soup = BeautifulSoup(html, "html.parser")
print(soup.prettify())


# In[82]:


# find the first news title
    
news_title = soup.body.find("div", class_="content_title").text

# find the paragraph associated with the first title

news_p = soup.body.find("div", class_="article_teaser_body").text


# In[83]:


print(f"The title is: \n{news_title}")
print()
print(f"The descriptive paragraph is:  \n{news_p}")


# In[84]:


#JPL MARS SPACE IMAGES 
#Visit the url for the Featured Space Image page here.
#Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
#Make sure to find the image url to the full size .jpg image.
#Make sure to save a complete url string for this image.
# Example:
#featured_image_url = 'https://spaceimages-mars.com/image/featured/mars2.jpg'


# In[85]:


url_image= "https://spaceimages-mars.com"
browser.visit(url_image)
html = browser.html


# In[86]:


soup = BeautifulSoup(html, "html.parser")
print(soup.prettify())


# In[87]:


image_mars= soup.body.find("img", class_="headerimage")["src"]

image_mars_url= url + image_mars

print(f"{image_mars_url}")


# In[88]:


#Mars facts
#Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
#Use Pandas to convert the data to a HTML table string.


# In[89]:


url = "https://galaxyfacts-mars.com"
facts_mars = pd.read_html(url)

facts_mars[0]


# In[90]:


df_facts_mars= facts_mars[0]


# In[91]:


df_facts_mars.columns = df_facts_mars.iloc[0]
df_facts_mars=df_facts_mars.drop (facts_mars[0].index[0])
df_facts_mars


# In[92]:


df_facts_mars= df_facts_mars.set_index("Mars - Earth Comparison")
df_facts_mars


# In[93]:


html_facts_mars = df_facts_mars.to_html()
html_facts_mars


# In[94]:


#Mars Hemispheres
# Visit the Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
# You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
# Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
# Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.


# In[95]:


hemisphere_url = "https://marshemispheres.com/"
browser.visit(hemisphere_url)
html = browser.html


# In[96]:


soup = BeautifulSoup(html, "html.parser")
print(soup.prettify())


# In[97]:


div_list = soup.body.find_all("div", class_="description")


# In[98]:


websites= []
for div in div_list:
    website= div.find("a", class_="product-item")["href"]
    websites.append(website)
websites


# In[99]:


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


# In[100]:


browser.quit()


# In[ ]:

scraped_data = {"NewsTitle": news_title,
    "NewsParagraph": news_p,
    "FeaturedImage": image_mars_url,
    "MarsFactsTable": html_facts_mars,
    "HemisphereImages": hemisphere_image_urls}
    
return scraped_data


