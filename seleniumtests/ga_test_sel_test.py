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

#Open GA
driver.find_element_by_xpath('/html/body/div[1]/div/a[2]').click()

#Submit GA Search Query
driver.find_element_by_xpath('//*[@id="start_date"]').send_keys('12/7/20')
driver.find_element_by_xpath('//*[@id="end_date"]').send_keys('12/7/20')
driver.find_element_by_xpath('//*[@id="start_gps_lat"]').send_keys(33.0)
driver.find_element_by_xpath('//*[@id="start_gps_lng"]').send_keys(33.0)
driver.find_element_by_xpath('//*[@id="end_gps_lat"]').send_keys(33.0)
driver.find_element_by_xpath('//*[@id="end_gps_lng"]').send_keys(33.0)
driver.find_element_by_xpath('//*[@id="suspect_name"]').send_keys('John Doe')
driver.find_element_by_xpath('//*[@id="gangname"]').send_keys('Whistleblowers')

assert driver.find_element_by_id('start_date-error')
assert driver.find_element_by_id('end_date-error')
assert driver.find_element_by_id('start_gps_lat-error')
assert driver.find_element_by_id('start_gps_lng-error')
assert driver.find_element_by_id('end_gps_lat-error')
assert driver.find_element_by_id('end_gps_lng'-error)
assert driver.find_element_by_id('suspect_name-error')
assert driver.find_element_by_id('gangname-error')

driver.find_element_by_xpath('//*[@id="calculate"]').click()
