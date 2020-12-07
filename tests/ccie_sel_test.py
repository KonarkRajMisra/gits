from selenium import webdriver
import time


import sys 
sys.path.append('../')
from gitsapp.models import Report

driver = webdriver.Chrome()
driver.get('http://127.0.0.1:5000')

#Register reporter
driver.find_element_by_xpath('/html/body/div[1]/div/div/aside[1]/div/article/form/div/div[1]/a').click()
driver.find_element_by_xpath('//*[@id="email"]').send_keys('reporter80@test.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="pass_confirm"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="submit"]').click()

#Sign reporter in
driver.find_element_by_xpath('//*[@id="email"]').send_keys('reporter@test.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="submit"]').click()

#Open CCIE
driver.find_element_by_xpath('/html/body/div[1]/div/a[1]').click()

#Create CCIE Report
driver.find_element_by_xpath('//*[@id="first_name"]').send_keys('John')
driver.find_element_by_xpath('//*[@id="last_name"]').send_keys('Doe')
driver.find_element_by_xpath('//*[@id="sup_fname"]').send_keys('Jane')
driver.find_element_by_xpath('//*[@id="sup_lname"]').send_keys('Doe')
driver.find_element_by_xpath('//*[@id="date"]').send_keys('02132004')
driver.find_element_by_xpath('//*[@id="city"]').send_keys('San Diego')
driver.find_element_by_xpath('//*[@id="cross_street"]').send_keys('Montezuma Blvd')
driver.find_element_by_xpath('//*[@id="state"]/option[6]').click()

input("Add a non image file and press enter to continue")

#Test if abbreviations, zipcode and crew fail
driver.find_element_by_xpath('//*[@id="street_address"]').send_keys('5500 Campanile Dr')
driver.find_element_by_xpath('//*[@id="zipcode"]').send_keys('123456')
driver.find_element_by_xpath('//*[@id="crew"]').send_keys('123456')
driver.find_element_by_xpath('//*[@id="submit"]').click()

assert driver.find_element_by_id('address-error')
assert driver.find_element_by_id('zipcode-error')
assert driver.find_element_by_id('crew-error')
assert driver.find_element_by_id('photos-error')

#Fix errors
driver.find_element_by_xpath('//*[@id="street_address"]').clear()
driver.find_element_by_xpath('//*[@id="street_address"]').send_keys('5500 Campanile Drive')
driver.find_element_by_xpath('//*[@id="zipcode"]').clear()
driver.find_element_by_xpath('//*[@id="zipcode"]').send_keys('92182')
driver.find_element_by_xpath('//*[@id="crew"]').clear()
driver.find_element_by_xpath('//*[@id="crew"]').send_keys('1234')
driver.find_element_by_xpath('//*[@id="state"]/option[5]').click()
input("Add an image file and press enter to continue")


driver.find_element_by_xpath('//*[@id="submit"]').click()

#Verify report submitted
assert len(Report.query.all()) != 0

print('Test completed succesfully!')