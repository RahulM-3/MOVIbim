from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from time import time, sleep

class mediadatabase:
	def __init__(self):
		options = Options()
		options.add_argument(r"user-data-dir=~/.var/app/com.google.Chrome/config/google-chrome")
		options.add_argument(r"profile-directory=Profile 1")
		#options.add_argument('--headless')
		options.add_argument("--window-size=20000,20000")
		options.add_argument("--disable-gpu")
		options.add_argument('--no-sandbox')
		options.add_argument('--lang=en_US')
		options.add_experimental_option('detach', True)
		user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
		options.add_argument(f'user-agent={user_agent}')
		self.driver = webdriver.Chrome(options)
		print("Driver active")
		self.searchpagelink_anime = ""
		self.searchpagelink_movie = ""

	def setup(self, imdb_username, imdb_pass, mal_username, mal_pass):
		mal = 'https://myanimelist.net/login.php?from=%2F&'
		imdb = 'https://www.imdb.com/'
		self.driver.get(mal)
		if("Login - MyAnimeList.net" == self.driver.title):
			print("Logging in [MAL]")
			while(True):
				try:
					self.driver.find_element("xpath", '//*[@id="loginUserName"]').send_keys(mal_username)
					self.driver.find_element("xpath", '//*[@id="login-password"]').send_keys(mal_pass)
					stayloggedin =  self.driver.find_element("xpath", '//*[@id="dialog"]/tbody/tr/td/form/div/p[5]/input')
					if(stayloggedin.is_enabled() == False):
						stayloggedin.click()
					self.driver.find_element("xpath", '//*[@id="dialog"]/tbody/tr/td/form/div/p[6]/input').click()
					break
				except:
					pass

		self.driver.get(imdb)
		if("Sign" in self.driver.find_element("xpath", '//*[@id="imdbHeader"]/div[2]/div[5]').text):
			print("Logging in [IMDB]")
			self.driver.get(imdb)
			while(True):
				try:
					self.driver.find_element("xpath", '//*[@id="ap_email"]').send_keys(imdb_username)
					self.driver.find_element("xpath", '//*[@id="ap_password"]').send_keys(imdb_pass)
					stayloggedin =  self.driver.find_element("xpath", '//*[@id="authportal-main-section"]/div[2]/div/div/form/div/div/div/div[3]/div/div/label/div/label/input')
					print(stayloggedin.is_enabled())
					if(stayloggedin.is_enabled() == False):
						stayloggedin.click()
					self.driver.find_element("xpath", '//*[@id="signInSubmit"]').click()
					break
				except:
					pass

	def searchmeida(self, searchkey, cat="all"):
		self.searchpagelink_anime = f"https://myanimelist.net/anime.php?q={searchkey}&cat=anime"
		self.searchpagelink_movie = f"https://www.imdb.com/find/?q={searchkey}&ref_=nv_sr_sm"

		s = time()
		if(cat=="anime" or cat=="all"):
			print("Searching in MAL")
			self.driver.get(self.searchpagelink_anime)
			entity = '//*[@id="content"]/div[6]/table/tbody/tr['
			while(True):
				try:
					newentity = list(self.driver.find_element("xpath", entity+"2]").text.split("\n"))
					newentity.pop(1)
					if(len(newentity) == 3):
						newentity.pop(1)
					newentity += list(newentity.pop(1).split(" "))
					print(newentity)
					nxt = 3
					try:
						while(True):
							newentity = list(self.driver.find_element("xpath", entity+f"{nxt}]").text.split("\n"))
							newentity.pop(1)
							if(len(newentity) == 3):
								newentity.pop(1)
							newentity += list(newentity.pop(1).split(" "))
							print(newentity)
							nxt += 1
					except:
						break
					break
				except:
					pass

		if(cat=="mov/ser" or cat=="all"):
			print("Searching in IMDB")
			self.driver.get(self.searchpagelink_movie)
			entity = '//*[@id="__next"]/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/ul/li['
			while(True):
				try:
					newentity = list(self.driver.find_element("xpath", entity+"1]").text.split("\n"))
					print(newentity)
					nxt = 2
					try:
						while(True):
							newentity = list(self.driver.find_element("xpath", entity+f"{nxt}]").text.split("\n"))
							print(newentity)
							nxt += 1
					except:
						break
					break
				except: 
					pass

		print(time()-s)

	def searchbytag(self, tags):
		pass

	def updatestatus(self, link, cat, status="completed", epno=0):
		if(cat == "anime"):
			pass
		elif(cat == "aniep"):
			self.driver.get(link)
			while(True):
				try:
					self.driver.find_element("xpath", '//*[@id="myinfo_watchedeps"]').clear()
					self.driver.find_element("xpath", '//*[@id="myinfo_watchedeps"]').send_keys(epno)
					self.driver.find_element("xpath", '//*[@id="addtolist"]/table/tbody/tr[4]/td[2]/input"]').click()
					return
				except Exception as err:
					print(err)
					pass
		elif(cat == "mov/ser"):
			self.driver.get(link)
			while(True):
				try:
					while(True):
						try:
							saveto = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[3]/div/div/button[1]'
							if(status == "completed"):
								self.driver.find_element("xpath", '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[3]/div/div/button[2]').click()
								saveto = '/html/body/div[4]/div[2]/div/div[2]/div/div[2]/ul/div[1]/div'
							elif(status == "onhold"):
								self.driver.find_element("xpath", '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[3]/div/div/button[2]').click()
								saveto = '/html/body/div[4]/div[2]/div/div[2]/div/div[2]/ul/div[2]/div'
							while(True):
								try:
									self.driver.find_element("xpath", saveto).click()
									return
								except:
									pass
						except:
							pass
				except:
					pass

	def getmediadata(self, link, entityno, cat):
		if(cat == "imdb"):
			movie_data = {}
			movie_userdata = {}

			#self.driver.get(self.searchpagelink_movie)
			#while(True):
			#	try:
			#		entity = f'//*[@id="__next"]/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/ul/li[{entityno+1}]'
			#		self.driver.find_element("xpath", entity).click()
			#		break
			#	except:
			#		pass

			self.driver.get(link)
			print("Gathering data in IMDB")
			while(True):
				try:
					info = list(self.driver.find_element("xpath", '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]').text.split("\n"))
					movie_data["name"] = info[0]
					if("Original title" in info[1]):
						movie_data["original title"] = info[1]
						movie_data["year"] = info[2]
						movie_data["rating"] = info[3]
						movie_data["duration"] = info[4]
					else:
						movie_data["year"] = info[1]
						movie_data["rating"] = info[2]
						movie_data["duration"] = info[3]
					movie_data["synopsis"] = self.driver.find_element("xpath", '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/p/span[3]').text
					movie_data["director"] = list(self.driver.find_element("xpath", '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[1]/div/ul').text.split(" "))
					movie_data["writer"] = list(self.driver.find_element("xpath", '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[2]/div/ul').text.split(" "))
					movie_data["main cast"] = list(self.driver.find_element("xpath", '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[3]/div/ul').text.split(" "))
					movie_data["genre"] = list(self.driver.find_element("xpath", '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]').text.split("\n"))
					rawdata = list(self.driver.find_element("xpath", '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/span/div/div[2]').text.split("\n"))
					movie_data["imdb rating"] = rawdata[0]+rawdata[1]+" By "+rawdata[2]+" Users"
					try:
						rawdata = list(self.driver.find_element("xpath", '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[3]/a/span/div/div[2]').text.split("\n"))
						movie_data["popularity"] = rawdata
					except:
						pass

					movie_userdata["userstatus"] = self.driver.find_element("xpath", '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[3]/div/div/button[1]/div/div[1]').text
					if(movie_userdata["userstatus"] == "In Watchlist"):
						movie_userdata["userstatus"] = "Plan to watch"
					else:
						movie_userdata["userstatus"] = ""
					movie_userdata["your rating"] = self.driver.find_element("xpath", '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[2]/button/span/div/div[2]/div').text.replace("\n", "")
					movie_data["user data"] = movie_userdata

					self.driver.get('https://hide.me/en/proxy')
					moviename = movie_data["name"].replace(" ", "-")
					replacethis = [":", "'", "?"]
					for c in replacethis:
						moviename = moviename.replace(c, "")
					moviename = "https://yts.mx/movies/"+moviename.lower()+"-"+movie_data["year"]
					self.driver.find_element("xpath", '//*[@id="u"]').send_keys(moviename)
					self.driver.find_element("xpath", '//*[@id="u"]').send_keys(Keys.ENTER)
					while(True):
						try:
							movie_data["posterlink"] = self.driver.find_element("xpath", '//*[@id="movie-poster"]/img').get_attribute('src')
							movie_data["donwload"] = {}
							for i in range(1, 5):
								try:
									movie_data["donwload"][self.driver.find_element("xpath", f'//*[@id="movie-info"]/p/a[{i}]').text] = f'//*[@id="movie-info"]/p/a[{i}]'
									#self.driver.find_element("xpath", f'//*[@id="movie-info"]/p/a[{i}]').click()
								except:
									break
							break
						except Exception as err:
							print(err)
							pass

					for k, v in movie_data.items():
						print(k, v)
					
					break
				except Exception as err:
					print(err)
					pass
		else:
			anime_data = {}
			anime_userdata = {}

			#self.driver.get(self.searchpagelink_anime)
			#while(True):
			#	try:
			#		entity = f'//*[@id="content"]/div[6]/table/tbody/tr[{entityno}]'
			#		self.driver.find_element("xpath", entity).click()
			#		break
			#	except:
			#		pass

			self.driver.get(link)
			print("Gathering data in MAL")
			while(True):
				try:
					anime_data["name"] = self.driver.find_element("xpath", '//*[@id="contentWrapper"]/div[1]/div/div[1]/div/h1/strong').text
					anime_data["synopsis"] = self.driver.find_element("xpath", '//*[@id="content"]/table/tbody/tr/td[2]/div[1]/table/tbody/tr[1]/td/p').text
					anime_data["posterlink"] = self.driver.find_element("xpath", '//*[@id="content"]/table/tbody/tr/td[1]/div/div[1]/a/img').get_attribute("src")
					
					info = '//*[@id="content"]/table/tbody/tr/td[1]/div/div['
					i = 5
					while("Type" not in self.driver.find_element("xpath", info+str(i)+"]").text):
						i += 1
					anime_information = [self.driver.find_element("xpath", info+str(i)+"]").text]
					while("Favorites" not in anime_information[len(anime_information)-1]):
						i += 1
						anime_information.append(self.driver.find_element("xpath", info+str(i)+"]").text)

					userstatus = Select(self.driver.find_element("xpath", '//*[@id="myinfo_status"]'))
					userstatus = userstatus.first_selected_option.text
					
					userscore = Select(self.driver.find_element("xpath", '//*[@id="myinfo_score"]'))
					userscore = userscore.first_selected_option.text

					anime_userdata["status"] = userstatus
					anime_userdata["eps Seen"] = self.driver.find_element("xpath", '//*[@id="myinfo_watchedeps"]').get_attribute('value')
					anime_userdata["your Score"] = userscore
					
					anime_data["information"] = anime_information
					anime_data["userdata"] = anime_userdata

					if("Status: Currently Airing" == anime_information[2]):
						self.driver.get('https://animeschedule.net/')
						self.driver.find_element("xpath", '//*[@id="header-search-bar"]').send_keys(anime_data["name"])
						self.driver.find_element("xpath", '//*[@id="header-search-submit"]').click()
						n = 0
						while(n < 5):
							try:
								anime_data["next ep"] = self.driver.find_element("xpath", '//*[@id="release-time-subs"]').text+" ["+self.driver.find_element("xpath", '//*[@id="countdown-wrapper"]/div[2]/time').text+"]"
								break
							except:
								n += 1
					break
				except Exception as err:
					print(err)
					pass
			

a = mediadatabase()
#a.setup("", "", "", "")
#name = input("Enter movie name: ")
#a.searchmeida(name, "all")

a.getmediadata("https://www.imdb.com/title/tt2409302/?ref_=fn_al_tt_1", 1, cat="imdb")
#a.getmediadata("https://www.imdb.com/title/tt0180093/?ref_=hm_tpks_tt_i_5_pd_tp1_pbr", 1, cat="imdb")

#l = ['https://myanimelist.net/anime/40357/Tate_no_Yuusha_no_Nariagari_Season_3', 'https://myanimelist.net/anime/53887/Spy_x_Family_Season_2', 'https://myanimelist.net/anime/47160/Goblin_Slayer_II', 'https://myanimelist.net/anime/54595/Kage_no_Jitsuryokusha_ni_Naritakute_2nd_Season', 'https://myanimelist.net/anime/52991/Sousou_no_Frieren', 'https://myanimelist.net/anime/55644/Dr_Stone__New_World_Part_2', 'https://myanimelist.net/anime/54918/Tokyo_Revengers__Tenjiku-hen', 'https://myanimelist.net/anime/52741/Undead_Unluck', 'https://myanimelist.net/anime/52990/Keikenzumi_na_Kimi_to_Keiken_Zero_na_Ore_ga_Otsukiai_suru_Hanashi', 'https://myanimelist.net/anime/50664/Saihate_no_Paladin__Tetsusabi_no_Yama_no_Ou']
#ts = 0
#for i in l:
#	s = time()
#	a.getmediadata(i, 1, cat="mal")
#	e = time() - s
#	print(e, "\n")
#	ts += e
#print(ts/len(l))