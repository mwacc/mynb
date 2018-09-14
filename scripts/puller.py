from selenium import webdriver
import os
import shutil
import glob
import re

BASEDIR = os.getcwd() + '\\..\\dwnld'

def pull_location(browser, city_name):
    browser.get("https://www.redfin.com/")
    browser.find_element_by_id('search-box-input').send_keys(city_name)
    buttons = browser.find_elements_by_tag_name('button')
    for b in buttons:
        if 'submit' == b.get_attribute('type'):
            print('Loading %s' % city_name)
            b.click()
            browser.find_element_by_id('download-and-save').click()
            rename(BASEDIR, city_name)
            break

def rename(basedir, city_name):
    src_file = glob.glob(basedir + '\\redfin*')[0]
    shutil.move(src_file, basedir + "\\" + re.sub(r"\s|\n", "", city_name) + ".csv")

# To prevent download dialog
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # set custom location
profile.set_preference('browser.download.manager.showWhenStarting', True)
profile.set_preference('browser.download.dir', BASEDIR)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

browser = webdriver.Firefox(firefox_profile = profile, executable_path = 'C:\Mix\geckodriver.exe')
browser.implicitly_wait(10) # seconds

with open("index.txt", "r") as lines:
    for line in lines:
        pull_location(browser, line)

browser.close()
