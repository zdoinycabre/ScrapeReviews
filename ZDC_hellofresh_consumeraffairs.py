# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 08:43:29 2020

@author: chudc
"""

from bs4 import BeautifulSoup
import requests
import csv
import time
import random

#user defined function to scrape the fields of the review we are interested in
#and store them in a dictionary
def scrape_one_page(reviews,csvwriter):
    for review in reviews:
        dictionary_reviews = {}
        username = review.find('strong', attrs={'class':'rvw-aut__inf-nm'}).string
        rating = review.find_all('meta')[1].get('content')
        date = review.find('span', attrs={'class': 'ca-txt-cpt'}).get_text()
        content = review.find('div',attrs={'class' : 'rvw-bd'}).get_text()
        dictionary_reviews['Username'] = username
        dictionary_reviews['Rating'] = rating
        dictionary_reviews['Date'] = date
        dictionary_reviews['Review'] = content
        review_writer.writerow(dictionary_reviews.values())
        
#Here I created a list with all the URL to scrape
url_list = ['https://www.consumeraffairs.com/food/hellofresh.html']
for i in range(2,39,1):
     url_list.append('https://www.consumeraffairs.com/food/hellofresh.html?page='+str(i))

#Created a csv file to save the reviews scraped
with open('hellofresh.csv','w',encoding = 'utf-8',newline='') as csvfile:
     review_writer = csv.writer(csvfile)
     review_writer.writerow(['reviewUsername', 'reviewRating', 'reviewDate','reviewText'])
     for index, url in enumerate(url_list):
         #here I requested to open the different URLs and created an objet with all the information from each page.
         response = requests.get(url).text
         soup = BeautifulSoup(response, 'html.parser')
         #this is to find all the div reviews in the website
         reviews = soup.find_all('div', attrs={'class':'rvw js-rvw'})
         #called the function that scrapes the username, rating and review 
         scrape_one_page(reviews,review_writer)
         #randomsleep to avoid getting banned from the server
         time.sleep(random.randint(1,3))
         print('Finished page' + str(index + 1))

     csvfile.close()

