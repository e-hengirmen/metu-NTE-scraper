import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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

print("check")