#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import os
import pandas as pd
import pprint
import pymongo

# @TODO: setup mongo connection
conn = 'mongodb://localhost:27017'

# @TODO: connect to mongo db and collection
client = pymongo.MongoClient(conn)
db = client.mars_db


# In[2]:


# URL for news site
url = "https://mars.nasa.gov/news/"


# In[3]:


# In[4]:

def scrape():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    db.news.remove()
    db.featured_image_url.remove()
    db.mars_weather.remove()
    db.mars_info.remove()
    db.mars_hemispheres.remove()


    # In[5]:


    browser.visit(url)
    time.sleep(1)

    # In[6]:


    html = browser.html


    # In[7]:


    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')


    # In[8]:


    # Find the title of the latest article
    title = soup.find('div', class_='content_title')
    news_title = title.text
    print(news_title)


    # In[9]:


    # Find the paragraph text of the latest aricle
    paragraph = soup.find('div', class_='article_teaser_body')
    news_p = paragraph.text
    print(news_p)
    news = {'title': news_title, 'paragraph': news_p}


    # In[17]:


    # URL for space images site
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url2)
    time.sleep(1)
    browser.click_link_by_id("full_image")
    time.sleep(5)

    html2 = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup2 = bs(html2, 'html.parser')

    # Find the title of the latest article
    image = soup2.find('img', class_='fancybox-image')['src']
    print(image)


    # In[18]:


    # Get url of featured image
    featured_image_url = 'https://www.jpl.nasa.gov' + image
    print(featured_image_url)
    featured_image_url = {'featured_image': featured_image_url}


    # In[19]:


    # URL for Mars Weather twitter
    url3 = 'https://twitter.com/marswxreport?lang=en'


    # In[20]:


    browser.visit(url3)
    html3 = browser.html


    # In[21]:


    # Create BeautifulSoup object; parse with 'html.parser'
    soup3 = bs(html3, 'html.parser')


    # In[22]:


    # Find the weather information on Mars based on the most recent tweet
    weather = soup3.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_weather = weather.text
    print(mars_weather)
    mars_weather = {'weather': mars_weather}


    # In[23]:


    # URL for Mars Facts
    url4 = 'https://space-facts.com/mars/'


    # In[24]:


    browser.visit(url4)
    html4 = browser.html


    # In[25]:


    # Create BeautifulSoup object; parse with 'html.parser'
    soup4 = bs(html4, 'html.parser')


    # In[26]:


    # Get table info and convert to html
    tables = pd.read_html(html4)
    info_table = tables[0]
    info_table = info_table.set_index(0)
    info_table = info_table.to_html(index_names=False, header=False)
    mars_info = {'table': info_table}

    # In[27]:


    # URL for USGS Astrogeology
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    # In[28]:


    browser.visit(url5)
    html5 = browser.html


    # In[29]:


    # Create BeautifulSoup object; parse with 'html.parser'
    soup5 = bs(html5, 'html.parser')


    # In[30]:


    def retrieve_hemis():
        # URL for USGS Astrogeology
        url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        
        # Visit URL and parse html
        browser.visit(url5)
        html5 = browser.html
        soup5 = bs(html5, 'html.parser')
        
        # find the articles
        articles = soup5.find_all('div', class_='description')[0:4]
        
        # create list object to store output
        imgs = []
        
        # iterate over articles
        for article in articles:
            img = {}
            href = article.h3.text
            browser.click_link_by_partial_text(href)
            html5 = browser.html
            soup5 = bs(html5, 'html.parser')
            img['title'] = href
            img['img_url'] = soup5.find('a', target='_blank')['href']
            imgs.append(img)
            
            #restart process
            browser.visit(url5)
        
        return(imgs)


    # In[31]:


    imgs = retrieve_hemis()


    # In[32]:


    print(imgs)


    # In[33]:

    db.news.insert(news)
    db.featured_image_url.insert(featured_image_url)
    db.mars_weather.insert(mars_weather)
    db.mars_info.insert(mars_info)
    db.mars_hemispheres.insert_many(imgs)


# Use to run the function
# scrape()