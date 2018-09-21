# this is our transcriped IPythonNoteBook script
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import os
import pymongo
import pprint
import urllib.request
import time
from splinter import Browser
browser = Browser('chrome')


def scrape()

	# define a dictionary variable to hold the results of the scraaping
	mars_collection = {}

	# establish all the urls used to scrape the information
	url1 = 'https://mars.nasa.gov/news/'
	url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	url3 = 'https://twitter.com/marswxreport?lang=en'
	url4 = 'http://space-facts.com/mars/'
	url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


	# scrape data from site 1
	browser.visit(url1)

	html = browser.html
	soup = bs(html,"html.parser")

	news_title = soup.find("div",class_="content_title").text
	news_paragraph = soup.find("div", class_="article_teaser_body").text
	
	# insert data from site 1 into a column of the dictionary 
	mars_collection['news_title'] = news_title
    mars_collection['news_paragraph'] = news_paragraph




    # begin the scraping process for site 2
	r = requests.get(url2)
	html_content = r.text
	soup = bs(html_content,"html.parser")

	browser.visit(url2)
	browser.find_by_id('full_image').click()
	featured_image_url = browser.find_by_css('.fancybox-image').first['src']
	
	# insert the results into a column of the dictionary 
	mars_collection['featured_image_url'] = featured_image_url




	# Start scraping for Mars weather
	browser.visit(url3)
	for text in browser.find_by_css('.tweet-text'):
	    if text.text.partition(' ')[0] == 'Sol':
	        mars_weather = text.text
	        break
	
	mars_collection['mars_weather'] = mars_weather

	


	df = pd.read_html(url4, attrs = {'id': 'tablepress-mars'})[0]
	df = df.set_index(0).rename(columns={1:"value"})
	del df.index.name
	mars_facts = df.to_html()

	mars_collection['mars_facts'] = mars_facts
	



	browser.visit(url5)
	first = browser.find_by_tag('h3')[0].text
	second = browser.find_by_tag('h3')[1].text
	third = browser.find_by_tag('h3')[2].text
	fourth = browser.find_by_tag('h3')[3].text

	browser.find_by_css('.thumb')[0].click()
	first_img = browser.find_by_text('Sample')['href']
	browser.back()

	browser.find_by_css('.thumb')[1].click()
	second_img = browser.find_by_text('Sample')['href']
	browser.back()

	browser.find_by_css('.thumb')[2].click()
	third_img = browser.find_by_text('Sample')['href']
	browser.back()

	browser.find_by_css('.thumb')[3].click()
	fourth_img = browser.find_by_text('Sample')['href']

	hemisphere_image_urls = [
	    {'title': first, 'img_url': first_img},
	    {'title': second, 'img_url': second_img},
	    {'title': third, 'img_url': third_img},
	    {'title': fourth, 'img_url': fourth_img}
	]

	mars_collection['hemisphere_image_urls'] = hemisphere_image_urls

	mars_results = {
		"news_title": mars_collection['news_title'], 
    	"news_paragraph": mars_collection['news_paragraph']
    	"featured_image_url": mars_collection['featured_image_url']
    	"mars_weather": mars_collection['mars_weather']
    	"mars_facts": mars_collection['mars_facts']
    	"hemisphere_image_urls": mars_collection['hemisphere_image_urls']
	}


	return mars_results 

