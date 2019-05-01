#!/usr/bin/env python
# coding: utf-8

# ## CWRU Data Analytics
# **Unit 12 | Assignment - Mission to Mars**
# 
# Robert Wood  
# 5/4/2019

# Import dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import time

def scrape():

    # ## Step 1 - Scraping

    # ### 1a. NASA Mars News
    # 
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
    # Assign the text to variables that you can reference later.

    # URL of page to be scraped
    nasa_url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(nasa_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    # results are returned as an iterable list
    results = soup.find_all('div', class_="slide")

    # Declare empty lists to hold results
    titles = []
    teasers = []

    # Loop through returned results
    for result in results:
        # Error handling
        try:
            # Identify and return article title, strip leading and trailing spaces
            title = result.find('div', class_="content_title").text.strip()
            # Append title to titles list
            titles.append(title)
            # Identify and return article text, strip leading and trailing spaces
            teaser = result.find('div', class_="rollover_description_inner").text.strip()
            # Append teaser to teasers list
            teasers.append(teaser)

        except AttributeError as e:
            print(e)

    # Store the title and teaser for the first article to variables
    first_article_title = titles[0]
    first_article_teaser = teasers[0]


    # ### 1b . JPL Mars Space Images - Featured Image
    # 
    # Visit the url for JPL Featured Space Image.  Use splinter to navigate the site and find the image url for the current
    # Featured Mars Image and assign the url string to a variable called featured_image_url. Make sure to find the image url
    # to the full size .jpg image. Make sure to save a complete url string for this image.

    # Assign path for chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}

    # Assign browser variable
    browser = Browser('chrome', **executable_path, headless=True)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Assign html code to variable
    html = browser.html
    # Navigate to the Full Image overlay
    browser.click_link_by_partial_text('FULL IMAGE')

    # Pause to ensure the browser has navigated before executing additional code
    time.sleep(2)

    # Assign html code to variable
    html = browser.html

    # Navigate to the more info page
    browser.click_link_by_partial_text('more info')

    # Assign html code to variable
    html = browser.html

    # Close browser window
    browser.quit()

    # Create BS object
    soup = BeautifulSoup(html, 'html.parser')

    # Find the two divs that contain the full-size photo links
    div = soup.find_all('div', class_="download_tiff")

    # Assign the filename for the .jpg using the second link
    jpg_filename = div[1].find('a').text

    # Assemble completed URL
    featured_image_url = "https://photojournal.jpl.nasa.gov/jpeg/" + jpg_filename


    # ### 1c. Mars Weather
    # 
    # Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.

    # URL of page to be scraped
    twitter_url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = requests.get(twitter_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Store body of tweet
    mars_weather = soup.find('p', class_="tweet-text").text

    # Store sub-element which contains the picture
    image = soup.find('a', class_="twitter-timeline-link")

    # Remove the image from the tweet, leaving only the text
    mars_weather = mars_weather.replace(image.text, '')

    # Reformat text to replace new lines with commas
    mars_weather = mars_weather.replace('\n', ', ')


    # ### 1d. Mars Facts
    # 
    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string.

    # Assign the URL to a variable
    facts_url = 'https://space-facts.com/mars/'

    # Read the html using Pandas, store into a list of DataFrames
    tables = pd.read_html(facts_url)

    # Assign the first (and only) table to a DataFrame
    mars_facts_df = tables[0]

    # Create column headers
    mars_facts_df.columns = ['Description', 'Value']

    # Set the index to the Description column
    mars_facts_df.set_index('Description', inplace=True)

    # Create html code for table
    mars_table = mars_facts_df.to_html()


    # ### 1e. Mars Hemispheres
    # 
    # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name.
    # Use a Python dictionary to store the data using the keys img_url and title. 
    # Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    # Assign path for chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}

    # Assign browser variable
    browser = Browser('chrome', **executable_path, headless=True)

    # Assign URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Declare empty list to store dictionaries
    hemisphere_image_urls = []

    # Define list of names for use in navigation
    name_list = ['Cerberus','Schiaparelli','Syrtis Major','Valles Marineris']

    for name in name_list:
        
        # Navigate to URL
        browser.visit(url)

        # Assign html code to variable
        html = browser.html

        # Navigate to the target page
        browser.click_link_by_partial_text(name)

        # Assign html code to variable
        html = browser.html

        # Create BS object
        soup = BeautifulSoup(html, 'html.parser')

        # Assign the title text
        title = soup.find('h2', class_="title").text

        # Assign partial URL using image source
        partial_url = soup.find('img', class_="wide-image")['src']
        
        # Construct full image URL
        img_url = "https://astrogeology.usgs.gov" + partial_url    
        
        # Define dictionary object
        image_dict = {
                    "title": title,
                    "img_url": img_url
                    }
        
        # Append dictionary to list
        hemisphere_image_urls.append(image_dict)

    # Close browser window
    browser.quit()


    # ### ...return one Python dictionary containing all of the scraped data

    # Create dictionary containing all scraped data
    scraped_data = {"first_article_title": first_article_title,
                    "first_article_teaser": first_article_teaser,
                    "featured_image_url": featured_image_url,
                    "mars_weather": mars_weather,
                    "mars_table": mars_table,
                    "hemisphere_image_urls": hemisphere_image_urls
                }

    # Return all scraped data
    return(scraped_data)