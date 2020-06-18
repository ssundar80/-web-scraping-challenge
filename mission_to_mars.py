def scrape():
    #Import Libraries
    import pandas as pd
    from splinter import Browser as browser
    from bs4 import BeautifulSoup as bs
    import requests
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    import time
    import pymongo
    import requests
    from bs4 import BeautifulSoup

    # # Step 1 -- NASA Mars News Scraping

    # NASA Mars News Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

    article_header = 'slide'
    content_title = 'content_title'
    content_body = 'article_teaser_body'
    wait_element = 'news'
    driver = webdriver.Chrome('/Users/samir/Desktop/Web-Scraping-Challenge/Missions_to_Mars/chromedriver.exe')
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    driver.get(url)
    time.sleep(10)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID,wait_element))
        )
    except:
        pass

    slide = driver.find_elements_by_class_name(article_header)[0]

    first_article_headline = slide.find_element_by_class_name(content_title).text
    first_article_headline
    first_article_paragraph = slide.find_element_by_class_name(content_body).text
    first_article_paragraph


    # # Step 2 -- JPL Mars Space Images - Featured Image
    # Visit the url for JPL Featured Space Image https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars.
    # Use request to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    # Make sure to find the image url to the full size .jpg image.
    # Make sure to save a complete url string for this image.

    # URL of page to be scraped
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    featured_image_response = requests.get(featured_image_url)

    if featured_image_response.status_code == 200:
        featured_image_html = featured_image_response.text

    featured_image_soup = BeautifulSoup(featured_image_html, "html.parser")
    image_element = featured_image_soup.find("a", {"class": "button fancybox"}).get('data-fancybox-href')
    "https://www.jpl.nasa.gov" + image_element


    # ### Mars Weather
    # 
    # * Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.
    # 
    # ```python
    # # Example:
    # mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
    # ```

    # URL of page to be scraped
    weather_tweets_url = "https://twitter.com/marswxreport?lang=en"
    driver = webdriver.Chrome('/Users/samir/Desktop/Web-Scraping-Challenge/Missions_to_Mars/chromedriver.exe')
    driver.get(weather_tweets_url)
    time.sleep(10)

    mars_weather = driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div/div/div/div/div/div[2]/section/div/div/div/div[1]/div/div/div/article/div/div[2]/div[2]/div[2]/div[1]/div/span")
    
    weather_tweet = mars_weather.text
    weather_tweet


    # ### Mars Facts
    # 
    # * Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # 
    # * Use Pandas to convert the data to a HTML table string.

    # URL of page to be scraped
    mars_fact_url = "https://space-facts.com/mars/"

    #Use the read_html function in Pandas to automatically scrape any tabular data from a page.
    all_mars_fact_tables = pd.read_html(mars_fact_url)

    #Return the table with Mars general information, assign it to a dataframe
    df_mars= all_mars_fact_tables[0]
    df_mars.columns=["Measurement", "Value"]
    df_mars


    #Use the to_html method to generate HTML tables from DataFrames.
    html_table = df_mars.to_html()
    html_table


    #Strip unwanted newlines to clean up the table.
    html_table.replace('\n', '')


    # ### Mars Hemispheres
    # 
    # * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
    # 
    # * You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # 
    # * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
    # 
    # * Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.


    #Create variables to store the dictionaries
    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    mars_hemisphere_response = requests.get(mars_hemisphere_url)
    if mars_hemisphere_response.status_code == 200:
        mars_hemisphere_html = mars_hemisphere_response.text



    def get_full_image_link(link):
        response = requests.get(link)
        if response.status_code == 200:
            html = response.text
        soup = BeautifulSoup(html, "html.parser")
        img_link = soup.find("a", text="Original").get("href")
        return img_link

    #Get a list of all fill page links
    mars_hemisphere_soup = BeautifulSoup(mars_hemisphere_html, "html.parser")
    link_elements = mars_hemisphere_soup.findAll("a", {"class": "itemLink product-item"})
    full_page_links = ["https://astrogeology.usgs.gov" + le.get('href') for le in link_elements]
    full_page_links


    def get_full_image_link(link):
        response = requests.get(link)
        if response.status_code == 200:
            html = response.text
        soup = BeautifulSoup(html, "html.parser")
        img_link = soup.find("a", text="Original").get("href")
        title = soup.find("h2", class_="title").text.split(" Enhanced")[0]
        return [title, img_link]


    mars_hemisphere_soup = BeautifulSoup(mars_hemisphere_html, "html.parser")
    link_elements = mars_hemisphere_soup.findAll("a", {"class": "itemLink product-item"})
    title_img_url_dict = [dict(title=get_full_image_link("https://astrogeology.usgs.gov" + le.get('href'))[0], img_url=get_full_image_link("https://astrogeology.usgs.gov" + le.get('href'))[1]) for le in link_elements]
    title_img_url_dict

    




