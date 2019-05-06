# author = 'Erin Dugan'
# modified by 'Rui Liu'
# 2019-05-06

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
import sys
from selenium.common.exceptions import NoSuchElementException

argvalue = 1
endpage = 1000

index = argvalue

driver = webdriver.Chrome()
driver2 = webdriver.Chrome()


driver.get("https://www.petfinder.com/search/cats-for-adoption/us/ny/11790/?page=" + str(index))

csv_file = open('pets_Denver10mi_' + str(index) + '.csv', 'w')
writer = csv.writer(csv_file)

#STEPS:
# 1 - From search result page - Click each dog's pic (pet_tile) to go to its page
# 2 - Scrape individual page
# 3 - Return to result page, select next pet until no more on page
# 4 - Next page, then repeat until no more pages

while index <= endpage:  #While Next button is at bottom of page
	try:
		print("Scraping Page #: " + str(index))
		index = index + 1

		# Find all the pets on the page
		pet_tiles = driver.find_elements_by_xpath('//a[@class="petCard-overlay-link"]')
		pets = [x.get_attribute("href") for x in pet_tiles]

		for pet in pets:   # Find all the info on each pet's page
			driver2.get(pet)
			pet_dict = {}  #initialize dictionary

			try:
				name = driver2.find_element_by_xpath('.//h1[@id="Detail_Main"]').text
			except NoSuchElementException:
				name = 0

			try:
			    organization = driver2.find_element_by_xpath('.//pf-truncate[@line-count="3"]').text
			except NoSuchElementException:
			    organization = 0

			try:
			    story = driver2.find_element_by_xpath('(.//div[@class="u-vr4x"])[2]').text
			except NoSuchElementException:
			    story = 0

			try:
				info1 = driver2.find_element_by_xpath('.//div[@class="card-section-inner"]').text
			except NoSuchElementException:
			    info1 = 0

			try:
				info2 = driver2.find_element_by_xpath('//div[@class="grid grid_gutterLg u-vr4x"]').text
			except NoSuchElementException:
			    info2 = 0

			try:
				script_info = driver2.find_elements_by_tag_name("script")
				info_all = 0
				for elem in script_info:
					if "published_at" in elem.get_attribute("innerHTML"):
						info_all = elem.get_attribute("innerHTML")
			except NoSuchElementException:
			    info_all = 0

			pet_dict['name'] = name
			pet_dict['organization'] = organization
			pet_dict['info1'] = info1
			pet_dict['info2'] = info2
			pet_dict['story'] = story
			pet_dict['info_all'] = info_all

			writer.writerow(pet_dict.values())  #writing to csv file

		# Locate the next button on the page.
		wait_button = WebDriverWait(driver, 10)
		next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,'.//button[@class="fieldBtn fieldBtn_altHover m-fieldBtn_iconRt m-fieldBtn_tight m-fieldBtn_full"]')))
		next_button.click()
		time.sleep(1)   #1-second wait while page loads

	except Exception as e:
		print(e)
		csv_file.close()
		driver.close()
		driver2.close()
		break

