import csv
import os
from selenium import webdriver
import time


errorlog_file_path = "/home/bozhi/Documents/seleniumRoblox/popularGames/redownload/"
redownload_folder_name = "redownload"

driver = webdriver.Chrome("/home/bozhi/Documents/seleniumRoblox/chromedriver")

def main():

	os.chdir(errorlog_file_path)
	
	game_url= []
	file_name = []

	with open("errorLog.csv","r") as f:
		reader = csv.reader(f)
		next(reader, None)
		for row in reader:
			id_tab_string = row[0][:-5].rsplit("/",1)[1]
			_id = id_tab_string.split("_",1)[0]
			tab = id_tab_string.split("_",1)[1]
			url = "https://www.roblox.com/games/"+_id+"/#!/"+tab
			game_url.append(url)
			file_name.append(id_tab_string+".html")

	if not os.path.exists(redownload_folder_name):
		os.mkdir(redownload_folder_name)

	os.chdir(redownload_folder_name)

	for i in range(len(game_url)):
		driver.get(game_url[i])
		time.sleep(6)
		html = driver.page_source
		with open(file_name[i],"w") as f:
			f.write(html)
		time.sleep(2)

	os.remove(errorlog_file_path+"errorLog.csv")

if __name__ == '__main__':
	main()
