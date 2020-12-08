from selenium import webdriver
import time


import sys 
sys.path.append('../')


driver = webdriver.Chrome()
driver.get('http://127.0.0.1:5000')

#Register inspector
driver.find_element_by_xpath('/html/body/div[2]/div/div/aside[2]/div/article/form/div/div[2]/a').click()
driver.find_element_by_xpath('//*[@id="email"]').send_keys('inspector@test.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('abcd123')
driver.find_element_by_xpath('//*[@id="pass_confirm"]').send_keys('abcd123')
driver.find_element_by_xpath('//*[@id="submit"]').click()

#Sign Inspector in
driver.find_element_by_xpath('//*[@id="email"]').send_keys('inspector@test.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('abcd123')
driver.find_element_by_xpath('//*[@id="submit"]').click()

#Open Dash
driver.find_element_by_xpath('/html/body/div/div/a[2]').click()

assert driver.find_element_by_id('dash-error')