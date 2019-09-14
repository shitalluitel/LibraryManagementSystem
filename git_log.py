import git 
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC 

repo = git.Repo(input('Git Repo Path: '))
author=input('Name of Author: ')
since=input('Time of Commit: ')
print(since)

filter = {}
filter['author'] = author
if not since == '':
    filter['since'] = since


commits = list(repo.iter_commits(**filter))

messages = []
for commit in commits:
    messages.append(commit.message)

# message = '\n '.join(messages)
message = ''.join(messages)

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://core.realhrsoft.com/user/work-log/log-work")

email = driver.find_element_by_id('id_email')
password = driver.find_element_by_id('id_password')
sign_in = driver.find_element_by_id('logInButton')

if email and password and sign_in:
    email.send_keys('shital.luitel@aayulogic.com')
    password.send_keys('c0d3r5@87')
    sign_in.click()

while not driver.current_url == 'https://core.realhrsoft.com/':    
    time.sleep(1)

time.sleep(5)

driver.find_element_by_css_selector('#app > div.v-application--wrap > nav > div.v-navigation-drawer__content > div > div:nth-child(4) > div > div.v-list-group__header.v-list-item.v-list-item--link.theme--dark').click()

driver.find_element_by_css_selector('#app > div.v-application--wrap > nav > div.v-navigation-drawer__content > div > div:nth-child(4) > div > div.v-list-group__items > div > a:nth-child(3)').click()

while not driver.current_url == 'https://core.realhrsoft.com/user/work-log/log-work':    
    time.sleep(1)

time.sleep(5)

driver.find_element_by_css_selector('#id_description > div > div.trumbowyg-editor').send_keys(message)
# driver.find_element_by_css_selector('#id_description > div > textarea').send_keys(message)
# driver.find_element_by_css_selector('#app > div > main > div > div > div > div:nth-child(2) > form > div > div.col-md-4.col > div > div.v-picker__body.theme--light > div > div.v-date-picker-table.v-date-picker-table--date.theme--light > table > tbody > tr:nth-child(2) > td:nth-child(6) > button').click()
