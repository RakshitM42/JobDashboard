#Importing libraries 
import pandas as pd
import numpy as np
import os
import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
import time
from bs4 import BeautifulSoup
import requests
import random
import bs4
import hashlib

# Part - A Initialize browser
browser = webdriver.Chrome()

# Navigating to the first page
url = "https://www.workopolis.com/jobsearch/find-jobs?ak=data%20analyst&l=&job=LcF3JDsXy2Rw8PXAtviT1-yE0yobxA0Chxxf4ptiikK1ObJFguHMLol_XZvkC1rP"
browser.get(url)
time.sleep(5)  # Wait for the first page to load

job_company = []
job_location = []


# Create a dictionary to store company names and their corresponding IDs
company_ids = {}

# Function to generate a consistent ID for a given company name using MD5 hash
def generate_id(job_company):
    hash_value = hashlib.md5(job_company.encode()).hexdigest()
    return int(hash_value, 16) % 1000000  # Generate IDs within the range of 0 to 999999


# Page counter
current_page = 1
max_pages = 50

# Continue looping through pages until max_pages is reached
while current_page <= max_pages:
    # Give it some time to load
    time.sleep(random.randint(5, 10))  # Random sleep interval between 5 to 10 seconds
    # Mock action: Print the current page number and URL
    #print(f"Currently on page {current_page}")
    #print(browser.current_url)

    # Extracting data from current page
    html_page = browser.page_source
    soup = BeautifulSoup(html_page, 'html.parser')
    
    # 1 - COMPANIES 
    companies = soup.findAll("div", class_="SerpJob-property SerpJob-company")
    for comp in companies:
        job_company.append(comp.text.strip())


    # 3 lOCATION
    locations = soup.findAll("span", class_="SerpJob-property SerpJob-location")  
    for l in locations:
        job_location.append(l.text.strip())

 
    # Move to the next page
    try:
        next_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.Pagination-link.Pagination-link--next'))
        )
        next_button.click()
        time.sleep(5)  # Wait for the next page to load
    except:
        # If "Next" arrow is not found or is not clickable, break the loop
        print("Could not find the 'Next' arrow or the next page didn't load in time. Exiting.")
        break

    # Increment the page counter
    current_page += 1

# Generate IDs for each company name
for name in job_company:
    company_ids[name] = generate_id(name)

# # # Create a DataFrame named "company_id_df"
# company_id_df = pd.DataFrame({"Company": job_company, "ID": [company_ids[name] for name in job_company]})

# # Print the DataFrame
# print(company_id_df)

# Part B - Initialize browser
browser = webdriver.Chrome()

# Going to plus code website
url = "https://plus.codes/map"
browser.get(url)
time.sleep(5)

search_box = browser.find_element(by="xpath", value='//*[@id="search-input"]')
time.sleep(2)

LatLong_data = []

# Clear the search box to ensure the previous query doesn't interfere with the next one
search_box.clear()
search_box.send_keys("Cibc" + ", " + "Toronto")

search_box.send_keys(Keys.RETURN)
time.sleep(2)  # Allow the results to load.

expand_icon = browser.find_element(by="xpath", value='//*[@id="summary"]/div[1]').click()
time.sleep(2)  # Allow the section to expand.

# For searching again with Second Page
for company, location in zip(job_company, job_location):
    search_box = browser.find_element(by="xpath", value='//*[@id="search-input"]')
    time.sleep(2)
    
    # Clear the search box to ensure the previous query doesn't interfere with the next one
    search_box.clear()
    search_box.send_keys(company + ", " + location)
    
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Allow the results to load.


    # Extract the details
    LatLong = browser.find_element(by="xpath", value='//*[@id="placecard-details"]/div[3]/div[1]').text
    LatLong_data.append({            
        #"Company": company,
        #"Location": location,
     LatLong
    })
    #print(f"{company}, {location}: {LatLong}")

browser.close()  # Close the browser after the loop

# Create a DataFrame from the collected data

df = pd.DataFrame({
    'Location': job_location,
    'Company': job_company,
    'Coordinates': LatLong_data,
    "ID": [company_ids[name] for name in job_company]
})

df.to_csv('B-1.csv', index=False)
browser.quit()
# Print the DataFrame
print(df)
