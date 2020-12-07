from selenium import webdriver
import time
import sys 

sys.path.append('../')


########### Reporter Test

driver = webdriver.Chrome()
driver.get('http://127.0.0.1:5000')

#Sign in nonexisting reporter in
driver.find_element_by_xpath('/html/body/div[1]/div/div/aside[1]/div/article/form/div/div[2]/a').click()
driver.find_element_by_xpath('//*[@id="email"]').send_keys('reporter11@test.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip124')
driver.find_element_by_xpath('//*[@id="submit"]').click()

# investigator logs into Reporter
driver.find_element_by_xpath('//*[@id="email"]').clear()
driver.find_element_by_xpath('//*[@id="email"]').send_keys('lfdeleon98@gmail.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="submit"]').click()

# Reporter Registration Test
driver = webdriver.Chrome()
driver.get('http://127.0.0.1:5000')


#Register Existing Reporter
driver.find_element_by_xpath('/html/body/div[1]/div/div/aside[1]/div/article/form/div/div[1]/a').click()
driver.find_element_by_xpath('//*[@id="email"]').send_keys('lfdeleon@gmail.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="pass_confirm"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="submit"]').click()

# Existing investigator tries to register
driver.find_element_by_xpath('//*[@id="email"]').clear()
driver.find_element_by_xpath('//*[@id="email"]').send_keys('lfdeleon98@gmail.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="pass_confirm"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="submit"]').click()

#nonmatching password input
driver.find_element_by_xpath('//*[@id="email"]').clear()
driver.find_element_by_xpath('//*[@id="email"]').send_keys('reporter11@test.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="pass_confirm"]').send_keys('flip124')
driver.find_element_by_xpath('//*[@id="submit"]').click()

#Successful Registration
driver.find_element_by_xpath('//*[@id="email"]').clear()
driver.find_element_by_xpath('//*[@id="email"]').send_keys('reporter11@test.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="pass_confirm"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="submit"]').click()

# Existing investigator tries to login
driver.find_element_by_xpath('//*[@id="email"]').send_keys('lfdeleon98@gmail.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="submit"]').click()

#Successful login
driver.find_element_by_xpath('//*[@id="email"]').clear()
driver.find_element_by_xpath('//*[@id="email"]').send_keys('reporter11@test.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="submit"]').click()


########### Investigator Test


driver = webdriver.Chrome()
driver.get('http://127.0.0.1:5000')

#Sign in nonexisting Investigator in
driver.find_element_by_xpath('/html/body/div[1]/div/div/aside[2]/div/article/form/div/div[2]/a').click()
driver.find_element_by_xpath('//*[@id="email"]').send_keys('investigator11@test.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip124')
driver.find_element_by_xpath('//*[@id="submit"]').click()

driver = webdriver.Chrome()
driver.get('http://127.0.0.1:5000')

#Register Existing Investigator
driver.find_element_by_xpath('/html/body/div[1]/div/div/aside[2]/div/article/form/div/div[1]/a').click()
driver.find_element_by_xpath('//*[@id="email"]').send_keys('lfdeleon98@test.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="pass_confirm"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="submit"]').click()

#nonmatching password input
driver.find_element_by_xpath('//*[@id="email"]').clear()
driver.find_element_by_xpath('//*[@id="email"]').send_keys('investigator11@test.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="pass_confirm"]').send_keys('flip124')
driver.find_element_by_xpath('//*[@id="submit"]').click()

#reporter tries to register as investigator
driver.find_element_by_xpath('//*[@id="email"]').clear()
driver.find_element_by_xpath('//*[@id="email"]').send_keys('reporter11@test.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="pass_confirm"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="submit"]').click()

#Successful registration
driver.find_element_by_xpath('//*[@id="email"]').clear()
driver.find_element_by_xpath('//*[@id="email"]').send_keys('investigator11@test.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="pass_confirm"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="submit"]').click()

# reporter logs into investigator
driver.find_element_by_xpath('//*[@id="email"]').send_keys('reporter11@test.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="submit"]').click()

# Successful login
driver.find_element_by_xpath('//*[@id="email"]').clear()
driver.find_element_by_xpath('//*[@id="email"]').send_keys('investigator11@test.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('flip123')
driver.find_element_by_xpath('//*[@id="submit"]').click()

print('Test completed succesfully!')