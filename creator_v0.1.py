from bs4 import BeautifulSoup
import csv
import re
import os
import glob

file_path = "/home/bozhi/Documents/seleniumRoblox/popularGames/redownload/creators/"

indie_about_file_name = "indie_about"
indie_about_header = ["Creator_ID","Creator_Name","Creator_Url","Friend_Count","Follower_Count","Following_Count","Join_Date","Place_Visits","Forum_Posts","Status_Text","About"]
indie_group_file_name = "indie_group"
indie_group_header = ["Creator_ID","Creator_Name","Creator_Url","Group_ID","Group_Name","Group_Url"]
indie_creation_file_name = "indie_creation"
indie_creation_header = ["Creator_ID","Creator_Name","Creator_Url","Game_ID","Game_Name","Game_Url"]
group_about_file_name = "group_about"
group_about_header = ["Group_ID","Group_Name","Group_Url","Owner_ID","Owner_Name","Owner_Url","Group_Member_Count","Clan_Member_Count","Group_Description"]
group_clan_file_name = "group_clan"
group_clan_header = ["Group_ID","Group_Name","Group_Url","Clan_Member_ID","Clan_Member_Name","Clan_Member_Url"]
group_creation_file_name = "group_creation"
group_creation_header = ["Group_ID","Group_Name","Group_Url","Game_ID","Game_Name","Game_Url"]
errorlog_file_name = "error_log"
errorlog_header = ["ID","Directory"]

def main():
	write_csv_header(indie_about_file_name,indie_about_header)
	write_csv_header(indie_group_file_name,indie_group_header)
	write_csv_header(indie_creation_file_name,indie_creation_header)
	write_csv_header(group_about_file_name,group_about_header)
	write_csv_header(group_clan_file_name,group_clan_header)
	write_csv_header(group_creation_file_name,group_creation_header)
	write_csv_header(errorlog_file_name,errorlog_header)

	os.chdir(file_path)
	for file_type in glob.glob('*.html'):
		print(file_path+file_type)
		if 'group_' in file_type:
			if '_main' in file_type:
				group_about_process(file_type)
				group_creation_process(file_type)
			elif '_clan' in file_type:
				group_clan_process(file_type)
		elif 'individual_' in file_type:
			if '_about' in file_type:
				indie_about_process(file_type)
				indie_group_process(file_type)
			elif '_creations' in file_type:
				indie_creation_process(file_type)

def get_creator_id(file_type):
	_id = file_type.rsplit("_",1)[0].rsplit("_",1)[1]
	return _id

def get_group_url(_id):
	group_url = "https://www.roblox.com/groups/group.aspx?gid="+_id
	return group_url

def get_indie_url(_id):
	indie_url = "https://www.roblox.com/users/"+_id+"/profile"
	return  indie_url


def read_html(file_type):
	try:
		page = open(file_type).read()
		soup = BeautifulSoup(page, "lxml")
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
def get_group_name(soup):
	try:
		for div in soup.find_all("div", {"class": "right-col"}):
			group_name = div.find("h2").text
		return group_name
	except UnboundLocalError:
		return None

def get_indie_name(soup):
	for header_div in soup.find_all("div", {"class": "header-caption"}):
		for title_div in header_div.find_all("div", {"class": "header-title"}):
			indie_name = title_div.find("h2").text
	return indie_name


def group_about(_id, group_url, soup, group_name):
	row = []
	table = []

	for div in soup.find_all("div", {"class": "right-col"}):
		for desc_div in div.find_all("div", {"id": "GroupDescP"}):
			group_description = desc_div.find("pre").text
		# print(group_description)

	for owner_div in soup.find_all("div", {"class": "GroupOwner"}):
		for panel_div in owner_div.find_all("div", {"id": "ctl00_cphRoblox_OwnershipPanel"}):
			owner_name = panel_div.find("a").text
			owner_url = panel_div.find("a")['href']
			owner_id = owner_url.rsplit("/", 1)[0].rsplit("/", 1)[1]
		group_member_count = owner_div.find("div", {"id": "MemberCount"}).text.rsplit(" ", 1)[1]
		clan = owner_div.find("div", {"id": "ClanMemberCount"})
		if clan is None:
			clan_member_count = 0
		else:
			clan_member_count = owner_div.find("span", {"class": "clan-members-count"}).text

	row.append(_id)
	row.append(group_name)
	row.append(group_url)
	row.append(owner_id)
	row.append(owner_name)
	row.append(owner_url)
	row.append(group_member_count)
	row.append(clan_member_count)
	row.append(group_description)
	table.append(row)

	return table

def group_creation(_id, group_url, soup, group_name):
	table = []
	game_name_array = []
	game_url_array = []
	game_id_array = []

	for div in soup.find_all("div", {"id": "GroupsPeople_Pane"}):
		for group_place in div.find_all("div", {"class": "PlaceName"}):
			game_name = group_place.find("a").text
			game_url = group_place.find("a")['href']
			game_id = game_url.rsplit("/", 2)[1]
			game_name_array.append(game_name)
			game_url_array.append(game_url)
			game_id_array.append(game_id)

	for i in range(len(game_id_array)):
		row = []
		row.append(_id)
		row.append(group_name)
		row.append(group_url)
		row.append(game_id_array[i])
		row.append(game_name_array[i])
		row.append(game_url_array[i])
		table.append(row)

	return table

def group_clan(_id, group_url, soup, group_name):
	clan_member_name_array = []
	clan_member_url_array = []
	clan_member_id_array = []
	table = []


	for clan_div in soup.find_all("div", {"id": "GroupsPeoplePane_Clan"}):
		for div in clan_div.find_all("div", {"class": "GroupMember"}):
			for span in div.find_all("span", {"class": "Name"}):
				clan_name = span.find("a").text
				clan_url = span.find("a")['href']
				clan_id = clan_url.rsplit("/", 2)[1]
				clan_member_id_array.append(clan_id)
				clan_member_url_array.append(clan_url)
				clan_member_name_array.append(clan_name)

	for i in range(len(clan_member_id_array)):
		row = []
		row.append(_id)
		row.append(group_name)
		row.append(group_url)
		row.append(clan_member_id_array[i])
		row.append(clan_member_name_array[i])
		row.append(clan_member_url_array[i])
		table.append(row)

	return table

def indie_about(_id, indie_url, soup, indie_name):
	table = []
	row = []
	social_li = []

	for header_div in soup.find_all("div", {"class": "header-caption"}):
		for details_div in header_div.find_all("div", {"class": "header-details"}):
			for ul in details_div.find_all("ul", {"class": "details-info"}):
				for a in ul.find_all("a"):
					social_li.append(a.text)

	for i in range(len(social_li)):
		if "K+" in social_li[i]:
			social_li[i] = social_li[i].rsplit("K+", 1)[0] + ",000"

	friends_count = social_li[0]
	followers_count = social_li[1]
	following_count = social_li[2]

	status_text = soup.find("span", {"id": "userStatusText"}).text
	about_text = soup.find("span", {"class": "profile-about-content-text linkify"}).text

	stats_li = []

	for li in soup.find_all("li", {"class": "profile-stat"}):
		for p in li.find_all("p", {"class": "text-lead"}):
			stats_li.append(p.text)

	join_date = stats_li[0]
	place_visits = stats_li[1]
	forum_posts = stats_li[2]

	row.append(_id)
	row.append(indie_name)
	row.append(indie_url)
	row.append(friends_count)
	row.append(followers_count)
	row.append(following_count)
	row.append(join_date)
	row.append(place_visits)
	row.append(forum_posts)
	row.append(status_text)
	row.append(about_text)
	table.append(row)

	return table

def indie_group(_id, indie_url, soup, indie_name):
	table = []
	group_name_array = []
	group_url_array = []
	group_id_array = []

	group_cards = soup.find("a", {"class": "card-item game-card-container"})
	if group_cards is None:
		group_name_array = ["."]
		group_url_array = ["."]
		group_id_array = ["."]
	else:
		for ul in soup.find_all("ul", {"class": "hlist game-cards group-list"}):
			for li in ul.find_all("li"):
				group_url = li.find("a")['href']
				group_name = li.find("div", {"class": "text-overflow game-card-name ng-binding"}).text
				group_id = group_url.rsplit("gid=", 1)[1]
				group_name_array.append(group_name)
				group_id_array.append(group_id)
				group_url_array.append(group_url)

	for i in range(len(group_id_array)):
		row = []
		row.append(_id)
		row.append(indie_name)
		row.append(indie_url)
		row.append(group_id_array[i])
		row.append(group_name_array[i])
		row.append(group_url_array[i])
		table.append(row)

	return table

def indie_creation(_id, indie_url, soup, indie_name):
	table = []
	game_id_array = []
	game_name_array = []
	game_url_array = []

	game_cards = soup.find("div", {"class": "game-container shown"})
	if game_cards is None:
		game_id_array = ["."]
		game_url_array = ["."]
		game_name_array = ["."]
	else:
		for div in soup.find_all("div", {"class": "game-grid"}):
			for ul in div.find_all("ul", {"class": "hlist game-cards"}):
				for li in ul.find_all("li"):
					game_url = li.find("a")['href']
					game_id = game_url.rsplit("PlaceId=", 1)[1].split("&", 1)[0]
					game_name = li.find("div", {"class": "text-overflow game-card-name"}).text
					game_name_array.append(game_name)
					game_url_array.append(game_url)
					game_id_array.append(game_id)

	for i in range(len(game_url_array)):
		row = []
		row.append(_id)
		row.append(indie_name)
		row.append(indie_url)
		row.append(game_id_array[i])
		row.append(game_name_array[i])
		row.append(game_url_array[i])
		table.append(row)

	return table

def group_about_process(file_type):
	_id = get_creator_id(file_type)
	group_url = get_group_url(_id)
	soup = read_html(file_type)
	group_name = get_group_name(soup)
	if group_name is None:
		write_to_csv([[_id,file_type]],errorlog_file_name)
	else:
		csv_input = group_about(_id,group_url,soup,group_name)
		write_to_csv(csv_input, group_about_file_name)

def group_creation_process(file_type):
	_id = get_creator_id(file_type)
	group_url = get_group_url(_id)
	soup = read_html(file_type)
	group_name = get_group_name(soup)
	if group_name is None:
		write_to_csv([[_id,file_type]],errorlog_file_name)
	else:
		csv_input = group_creation(_id,group_url,soup,group_name)
		write_to_csv(csv_input, group_creation_file_name)

def group_clan_process(file_type):
	_id = get_creator_id(file_type)
	group_url = get_group_url(_id)
	soup = read_html(file_type)
	group_name = get_group_name(soup)
	if group_name is None:
		write_to_csv([[_id,file_type]],errorlog_file_name)
	else:
		csv_input = group_clan(_id,group_url,soup,group_name)
		write_to_csv(csv_input, group_clan_file_name)

def indie_about_process(file_type):
	_id = get_creator_id(file_type)
	indie_url = get_indie_url(_id)
	soup = read_html(file_type)
	indie_name = get_indie_name(soup)
	if indie_name is None:
		write_to_csv([[_id, file_type]], errorlog_file_name)
	else:
		csv_input = indie_about(_id,indie_url,soup,indie_name)
		write_to_csv(csv_input, indie_about_file_name)

def indie_group_process(file_type):
	_id = get_creator_id(file_type)
	indie_url = get_indie_url(_id)
	soup = read_html(file_type)
	indie_name = get_indie_name(soup)
	if indie_name is None:
		write_to_csv([[_id, file_type]], errorlog_file_name)
	else:
		csv_input = indie_group(_id,indie_url,soup,indie_name)
		write_to_csv(csv_input, indie_group_file_name)

def indie_creation_process(file_type):
	_id = get_creator_id(file_type)
	indie_url = get_indie_url(_id)
	soup = read_html(file_type)
	indie_name = get_indie_name(soup)
	if indie_name is None:
		write_to_csv([[_id, file_type]], errorlog_file_name)
	else:
		csv_input = indie_creation(_id,indie_url,soup,indie_name)
		write_to_csv(csv_input, indie_creation_file_name)

def write_csv_header(file_name, header):
	with open(file_path+"/"+file_name+".csv","w+") as f:
		dw = csv.DictWriter(f, fieldnames = header)
		dw.writeheader()

def write_to_csv(input, file_name):
	with open(file_path+"/"+file_name+".csv","a") as f:
		for i in range(len(input)):
			writer = csv.writer(f)
			writer.writerow(input[i])


if __name__ == '__main__':
    main()