from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
import os
import getpass

WINDOW_SIZE = "1920,1080"

def checker(link, user, pwd, recheck):
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

	browser = webdriver.Chrome(options=chrome_options) # remove the argument if you wanna see the actual browser
	browser.get(link) # loads the link

	time.sleep(5) # let the browser land on the login page if needed

	if "Sign-On" in browser.title:

		username = browser.find_element("id","logon")
		password = browser.find_element("id","pass")
		username.send_keys(user)
		password.send_keys(pwd)
		browser.find_element("name","_eventId_proceed").click()
		
		print("Logging in...",end='\r')

		time.sleep(5) # let the login go through

		if "Class Detail" in browser.title:
			print("Logged in! Checking course status now...")
		else:
			print("Wrong credentials or wrong link. Check github page for directions. Exiting...")
			return
	
	while 1:

		content = browser.page_source
		soup = BeautifulSoup(content,features="lxml")
		name = ""
		check = ""
		for a in soup.findAll('tr',attrs={'class':'enrl_mtng_info scrollable-collapse table-width2'}):
			name = a.find('td')
		if name != "":
			check = name.string

		print(check, end='\n')

		if 'Open' in check:
			print("Got the course open. Sending notification and closing. Bye!")
			os.system('say "Hey! Wake up! We got your course!"')
			# os.system("osascript -e 'display alert \"ALERT\" message \"Course Open!\"'")
			os.system("osascript -e 'display notification \"Course Open!\" with title \"ALERT\"'")
			break
		elif 'Waitlist' in check:
			if 'of' in check:
				print("Got the waitlist open. Sending notification and closing. Bye!")
				os.system('say "Hey! Wake up! Maybe waitlist is open!"')
				# os.system("osascript -e 'display alert \"ALERT\" message \"Waitlist Open!\"'")
				os.system("osascript -e 'display notification \"Waitlist Open!\" with title \"ALERT\"'")
				break
		
		previousLength = 0
		for i in range(recheck*60,0,-1):
			if i<60:
				t = 'Waiting for '+ str(i) +' seconds to re-check'
				print(" " * previousLength, end="\r")
				print(t , end='\r')
				previousLength = len(t)
			else:
				mins = int(i/60)
				secs = i%60
				t = 'Waiting for ' + str(mins) + ' mins, ' + str(secs) + ' seconds to re-check'
				print(" " * previousLength, end="\r")
				print( t, end='\r')
				previousLength = len(t)
			time.sleep(1)
		print(" " * previousLength, end="\r")

		browser.refresh()
		time.sleep(3) # wait for refresh

	browser.close()

os.system("printf '\033c'")
link = input("Enter the link: ")
recheck = int(input("Enter re-check interval (in mins): "))
user = input("Enter your UCLA username: ")
pwd = getpass.getpass(prompt="Enter your UCLA password: ")
checker(link, user, pwd, recheck)
