from selenium import webdriver
import os
import shutil
import glob
import re

BASEDIR = os.getcwd() + '\\..\\dwnld'

# To prevent download dialog
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # set custom location
profile.set_preference('browser.download.manager.showWhenStarting', True)
profile.set_preference('browser.download.dir', BASEDIR)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

def pull_location(city_name):
    browser = webdriver.Firefox(firefox_profile = profile, executable_path = 'C:\Mix\geckodriver.exe')
    browser.implicitly_wait(10) # seconds

    browser.get("https://www.redfin.com/")
    browser.find_element_by_id('search-box-input').send_keys(city_name)
    print('Search %s' % city_name)
    for attempt in range(0,5):
        buttons = browser.find_elements_by_tag_name('button')
        for b in buttons:
            if 'submit' == b.get_attribute('type'):
                print('Loading %s' % city_name)
                b.click()
                browser.find_element_by_id('download-and-save').click()
                rename(BASEDIR, city_name)
                browser.close()
                return


def rename(basedir, city_name):
    src_file = glob.glob(basedir + '\\redfin*')[0]
    shutil.move(src_file, basedir + "\\" + re.sub(r"\s|\n", "", city_name) + ".csv")

with open("index.txt", "r") as lines:
    for line in lines:
        pull_location(line)
