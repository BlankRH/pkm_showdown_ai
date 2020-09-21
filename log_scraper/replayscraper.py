from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from argparse import ArgumentParser
argparser = ArgumentParser()
argparser.add_argument('--MAXN', type=int, default=100)
argparser.add_argument('--MAXUSER', type=int, default=100)
args = argparser.parse_args()

#create chrome webdriver and navigate to pokemon showdown site
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get("https://play.pokemonshowdown.com/ladder")
assert "Showdown" in driver.title
driver.find_element_by_xpath("//*[@id='room-ladder']/div/ul[8]/li[1]/button").click()
MAXN = args.MAXN
MAXUSER = args.MAXUSER
cnt = 0

#process bar
import time
import sys

toolbar_width = 40


with open("data/userList.txt", "r") as fp:
    recorded = fp.readlines()

#retrieve list of top players on pokemon showdown
fp = open("data/userList.txt", "a")
userList = []
#for i in range(5):
for i in range(MAXUSER):
    try:
        user = driver.find_element_by_xpath("//*[@id='room-ladder']/div/table/tbody/tr[" + str(i + 2) + "]/td[2]").text
    except:
        driver.save_screenshot("error.jpg")
    if user in recorded:
        MAXUSER += 1
        continue
    userList.append(user)
    fp.write(user+'\n')
fp.close()

print("Finished Getting Users")

#search pokemon showdown replays for each username in list
cnt2 = 0
printList = []
for user in userList:
    cnt2 += 1
    driver.implicitly_wait(5)
    driver.get("https://replay.pokemonshowdown.com/search?user=" + user)
    #for each random battle replay found, save link to source
    for li in driver.find_elements_by_xpath("/html/body/div[2]/div/ul/li"):
        t = li.text
        if "[gen6ou]" in t:
            cnt += 1
            print("Found HTML Username={}".format(t))
            printList.append(str(li.find_element_by_tag_name("a").get_attribute('href')))
        if cnt >= MAXN:
            break

#obtain source from links
i = len(recorded)
for link in printList:
    driver.implicitly_wait(10)
    driver.get(link)
    log = driver.find_element_by_xpath("/html/body/div[2]/div/script")
    with open("data/"+ str(i) + ".txt", "w") as text:
        text.write(str(log.get_attribute("innerHTML")))
    i += 1

print("Finished")

driver.close()
