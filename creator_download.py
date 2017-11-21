import csv
import re
import os
import glob
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementNotVisibleException


about_csv_file_file_path = "/home/bozhi/Documents/seleniumRoblox/popularGames/redownload/"
about_csv_file_file_name = "about_data.csv"
creator_html_file_path = "/home/bozhi/Documents/seleniumRoblox/popularGames/redownload/creators"

driver = webdriver.Chrome("/home/bozhi/Documents/seleniumRoblox/chromedriver")

creator_url = []
individual_url = []
group_url = []

def main():
	with open(about_csv_file_file_path+about_csv_file_file_name,"r") as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			try:
				creator_url.append(row[7][:-1])
			except IndexError:
				pass

	for url in creator_url:
		if "groups" in url:
			group_url.append(url)
		else:
			individual_url.append(url)

	os.chdir(creator_html_file_path)
	'''
	for url in group_url:
		creator_id = url.rsplit("gid=", 1)[1]
		driver.get(url)
		if page_error(url) is False:
			time.sleep(2)
			main_html = driver.page_source
			print(url)
			with open("group_"+creator_id+"_main.html","w") as f:
				f.write(main_html)
			clan_tab = driver.find_elements_by_css_selector('div#GroupsPeople_Clan')
			if len(clan_tab) > 0:
				clan_tab[0].click()
				time.sleep(2)
				clan_html = driver.page_source
				print(url)
				with open("group_"+creator_id+"_clan.html","w") as f:
					f.write(clan_html)
	'''

	for url in individual_url:
		creator_id = url.rsplit("/", 1)[0].rsplit("/", 1)[1]
		driver.get(url)
		if page_error(url) is False:
			print(url)
			time.sleep(3)
			grid_view_button = driver.find_element_by_xpath('//div[@class="tab-pane active"]//button[@class="profile-view-selector btn-control-xs"][@title="Grid View"]')
			try:
				grid_view_button.click()
			except ElementNotVisibleException:
				pass
			time.sleep(2)
			load_more_button = driver.find_elements_by_xpath('//div[@class="tab-pane active"]//a[@class="btn btn-control-xs load-more-button ng-scope"]')
			while len(load_more_button) > 1:
				try:
					load_more_button[0].click()
					load_more_button = driver.find_elements_by_xpath('//div[@class="tab-pane active"]//a[@class="btn btn-control-xs load-more-button ng-scope"]')
				except ElementNotVisibleException:
					pass
			time.sleep(2)
			print(url)
			about_html = driver.page_source
			with open("individual_"+creator_id+"_about.html","w") as f:
				f.write(about_html)
			creation_tab = driver.find_element_by_id("tab-creations")
			try:
				creation_tab.click()
			except ElementNotVisibleException:
				pass
			time.sleep(3)
			grid_view_button = driver.find_element_by_xpath('//div[@class="tab-pane active"]//button[@class="profile-view-selector btn-control-xs"][@title="Grid View"]')
			try:
				grid_view_button.click()
			except ElementNotVisibleException:
				pass
			time.sleep(2)
			load_more_button = driver.find_elements_by_xpath('//div[@class="tab-pane active"]//a[@class="btn btn-control-xs load-more-button"]')
			try:
				while len(load_more_button) > 1:
					load_more_button[0].click()
			except ElementNotVisibleException:
				pass
			time.sleep(2)
			creation_html = driver.page_source
			with open("individual_"+creator_id+"_creations.html","w") as f:
				f.write(creation_html)


def page_error(url):
	error_message = driver.find_elements_by_class_name("error-message")
	if len(error_message) > 0:
		with open("download_errorlog.csv","a") as f:
			writer = csv.writer(f)
			writer.writerow([url,error_message[0].text])
		return True
	else:
		return False

if __name__ == '__main__':
	main()
