import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import io

#normally if webdriver executable is placed in the same directory, filepath is not necessary
#for it to work. If not, replace it with your own chromedriver file path
driver = webdriver.Chrome("/home/bozhi/Documents/seleniumRoblox/chromedriver")

#current page contains popular games with no gener filter
homePageString = "https://www.roblox.com/games/?SortFilter=1&TimeFilter=0&GenreFilter=1"




def main():

	home = driver.get(homePageString)

	time.sleep(5)
	
	#60 games without scroll, each additional scroll brings in addtional 60 games
	#current: 8 * 60 + 60 = 540 games

	for i in range(8):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(3)
	
	html = driver.page_source
	soup = BeautifulSoup(html,'lxml')
	
	gameLinks = []
	aboutUrls = []
	storeUrls = []
	leaderboardsUrls = []
	serverUrls = []

	for href in soup.find_all('a',{'class':'game-card-link'}):
		gameLinks.append(href['href'])

	for i in range(len(gameLinks)):
		aboutUrls.append(gameLinks[i])#about
		storeUrls.append(gameLinks[i]+"#!/store")#store
		leaderboardsUrls.append(gameLinks[i]+"#!/leaderboards")#leaderboards
		serverUrls.append(gameLinks[i]+"#!/game-instances")#server

	for i in range(len(gameLinks)):
		#print(aboutUrls[i])
		driver.get(aboutUrls[i])
		about_html = driver.page_source
		time.sleep(2)
		with open(getGameID(gameLinks[i])+"_about.html",'w') as f:
			f.write(about_html)
		time.sleep(2)
		
		#print(storeUrls[i])
		driver.get(storeUrls[i])
		store_html = driver.page_source
		with open(getGameID(gameLinks[i])+"_store.html",'w') as f:
			f.write(store_html)
		time.sleep(2)

		#print(leaderboardsUrls[i])
		driver.get(leaderboardsUrls[i])
		time.sleep(5)
		leaderboards_html = driver.page_source
		with open(getGameID(gameLinks[i])+"_leaderboards.html",'w') as f:
			f.write(leaderboards_html)
		time.sleep(2)
		
		#print(serverUrls[i])
		driver.get(serverUrls[i])
		server_html = driver.page_source
		with open(getGameID(gameLinks[i])+"_server.html",'w') as f:
			f.write(server_html)
		time.sleep(2)

def getGameID(gameUrl):
	gameID = gameUrl.rsplit("PlaceId=", 1)[1].split("&", 1)[0]
	return gameID


if __name__ == '__main__':
    main()	