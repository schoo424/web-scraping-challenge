from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pymongo
import pandas as pd


# def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=False)  

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)  

    first_news_title, first_news_p = mars_news (browser)
    mars_data = {
        "title": first_news_title, 
        "paragraph": first_news_p,
        "image_URL": featured_image(browser),
        "facts": mars_facts()
        # add images and hemisphere stuff here
    }

    return mars_data

def mars_news(browser):
    # NOTE: we're using the chromedriver approach for another example,
    # but we could certainly use the requests library as well.
    # browser = scrape()
    listings = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    results = soup.find_all('li', class_ = 'slide')

    news_title = results[1].find_all('div', class_= 'content_title')
    first_news_title = news_title[0].get_text()

    news_p = soup.find_all('div', class_= 'article_teaser_body')
    first_news_p = news_p[0].get_text()

    return first_news_title, first_news_p

def featured_image(browser):
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    browser.links.find_by_partial_text('more info').click()

    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    feat_img_url = image_soup.find('figure', class_='lede').a['href']
    feat_img_full_url = f'https://www.jpl.nasa.gov{feat_img_url}'
    # print(feat_img_full_url)

    return feat_img_full_url

def mars_facts():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]  
    df.columns = ['Attribute', 'Value']
    df.set_index('Attribute')

    return df.to_html()
