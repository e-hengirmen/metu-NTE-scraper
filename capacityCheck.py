import time
from os.path import exists
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

import os
import urllib.request
import predict

#########################################################
# change myDEPT to your department
# delete departments that you dont want to take courses from the class_codes list
myDEPT      = 'CENG'
class_codes = [ "120", "121", "125", "230", "232", "233", "236", "240", "241", "310", "311", "312", "314", "410", "420", "450", "453","602", "603", "604", "605", "606", "607", "608","610", "611", "612", "639","642", "643", "644", "651", "682", "831", "863"]
Username    = "e246801"     #fill your metu username
Password    = "##########"    #fill your password
#########################################################

start = time.time()

# prerequsite course list check
if not exists("out2.txt"):
    print("out2.txt does not exist")
    print("Create course background using courseDet.py first")
    quit()
# opening course window
url  = "https://student.metu.edu.tr/"
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)
driver.find_element(By.LINK_TEXT,"View Course Capacity (158)").click()
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"textUsername"))).send_keys(Username)
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"textPassword"))).send_keys(Password)
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="signinForm"]/fieldset/div[3]/div/button[1]'))).click()

iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))  # its in the first frame
driver.switch_to.frame(iframe)

# checking capacity for every course
file_existing = open("out2.txt", encoding="utf8")
course_code="0"
while True:
    course_current_sections=[]
    line = file_existing.readline().split()
    if not line:
        break
    if(line[0]=='ALL' or line[0]==myDEPT):
        # does not recheck same sections
        #if course_code==line[1]:
         #   continue
        course_code=line[1]
        course_current_section=line[-1]


        captcha_fails = True

        while captcha_fails:
            # change to frame enter course code and get image url

            # download and solve captcha
            captcha_url = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="SignInFormDiv"]/form/fieldset/div[2]/div[1]/img'))).get_attribute("src")
            urllib.request.urlretrieve(captcha_url, 'temp_captcha.jpg')
            captcha_result=predict.predict_captcha('temp_captcha.jpg')
            os.remove('temp_captcha.jpg')

            input_course = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "text_course_code")))
            input_captcha = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "text_img_number")))
            input_course.clear()
            input_course.send_keys(course_code)
            input_captcha.clear()
            input_captcha.send_keys(captcha_result)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="SignInFormDiv"]/form/fieldset/div[4]/div[2]/input'))).click()

            if WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/div/div[1]/div[1]'))).text=="×\nInvalid Image Verification.":
                continue
            captcha_fails=False

            sections=WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, '/html/body/div/div/div[1]/div/div[2]/div/div[3]/div/form/table/tbody/tr')))[0:]
            for section in sections:
                section_vars=section.find_elements(By.TAG_NAME,'td')
                if section_vars[0].text==course_current_section:
                    if section_vars[3].text=="":
                        break
                    section_capacity = int(section_vars[3].text)
                    used_section_capacity = int(section_vars[4].text)
                    if section_capacity>used_section_capacity:
                        print(course_code,'-',section_vars[0].text,'\t',section_capacity,"<->",used_section_capacity)
                    break
            ### check failure if does not fail

driver.quit()
quit()

#################################################################

