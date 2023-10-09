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
		options.add_experimental_option('detach', True)
		user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
		options.add_argument(f'user-agent={user_agent}')
		self.driver = webdriver.Chrome(options)
		print("Driver active")
		self.searchpagelink_anime = ""
		self.searchpagelink_movie = ""

	def setup(self, imdb_username, imdb_pass, mal_username, mal_pass):
		mal = 'https://myanimelist.net/login.php?from=%2F&'
		imdb = 'https://www.imdb.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.imdb.com%2Fregistration%2Fap-signin-handler%2Fimdb_us&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=imdb_us&openid.mode=checkid_setup&siteState=eyJvcGVuaWQuYXNzb2NfaGFuZGxlIjoiaW1kYl91cyIsInJlZGlyZWN0VG8iOiJodHRwczovL3d3dy5pbWRiLmNvbS8_cmVmXz1sb2dpbiJ9&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&tag=imdbtag_reg-20'
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

		self.driver.get('https://www.imdb.com/')
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
			self.driver.get(self.searchpagelink_movie)
			print("Gathering data in IMDB")
			while(True):
				try:
					entity = f'//*[@id="__next"]/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/ul/li[{entityno+1}]'
					self.driver.find_element("xpath", entity).click()
					break
				except:
					pass
			while(True):
				try:
					pass
				except:
					pass
		else:
			anime_data = {}
			anime_userdata = {}

			#self.driver.get(self.searchpagelink_anime)
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
								
					print(anime_data["name"])
					print(anime_data["synopsis"])
					print(anime_data["posterlink"])
					for i in anime_information:
						print(i)
					if("next ep" in anime_data):
						print(anime_data["next ep"])
					break
				except Exception as err:
					print(err)
					pass
			

a = mediadatabase()
a.setup("", "", "", "")
#name = input("Enter movie name: ")
#a.searchmeida(name, "all")
l = ['https://myanimelist.net/anime/40357/Tate_no_Yuusha_no_Nariagari_Season_3', 'https://myanimelist.net/anime/53887/Spy_x_Family_Season_2', 'https://myanimelist.net/anime/47160/Goblin_Slayer_II', 'https://myanimelist.net/anime/54595/Kage_no_Jitsuryokusha_ni_Naritakute_2nd_Season', 'https://myanimelist.net/anime/52991/Sousou_no_Frieren', 'https://myanimelist.net/anime/55644/Dr_Stone__New_World_Part_2', 'https://myanimelist.net/anime/54918/Tokyo_Revengers__Tenjiku-hen', 'https://myanimelist.net/anime/52741/Undead_Unluck', 'https://myanimelist.net/anime/52990/Keikenzumi_na_Kimi_to_Keiken_Zero_na_Ore_ga_Otsukiai_suru_Hanashi', 'https://myanimelist.net/anime/50664/Saihate_no_Paladin__Tetsusabi_no_Yama_no_Ou']
ts = 0
for i in l:
	s = time()
	a.getmediadata(i, 1, cat="mal")
	e = time() - s
	print(e, "\n")
	ts += e
print(ts/len(l))