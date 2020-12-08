from selenium import webdriver
import time


import sys 
sys.path.append('../')
from gitsapp.models import Report

driver = webdriver.Chrome()
driver.get('http://127.0.0.1:5000')

#Register reporter
driver.find_element_by_xpath('/html/body/div[1]/div/div/aside[1]/div/article/form/div/div[1]/a').click()
driver.find_element_by_xpath('//*[@id="email"]').send_keys('reporter@test.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="pass_confirm"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="submit"]').click()

#Sign reporter in
driver.find_element_by_xpath('//*[@id="email"]').send_keys('reporter@test.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="submit"]').click()

#Open Dash
driver.find_element_by_xpath('/html/body/div[1]/div/a[0]').click()

assert driver.find_element_by_id('reporter-dash-error')