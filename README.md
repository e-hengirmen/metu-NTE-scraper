# Metu NTE scraper
Metu NTE scraper project was created for educational purposes and community needs. It comprises of 3 tools for 3 different jobs:
1. `main.py` that collects the NTE's given to ur department
2. `NewCourseAlarm.py` that alerts the user if there are new courses that are given to ur department(uses "out2.txt")
3. `capacityCheck.py` that searches through courses given to ur department and finds those with unused capacity(uses "out2.txt")

Note: `capacityCheck.py` uses the CNN model [Basic-number-captcha-solver](https://github.com/e-hengirmen/Basic-number-captcha-solver/edit/master/README.md) that was specifically developed to be used in this scraper. The current model works with 99.94% accuracy.

## Getting Started
These instructions will help you list Non-Technical Elective courses given to your department in the current semester
## Prerequisites
Python 3.x  
Google Chrome   
selenium - An API for python to write functional/acceptance tests using Selenium WebDriver. 
Tensorflow - A free open-source library for AI and machine learning applications

you can install necessary packages with(including selenium and tensorflow):
```
sudo pip3 install -r requirements.txt
```
If u encounter any problems apply these commands:
```
pip install selenium webdriver_manager
python3 -m pip install webdriver-manager --upgrade
python3 -m pip install packaging
```
## Options
Before running the code make sure you change the below variables inside `main.py` to neccessary values:
* For `main.py` and `NewCourseAlarm.py`
  * myDEPT (contains department abbreviation to help find courses given to that department)(default value set for ceng change it to your department's code)
  * class_codes (contains departments that give NTE courses)(you can delete the department numbers that you do not want in your list)
* For `capacityCheck.py`
  * Username (fill your metu username)(It is only used to access metu capacity checker which is unaccessable withput a username and password)
  * Password (fill your metu password))(It is only used to access metu capacity checker which is unaccessable withput a username and password)
## Running the code
Use below line to scrape current NTE list(it takes about 6 minutes)
```
python main.py >out2.txt
```
After the creation of `out2.txt` use below command to check for new courses given to ur department:
```
python NewCourseAlarm.py
```
After the creation of `out2.txt` use below command to check for capacities of the listed courses:
```
python capacityCheck.py
```
## How it collects
`capacityCheck.py` simulates the user using selenium.  
The program first goes into the course capacity section by entering user's password and username . After this point until every course in "out2.txt" is exhausted it answers captchas by first uploading the captcha image which is send to the CNN model provided which solves the captcha and the result gets sent back to the browser.  
  
You can see how it looks when `capacityCheck.py` is running from below gif. 
  
![](media/capacityRunning.gif)
