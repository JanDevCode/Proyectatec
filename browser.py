from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

def search(something):
 browser = webdriver.Chrome('C:\\ChromeVirtual\\chrome-win64')
 
 browser.maximize_window()
 browser.get('https://www.google.com.mx/')
 findElem = browser.find_element_by_name('q')
 findElem.send_keys(something)
 findElem.send_keys(Keys.RETURN)