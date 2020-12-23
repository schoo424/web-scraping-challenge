from splinter import Browser
from bs4 import BeautifulSoup


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
        "paragraph": first_news_p
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

    # listings["headline"] = soup.find("a", class_="result-title").get_text()
    # listings["price"] = soup.find("span", class_="result-price").get_text()
    # listings["hood"] = soup.find("span", class_="result-hood").get_text()
    results = soup.find_all('li', class_ = 'slide')

    news_title = results[1].find_all('div', class_= 'content_title')
    first_news_title = news_title[0].get_text()

    news_p = soup.find_all('div', class_= 'article_teaser_body')
    first_news_p = news_p[0].get_text()

    return first_news_title, first_news_p
