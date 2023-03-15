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


def mld_switch(str):
    dict = {
        "ARAB": "602",
        "FREN": "603",
        "GERM": "604",
        "JA": "605",
        "ITAL": "606",
        "RUS": "607",
        "SPAN": "608",
        "HEB": "609",
        "GRE": "610",
        "GREEK": "610",
        "CHN": "611",
        "PERS": "612",
        "ENG": "639"
    }
    courseName = ""
    for c in str:
        if c == ' ' or c.isdigit():
            break
        courseName += c
    return dict[courseName]


def write_num(str):
    courseCode = ""
    for c in str:
        if c.isdigit():
            courseCode += c
    return courseCode


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
action = ActionChains(driver)

#########################################################
# change myDEPT to your department
# delete departments that you dont want to take courses from the class_codes list
myDEPT = 'CENG'
class_codes = ["120", "121", "125", "230", "232", "233", "236", "240", "241", "310", "311", "312", "314", "410", "420",
               "450", "453", "602", "603", "604", "605", "606", "607", "608", "610", "611", "612", "639", "642", "643",
               "644", "651", "682", "831", "863"]
#########################################################


NTE_codes = set()
if exists("./NTE_codes.txt"):
    file = open("NTE_codes.txt", "r")
    for course_code in file.readline().split():
        NTE_codes.add(course_code)
else:
    file = open("NTE_codes.txt", "w")
    NTE_URL = "https://muhfd.metu.edu.tr/en/nte-courses"
    driver.get(NTE_URL)
    rows = driver.find_elements(By.XPATH, '//*[@id="content"]/article/div[2]/table/tbody/tr')

    col_td_list=[]
    for i, index in zip(rows, range(1,1+len(rows))):
        col_td_list.append(driver.find_elements(By.XPATH, '//*[@id="content"]/article/div[2]/table/tbody/tr['+str(index)+']/td')[0].text)
    for col_td_text, index in zip(col_td_list, range(1,1+len(col_td_list))):
        if index<0:
            continue
        # getting link and course_code
        class_code = write_num(col_td_text)
        if (int(class_code) >= 603 and int(class_code) <= 639):
            continue
        if int(class_code) >311:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_elements(By.XPATH, '//*[@id="content"]/article/div[2]/table/tbody/tr['+str(index)+']/td')[0].click()
        #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/article/div[2]/table/tbody/tr['+str(index)+']/td[2]')))[0].click()

        #driver.find_elements(By.XPATH, '//*[@id="content"]/article/div[2]/table/tbody/tr['+str(index)+']/td')[0].click()

        if (int(class_code) != 602):
            course_table = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="content"]/article/div[2]/table/tbody/tr')))[1:]
            for course in course_table:
                course_code = write_num(course.find_elements(By.TAG_NAME, 'td')[0].text)
                full_code = class_code + ("0" if len(course_code) == 3 else "") + course_code
                NTE_codes.add(full_code)
                file.write(full_code + " ")
        else:  # mld specific case their xpath and table structure are different
            course_table = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="content"]/div[2]/table/tbody/tr')))[1:]
            for course in course_table:
                course_name = course.find_elements(By.TAG_NAME, 'td')[0].text
                course_code = write_num(course_name)
                class_code = mld_switch(course_name)
                full_code = class_code + ("0" if len(course_code) == 3 else "") + course_code
                NTE_codes.add(full_code)
                file.write(full_code + " ")
        driver.back()

url = "https://oibs2.metu.edu.tr/View_Program_Course_Details_64/"

#################################
driver.get(url)
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
        if column.text in NTE_codes:
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



