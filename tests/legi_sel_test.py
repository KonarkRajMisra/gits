from selenium import webdriver
import time


import sys 
sys.path.append('../')
from gitsapp.models import Report

driver = webdriver.Chrome()
driver.get('http://127.0.0.1:5000')

#Sign in as existing investigator
driver.find_element_by_xpath('/html/body/div[1]/div/div/aside[2]/div/article/form/div/div[2]/a').click()
driver.find_element_by_xpath('//*[@id="email"]').send_keys('lfdeleon98@gmail.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('123456')
driver.find_element_by_xpath('//*[@id="submit"]').click()

driver.find_element_by_xpath('/html/body/div[1]/div/a[1]').click()
driver.find_element_by_xpath('/html/body/div[1]/div/table/tbody[2]/tr[2]/th/a').click()

driver.find_element_by_xpath('//*[@id="moniker"]').send_keys('A cool ass frog.')
driver.find_element_by_xpath('//*[@id="cleanup"]/option[2]').click()
driver.find_element_by_xpath('//*[@id="investigation_status"]/option[1]').click()
driver.find_element_by_xpath('//*[@id="type_of_building"]/option[1]').click()


driver.find_element_by_xpath('//*[@id="search_first_name"]').send_keys('Pixie')
driver.find_element_by_xpath('//*[@id="search_last_name"]').send_keys('Cut')
driver.find_element_by_xpath('//*[@id="type_of_building"]/option[1]').click()


driver.find_element_by_xpath('//*[@id="submit"]').click()
print('Test completed succesfully!')
