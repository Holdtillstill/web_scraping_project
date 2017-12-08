# web_scraping_project
Parse and extract data for client's research
## Prerequisites
Python 3.x </br>
BeautifulSoup4 </br>
Selenium and ChromeDriver </br>
## Directory Tree
```
project(base_path)
	|──about_data.csv
	|──badges_data.csv
	|──clanLeaderboards_data.csv
	|──playerLeaderboards_data.csv
	|──recommendedGames_data.csv
	|──store_data.csv
	└──popularGames
		|──game_about.html
		|──game_store.html
		|──game_leaderboard.html
		└──creators(from popularGames)
			|──group_main.html
			|──group_clan.html
			|──individual_about.html
			|──individual_creation.html
			|──individual_player_badge_page_x.html
			|──individual_player_favorite_game_page_x.html
			|──group_clan.csv
			|──group_about.csv
			|──indie_about.csv
			|──indie_group.csv
			|──group_creation.csv
			|──indie_creation.csv
			|──indie_player_badge.csv
			|──indie_roblox_badge.csv
			|──indie_favorite_game.csv
			└──secondTier(games created by creators from previous level)
					|──game_about.html
					|──game_store.html
					|──game_leaderboard.html
```
