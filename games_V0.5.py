from bs4 import BeautifulSoup
import csv
import re
import os
import glob
import multiprocessing

#csv output directory
base_path = "/home/bozhi/Documents/seleniumRoblox/popularGames/"
#downloaded html directory
file_path = base_path + "redownload/"
#/creators/secondtier/


about_file_name = "about_data"
recommendedGames_file_name = "recommendedGames_data"
gameBadges_file_name = "badges_data"
store_file_name = "store_data"
playerLeaderboards_file_name = "playerLeaderboards_data"
clanLeaderboards_file_name = "clanLeaderboards_data"

def main():

	WriteGameAboutCsvHeader(base_path,about_file_name)
	WriteRecommendedGamesCsvHeader(base_path,recommendedGames_file_name)
	WriteGameBadgesCsvHeader(base_path,gameBadges_file_name)
	WriteGameStoreCsvHeader(base_path,store_file_name)
	WritePlayerLeaderboardsCsvHeader(base_path, playerLeaderboards_file_name)
	WriteClanLeaderboardsCsvHeader(base_path, clanLeaderboards_file_name)
	WriteErrorLogCsvHeader(base_path)

	os.chdir(file_path)

	for file_type in glob.glob('*.html'):

		#print(file_path+file_type)
		gameID = GetGameID(file_type)
		soup = ReadHTML(file_type)

		game_heading = GetGameName(soup)

		if game_heading is None:
			write_errorlog(file_path+file_type)

		else:
			gameName = game_heading.text
			if '_about' in file_type:
				print(file_type)
				aboutP = multiprocessing.Process(target=ProcessAbout, args=(soup, gameID, gameName, base_path+about_file_name,file_path+file_type))
				recommendedGamesP = multiprocessing.Process(target=ProcessRecommendedGames, args=(soup, gameID, gameName, base_path+recommendedGames_file_name))
				gameBadgesP = multiprocessing.Process(target=ProcessGameBadges, args=(soup, gameID, gameName, base_path+gameBadges_file_name))
				try:
					aboutP.start()
				except UnboundLocalError:
					write_errorlog(file_path+file_type)
					pass
				recommendedGamesP.start()
				gameBadgesP.start()

			#elif '_server' in file_type:

			elif '_store' in file_type:
				print(file_type)
				storeP = multiprocessing.Process(target=ProcessStore, args=(soup, gameID, gameName, base_path+store_file_name,))
				storeP.start()

			elif '_leaderboards' in file_type:
				print(file_type)
				playerLeaderboardsP = multiprocessing.Process(target=ProcessPlayersLeaderboards, args=(soup, gameID, gameName, base_path+playerLeaderboards_file_name,))
				clanLeaderboardsP = multiprocessing.Process(target=ProcessClansLeaderboards, args=(soup, gameID, gameName, base_path+clanLeaderboards_file_name,))
				playerLeaderboardsP.start()
				clanLeaderboardsP.start()

def WriteErrorLogCsvHeader(base_path):
	file = base_path+"/"+"errorLog.csv"
	if not os.path.exists(file):
		header = ["File_Location"]
		with open(file,"w+") as f:
			dw = csv.DictWriter(f, fieldnames = header)
			dw.writeheader()

def write_errorlog(file_location):
	with open(base_path+"/"+"errorLog.csv","a") as f:
		writer = csv.writer(f)
		writer.writerow([file_location])


def WriteGameAboutCsvHeader(base_path, file_name):
	file = base_path+"/"+file_name+".csv"
	if not os.path.exists(file):
		header = ["Game_ID","Game_Name","Free_Paid","Price","Creator_ID","Creator_Name","Creator_Type","Creator_Url","Favorited_Times","Upvotes","Downvotes","Playing","Visits","Created_Date","Last_Update","Max_Player","Genre","Genre_Url","Gear","Description"]
		with open(file,"w+") as f:
			dw = csv.DictWriter(f, fieldnames = header)
			dw.writeheader()

def WriteRecommendedGamesCsvHeader(base_path, file_name):
	file = base_path+"/"+file_name+".csv"
	if not os.path.exists(file):
		header = ["Game_ID","Game_Name","Recommended_Game_ID","Recommended_Game_Name","Recommended_Game_Url"]
		with open(file,"w+") as f:
			dw = csv.DictWriter(f, fieldnames = header)
			dw.writeheader()

def WriteGameBadgesCsvHeader(base_path, file_name):
	file = base_path+"/"+file_name+".csv"
	if not os.path.exists(file):
		header = ["Game_ID","Game_Name","Badge_Name","Badge_Description","Badge_Rarity","Badge_Won_Yesterday","Ever"]
		with open(file,"w+") as f:
			dw = csv.DictWriter(f, fieldnames = header)
			dw.writeheader()

def WriteGameStoreCsvHeader(base_path, file_name):
	file = base_path+"/"+file_name+".csv"
	if not os.path.exists(file):
		header = ["Game_ID","Game_Name","Pass_ID","Pass_Name","Pass_Url","Pass_Price"]
		with open(file,"w+") as f:
			dw = csv.DictWriter(f, fieldnames = header)
			dw.writeheader()

def WritePlayerLeaderboardsCsvHeader(base_path, file_name):
	file = base_path+"/"+file_name+".csv"
	if not os.path.exists(file):
		header = ["Game_ID","Game_Name","Player_ID","Player_Name","Player_Url","Player_Group","Rank","Points"]
		with open(file,"w+") as f:
			dw = csv.DictWriter(f, fieldnames = header)
			dw.writeheader()

def WriteClanLeaderboardsCsvHeader(base_path, file_name):
	file = base_path+"/"+file_name+".csv"
	if not os.path.exists(file):
		header = ["Game_ID","Game_Name","Clan_ID","Clan_Name","Clan_Url","Clan_Owner","Rank","Points"]
		with open(file,"w+") as f:
			dw = csv.DictWriter(f, fieldnames = header)
			dw.writeheader()

def ReadHTML(file_type):
	try:
		page = open(file_type).read()
		soup = BeautifulSoup(page,"lxml")
		return soup
	except Exception:
		print("Exception")
		pass
	except AttributeError:
		print("AttributeError")
		pass
	except TypeError:
		print("TypeError")
		pass

def GetGameID(file_type):
	gameID = file_type.split("_",1)[0]
	return gameID

def GetGameName(soup):
	gameName = soup.find("h2",{"class":"game-name"})
	return gameName

def ProcessAbout(soup, gameID, gameName, csv_directory, file_location):

	voting_spinner = soup.find("span",{"class":"voting-panel spinner spinner-default"})
	if voting_spinner is not None:
		write_errorlog(file_location)
		return
		
	row = []
	table = []

	payToPlay = soup.find("div",{"id":"PurchaseRequired"})

	if payToPlay:
		for span in payToPlay.find_all("span"):
			price = span["data-expected-price"]
			paidOrFree = "Paid"
	else:
		paidOrFree = "Free"
		price = "0"

	for div in soup.find_all("div",{"class":"game-creator"}):
		creatorInfo = div.find("a",{"class":"text-name"})
		creatorName = creatorInfo.text
		creatorUrl = creatorInfo['href']
		if "gid=" in creatorUrl:
			creatorID = creatorUrl.rsplit("gid=",1)[1]
			creatorType = "Group"
		else:
			creatorID = creatorUrl.rsplit("/", 1)[0].rsplit("/", 1)[1]
			creatorType = "Individual"

	for favorite in soup.find_all("a",{"id":"toggle-favorite"}):
		for favoriteInfo in soup.find_all("span",{"id":"result"}):
			favoriteCount = favoriteInfo['title']

	for voteNumbers in soup.find_all("div",{"class":"vote-numbers"}):
		for upvoteSpan in voteNumbers.find_all("span",{"id":"vote-up-text"}):
			upvoteNumber = upvoteSpan["title"]
		for downvoteSpan in voteNumbers.find_all("span",{"id":"vote-down-text"}):
			downvoteNumber = downvoteSpan["title"]

	gameDescription = soup.find("pre",{"class":"game-description linkify"}).text

	gameStats = []
	gearSpanArray = []

	for ulGameStats in soup.find_all("ul",{"class":"game-stats-container"}):
		for gear in ulGameStats.find_all("p",{"class":"text-lead stat-gears"}):
			for gearSpan in gear.find_all("span",{"data-toggle":"tooltip"}):
				gearSpanArray.append(gearSpan["data-original-title"])
		for textLead in ulGameStats.find_all("p",{"class":"text-lead"}):
			gameStats.append(textLead)

	gearStats = gearSpanArray[0]
	playing = gameStats[0].text
	visits = gameStats[1]["title"]
	dateCreated = gameStats[2].text
	lastUpdateDate = gameStats[3].text
	maxPlayers = gameStats[4].text
	genre = gameStats[5].text
	genreUrl = gameStats[5].find("a")["href"]


	row.append(gameID+"\t")
	row.append(gameName+"\t")
	row.append(paidOrFree+"\t")
	row.append(price+"\t")
	row.append(creatorID+"\t")
	row.append(creatorName+"\t")
	row.append(creatorType+"\t")
	row.append(creatorUrl+"\t")
	row.append(favoriteCount+"\t")
	row.append(upvoteNumber+"\t")
	row.append(downvoteNumber+"\t")
	row.append(playing+"\t")
	row.append(visits+"\t")
	row.append(dateCreated+"\t")
	row.append(lastUpdateDate+"\t")
	row.append(maxPlayers+"\t")
	row.append(genre+"\t")
	row.append(genreUrl+"\t")
	row.append(gearStats+"\t")
	row.append(gameDescription+"\t")
	table.append(row)

	WriteToCsv(table,csv_directory)

def ProcessRecommendedGames(soup, gameID, gameName, csv_directory):

	recommendedGamesID = []
	recommendedGamesName = []
	recommendedGamesUrl = []
	table = []
	
	for gameLinks in soup.find_all("a",{"class":"game-card-link"}):
		url = gameLinks['href']
		recommendedGamesUrl.append(url)
		recommendedGamesID.append(url.rsplit("PlaceId=", 1)[1].split("&", 1)[0])
	
	for gameNameDiv in soup.find_all("div",{"class":"text-overflow game-card-name"}):
		recommendedGamesName.append(gameNameDiv.text)

	for i in range(len(recommendedGamesID)):
		row = []
		row.append(gameID+"\t")
		row.append(gameName+"\t")
		row.append(recommendedGamesID[i]+"\t")
		row.append(recommendedGamesName[i]+"\t")
		row.append(recommendedGamesUrl[i]+"\t")
		table.append(row)

	WriteToCsv(table, csv_directory)

	
def ProcessGameBadges(soup, gameID, gameName, csv_directory):
	hasBadges = soup.find("div",{"class":"stack badge-container"})

	if hasBadges is None:
		table = [[gameID+"\t",gameName+"\t","."+"\t","."+"\t","."+"\t","."+"\t","."+"\t"]]
	else:

		badgeName = []
		badgeDescription = []
		badgeRarity = []
		wonYesterday = []
		wonEver = []
		table = []
		statsArray = []

		for badgeContent in soup.find_all("div",{"class":"badge-content"}):
			for badgeInfo in badgeContent.find_all("div",{"class":"badge-data-container"}):
				badgeName.append((badgeInfo.find("div",{"class":"badge-name"})).text)
				dscr = badgeInfo.find("p").text
				if not dscr:
					badgeDescription.append(".")
				else:
					badgeDescription.append(""+dscr+"")
			for badgeStats in badgeContent.find_all("div",{"class":"badge-stats-info"}):
				statsArray.append(badgeStats.text)
			badgeRarity.append(statsArray[0].rsplit(" (",1)[0])
			wonYesterday.append(statsArray[1])
			wonEver.append(statsArray[2])
			statsArray = []

		for i in range(len(badgeName)):
			row = []
			row.append(gameID+"\t")
			row.append(gameName+"\t")
			row.append(badgeName[i]+"\t")
			row.append(badgeDescription[i]+"\t")
			row.append(badgeRarity[i]+"\t")
			row.append(wonYesterday[i]+"\t")
			row.append(wonEver[i]+"\t")
			table.append(row)
	
	WriteToCsv(table, csv_directory)

def ProcessStore(soup, gameID, gameName, csv_directory):
	gamePassName = []
	gamePassUrl = []
	gamePassPrice = []
	gamePassId = []
	table = []

	for storeDiv in soup.find_all("div",{"id":"store"}):
		contentOff = storeDiv.find("p",{"class":"section-content-off"})

	if contentOff:
		table = [[gameID+"\t",gameName+"\t","."+"\t","."+"\t","."+"\t","."+"\t"]]
	else:
		for ul in soup.find_all("ul",{"id":"rbx-passes-container"}):
				for div in ul.find_all("div",{"class":"store-card"}):
					for a in div.find_all("a",{"class":"gear-passes-asset"}):
						url = a["href"]
						gamePassUrl.append(url)
						passId = url.rsplit("/",1)[0].rsplit("/",1)[1]
						gamePassId.append(passId)
					for caption in div.find_all("div",{"class":"store-card-caption"}):
						for passNameDiv in caption.find_all("div",{"class":"text-overflow store-card-name"}):
							gamePassName.append(passNameDiv.text)
						for priceDiv in caption.find_all("div",{"class":"store-card-price"}):
							for priceSpan in priceDiv.find_all("span",{"class":"text-robux"}):
								gamePassPrice.append(priceSpan.text)

		for i in range(len(gamePassName)):
			row = []
			row.append(gameID+"\t")
			row.append(gameName+"\t")
			row.append(gamePassId[i]+"\t")
			row.append(gamePassName[i]+"\t")
			row.append(gamePassUrl[i]+"\t")
			row.append(gamePassPrice[i]+"\t")
			table.append(row)

	WriteToCsv(table, csv_directory)
		

def ProcessPlayersLeaderboards(soup, gameID, gameName, csv_directory):
	playerId = []
	playerName = []
	playerUrl = []
	playerGroup = []
	playerPoints = []
	playerRank = []
	table = []

	for playerDiv in soup.find_all("div",{"id":"rbx-leaderboard-container-player"}):
		for sectionDiv in playerDiv.find_all("div",{"class":"section-content rbx-leaderboard-items"}):
			for lbItems in sectionDiv.find_all("div",{"class":"rbx-leaderboard-item"}):
				for rank in lbItems.find_all("div",{"class":"rank"}):
					playerRank.append(rank.text)
				for a in lbItems.find_all("a",{"class":"text-name"}):
					url = a["href"]
					playerUrl.append(url)
					_id = url.rsplit("/", 1)[0].rsplit("/", 1)[1]
					playerId.append(_id)
				for playernameSpan in lbItems.find_all("span",{"class":"name text-overflow"}):
					playerName.append(playernameSpan.text)
				for groupNameSpan in lbItems.find_all("span",{"class":"group text-overflow"}):
					if groupNameSpan.text is None:
						playerGroup.append(".")
					else:
						playerGroup.append(groupNameSpan.text)
				for pointsDiv in lbItems.find_all("div",{"class":"font-fold points"}):
					if pointsDiv.has_attr("title"):
						playerPoints.append(pointsDiv["title"])
					else:
						playerPoints.append(pointsDiv.text)


	for i in range(len(playerName)):
		row = []
		row.append(gameID+"\t")
		row.append(gameName+"\t")
		row.append(playerId[i]+"\t")
		row.append(playerName[i]+"\t")
		row.append(playerUrl[i]+"\t")
		row.append(playerGroup[i]+"\t")
		row.append(playerRank[i]+"\t")
		row.append(playerPoints[i]+"\t")
		table.append(row)

	WriteToCsv(table, csv_directory)

def ProcessClansLeaderboards(soup, gameID, gameName, csv_directory):
	clanId = []
	clanName = []
	clanUrl = []
	clanOwner = []
	clanPoints = []
	clanRank = []
	table = []

	for clanDiv in soup.find_all("div",{"id":"rbx-leaderboard-container-clan"}):
		for sectionDiv in clanDiv.find_all("div",{"class":"section-content rbx-leaderboard-items"}):
			for lbItems in sectionDiv.find_all("div",{"class":"rbx-leaderboard-item"}):
				for rank in lbItems.find_all("div",{"class":"rank"}):
					clanRank.append(rank.text)
				for a in lbItems.find_all("a",{"class":"text-name"}):
					url = a["href"]
					clanUrl.append(url)
					_id = url.rsplit("gid=",1)[1]
					clanId.append(_id)
				for clannameSpan in lbItems.find_all("span",{"class":"name text-overflow"}):
					clanName.append(clannameSpan.text)
				for clanOwnerSpan in lbItems.find_all("span",{"class":"group text-overflow"}):
					clanOwner.append(clanOwnerSpan.text)
				for pointsDiv in lbItems.find_all("div",{"class":"font-fold points"}):
					if pointsDiv.has_attr("title"):
						clanPoints.append(pointsDiv["title"])
					else:
						clanPoints.append(pointsDiv.text)

	for i in range(len(clanName)):
		row = []
		row.append(gameID+"\t")
		row.append(gameName+"\t")
		row.append(clanId[i]+"\t")
		row.append(clanName[i]+"\t")
		row.append(clanUrl[i]+"\t")
		row.append(clanOwner[i]+"\t")
		row.append(clanRank[i]+"\t")
		row.append(clanPoints[i]+"\t")
		table.append(row)

	WriteToCsv(table, csv_directory)


def WriteToCsv(input_, csv_directory):
	with open(csv_directory+".csv","a") as f:
		for i in range(len(input_)):
			writer = csv.writer(f, delimiter='\t')
			writer.writerow(input_[i])

if __name__ == '__main__':
    main()
