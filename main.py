import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

start = time.time()

# mld always creates problems for everyone
def mld_switch(str):
    dict={
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
    courseName=""
    for c in str:
        if c==' ' or c.isdigit():
            break
        courseName+=c
    return dict[courseName]

def write_num(str):
    courseCode = ""
    for c in str:
        if c.isdigit():
            courseCode += c
    return courseCode


NTE_URL = "https://muhfd.metu.edu.tr/en/nte-courses"

url1 = "https://sis.metu.edu.tr/get.php?package="
site_package = "3i-Uh6Eddmrp6bYyWh70SAtQUE2UoAyMNIz4G0JZWB8qFIj0BwTKcGuJHGuHLz9q81RivLrzjR5p98b5-theyQ"
url2 = "#/?selectSemester=20221&selectProgram="
class_codes = ["120", "121", "125", "230", "232", "233", "236", "240", "241", "310", "311", "312", "314", "410", "420",
               "450", "453", "454", "602", "603", "604", "605", "606", "607", "608", "609", "610", "611", "612", "639",
               "642", "643", "644", "651", "682", "831", "863"]
url3 = "&selectDepartmentOfCourse%5B%5D=571&selectDepartmentOfCourse%5B%5D=571&submitSearchForm=Search&stamp=DAfsr9hLq3WKfFAoHCjV4PUiC-Q3vgWwNQaHZX6hQ4dr2qCbJ9o5xcR_LjW9ZGyE3cwLd5fr9ksSXa1an--EEA"
course_set=set()

driver = webdriver.Chrome()
driver.maximize_window()
action = ActionChains(driver)



#################################
driver.get(NTE_URL)
rows = driver.find_elements(By.XPATH,'//*[@id="content"]/article/div[2]/table/tbody/tr')
for i in rows:
    cols=i.find_elements(By.TAG_NAME,'td')
    # getting link and course_code
    class_code=write_num(cols[0].text)
    if (int(class_code)>=603 and int(class_code)<=639):
        continue
    driver.execute_script("arguments[0].scrollIntoView();", cols[0])
    cols[0].click()

    if(int(class_code)!=602):
        course_table=WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="content"]/article/div[2]/table/tbody/tr')))[1:]
        for course in course_table:
            course_code = write_num(course.find_elements(By.TAG_NAME, 'td')[0].text)
            full_code = class_code + ("0" if len(course_code) == 3 else "") + course_code
            course_set.add(full_code)
    else:           # mld specific case their xpath and table structure are different
        course_table = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="content"]/div[2]/table/tbody/tr')))[1:]
        for course in course_table:
            course_name=course.find_elements(By.TAG_NAME, 'td')[0].text
            course_code = write_num(course_name)
            class_code = mld_switch(course_name)
            full_code = class_code + ("0" if len(course_code) == 3 else "") + course_code
            course_set.add(full_code)
    driver.back()

end = time.time()
print("all NTEs recorded in : ",end-start," seconds")
#################################


first_time = True
for class_code in class_codes:

    old_url = driver.current_url
    driver.get(url1 + site_package + url2 + class_code + url3)
    WebDriverWait(driver, 10).until(lambda url_check: driver.current_url != old_url)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)

    # searched
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(("xpath", '//*[@id="submitSearchForm"]'))).click()
    time.sleep(0.5)

    if first_time:
        first_time = False
        # all entries selected
        drop_mask = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="s2id_autogen4"]/a')))
        driver.execute_script("arguments[0].scrollIntoView()",
                              driver.find_element(By.XPATH, '//*[@id="row_"]/div/div/div[2]/div/div[1]/div[2]'))
        action.move_to_element(drop_mask).click().perform()

        drop_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="select2-drop"]/ul/li[4]/div')))
        action.move_to_element(drop_button).click().perform()

        # columns
        column = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="okzTools_SearchResults"]/div')))
        column.click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="SearchResults_column_toggler"]/label[1]'))).click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="SearchResults_column_toggler"]/label[7]'))).click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="SearchResults_column_toggler"]/label[8]'))).click()

    # print department name
    dep_name=WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="s2id_selectProgram"]/a/span[1]'))).text
    print(dep_name)

    # print table
    table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'SearchResults'))).text
    for row in table.splitlines()[1:]:
        if len(row)>7 and (row[:7] in course_set):
            print(row)
    print("")

driver.quit()

end = time.time()
print("done ",end-start," seconds")