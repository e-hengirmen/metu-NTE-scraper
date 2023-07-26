import time
from os.path import exists
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

start = time.time()


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
action = ActionChains(driver)

#########################################################
# change myDEPT to your department
# delete departments that you dont want to take courses from the class_codes list
myDEPT = 'CENG'
# class_codes = ["120", "121", "125", "230", "232", "233", "236", "240", "241", "310", "311", "312", "314", "410", "420",
#                "450", "453", "602", "603", "604", "605", "606", "607", "608", "610", "611", "612", "639", "642", "643",
#                "644", "651", "682", "831", "863"]
#########################################################


url = "https://oibs2.metu.edu.tr/View_Program_Course_Details_64/"

#################################
driver.get(url)

class_code_webelemnt_list=driver.find_elements(By.CSS_SELECTOR, 'option')
class_codes=[element.get_attribute("value") for element in class_code_webelemnt_list if len(element.get_attribute("value"))==3]

#single_content > form:nth-child(3) > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > select:nth-child(2) > option:nth-child(101)
#single_content > form:nth-child(3) > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > select:nth-child(2) > option:nth-child(1)
# <option value="572">Aerospace Engineering/Havacılık ve Uzay Mühendisliği </option>
for class_code in class_codes:
    el2 = driver.find_element(By.CSS_SELECTOR, 'option[value="' + class_code + '"]')
    print(el2.text)
    el2.click()
    driver.find_element(By.XPATH, '//*[@id="single_content"]/form/table[3]/tbody/tr/td/input').click()

    # -----------------------fail check---------------
    fm = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "formmessage")))
    # fm = driver.find_elements(By., "There is no")
    if fm.text == "Information about the department could not be found.":
        continue
    # -----------------------------------------------

    table = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="single_content"]/form/table[4]/tbody/tr')))[1:]
    for i in range(0, len(table)):
        row = table[i]
        try:
            column = row.find_element(By.XPATH, "./td[2]")
        except:
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="single_content"]/form/table[4]/tbody/tr')))[1:]
            row = table[i]
            column = row.find_element(By.XPATH, "./td[2]")
        
        


        rowTEXT = row.text
        # clicking course
        row.find_element(By.XPATH, "./td[1]/font/input").click()
        driver.find_element(By.XPATH, '//*[@id="single_content"]/form/table[2]/tbody/tr/td[1]/input').click()
        # clicking to sections
        sections = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[name=submit_section]')))
        for j in range(0, len(sections)):
            section = sections[j]
            try:
                section.click()
            except:
                sections = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[name=submit_section]')))
                section = sections[j]
                section.click()
            fm = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "formmessage")))
            # fm = driver.find_elements(By., "There is no")
            if fm.text == "There is no section criteria to take the selected courses for this section.":
                print("ALL", "\t", rowTEXT, j + 1)

            table2 = driver.find_elements(By.XPATH, '//*[@id="single_content"]/form/table[3]/tbody/tr')[1:]
            for row2 in table2:
                dept = row2.find_element(By.XPATH, './td[1]').text
                if dept == 'ALL' or dept == myDEPT:
                    print(dept, "\t", rowTEXT, j + 1)
                    break
            driver.back()
        driver.back()
    driver.back()

driver.quit()

end = time.time()
print("done ", end - start, " seconds")



