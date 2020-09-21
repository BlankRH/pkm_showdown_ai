from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from argparse import ArgumentParser
argparser = ArgumentParser()
argparser.add_argument('--MAXN', type=int, default=10)
argparser.add_argument('--MAXUSER', type=int, default=50)
args = argparser.parse_args()

#create chrome webdriver and navigate to pokemon showdown site
print(1)
driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get("https://play.pokemonshowdown.com/ladder")
assert "Showdown" in driver.title
driver.find_element_by_xpath("//*[@id='room-ladder']/div/ul[2]/li[1]/button").click()
MAXN = arg.MAXN
MAXUSER = arg.MAXUSER
cnt = 0

#retrieve list of top players on pokemon showdown
userList = []
#for i in range(5):
for i in range(MAXUSER):
    print(i)
    userList.append(driver.find_element_by_xpath("//*[@id='room-ladder']/div/table/tbody/tr[" + str(i + 2) + "]/td[2]").text)

print("Finished Getting Users")

#search pokemon showdown replays for each username in list
cnt2 = 0
printList = []
for user in userList:
    cnt2 += 1
    print("User Number %d", cnt2)
    driver.implicitly_wait(5)
    driver.get("https://replay.pokemonshowdown.com/search?user=" + user)
    #for each random battle replay found, save link to source
    for li in driver.find_elements_by_xpath("/html/body/div[2]/div/ul/li"):
        t = li.text
        if "[gen7ou]" in t:
            cnt += 1
            print("Found Player {}, username={}".format(cnt, t))
            printList.append(str(li.find_element_by_tag_name("a").get_attribute('href')))
        if cnt >= MAXN:
            break

#obtain source from links
i = 0
for link in printList:
    text = open("data/"+ str(i) + ".txt", "w")
    driver.implicitly_wait(10)
    driver.get(link)
    log = driver.find_element_by_xpath("/html/body/div[2]/div/script")
    text.write(str(log.get_attribute("innerHTML").encode("utf-8")))
    text.close()
    i += 1
    print("Downloaded HTML Number %d", i)

print("Finished")

driver.close()
