import csv
import re
import os
import glob
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import multiprocessing

file_path = "/home/bozhi/Documents/seleniumRoblox/popularGames/redownload/creators/"
indie_creation_file_name = "indie_creation.csv"
group_creation_file_name = "group_creation.csv"
download_folder_path = "/home/bozhi/Documents/seleniumRoblox/popularGames/redownload/creators/secondtier"

driver = webdriver.Chrome("/home/bozhi/Documents/seleniumRoblox/chromedriver")
driver1 = webdriver.Chrome("/home/bozhi/Documents/seleniumRoblox/chromedriver")

indie_game_url = []
group_game_url = []

def main():
	with open(file_path+indie_creation_file_name,"r") as f:
		reader = csv.reader(f)
		next(reader)
		for row in reader:
			try:
				indie_game_url.append(row[5])
			except IndexError:
				pass

	with open(file_path+group_creation_file_name,"r") as f:
		reader = csv.reader(f)
		next(reader)
		for row in reader:
			try:
				group_game_url.append(row[5])
			except IndexError:
				pass

	indie_game_id = get_indie_game_id(indie_game_url)
	group_game_id = get_group_game_id(group_game_url)

	os.chdir(download_folder_path)
	indie_process = multiprocessing.Process(target=download, args=(indie_game_url, indie_game_id, driver))
	group_process = multiprocessing.Process(target=download, args=(group_game_url, group_game_id, driver1))
	indie_process.start()
	group_process.start()
	
def get_indie_game_id(game_url):
	game_id = []
	for i in range(len(game_url)):
		game_id.append(game_url[i].rsplit("PlaceId=", 1)[1].split("&", 1)[0])
	return game_id

def get_group_game_id(game_url):
	game_id = []
	for i in range(len(game_url)):
		game_id.append(game_url[i].rsplit("/", 2)[1])
	return game_id

def download(game_url, game_id, driver):

	about_url = []
	store_url = []
	leaderboard_url = []


	for i in range(len(game_url)):
		about_url.append(game_url[i])#about
		store_url.append(game_url[i]+"#!/store")#store
		leaderboard_url.append(game_url[i]+"#!/leaderboards")#leaderboards

	for i in range(len(game_url)):
		#print(about_url[i])
		driver.get(about_url[i])
		about_html = driver.page_source
		time.sleep(3)
		with open(game_id[i]+"_about.html",'w') as f:
			f.write(about_html)
		time.sleep(2)
		
		#print(store_url[i])
		driver.get(store_url[i])
		store_html = driver.page_source
		time.sleep(3)
		with open(game_id[i]+"_store.html",'w') as f:
			f.write(store_html)
		time.sleep(2)

		#print(leaderboard_url[i])
		driver.get(leaderboard_url[i])
		time.sleep(5)
		leaderboards_html = driver.page_source
		with open(game_id[i]+"_leaderboards.html",'w') as f:
			f.write(leaderboards_html)
		time.sleep(2)
		

if __name__ == '__main__':
	main()