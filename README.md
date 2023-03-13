# Metu NTE scraper
Metu NTE scraper project was created for educational proposes and community needs. It comprises of 3 tools for 3 different jobs:
1. `main.py` that collects the NTE's given to ur department
2. `NewCourseAlarm.py` that alerts the user if there are new courses that are given to ur department(uses "out2.txt")
3. `capacityCheck.py` that searches through courses given to ur department and finds those with unused capacity(uses "out2.txt")
## Getting Started
These instructions will help you list Non-Technical Elective courses given to your department in the current semester
## Prerequisites
Python 3.x  
Google Chrome   
selenium - An API for python to write functional/acceptance tests using Selenium WebDriver.

you can install selenium with either pip:
```
sudo pip3 install selenium
```
OR if you have anaconda:
```
conda install -c conda-forge selenium
```
## Setup
After installing the prerequisites [download the corresponding chrome webdriver from here](https://chromedriver.chromium.org/downloads) according to your chrome version. 

If you are using **Windows** unzip the chromedriver to your github folder. 

If you are using **Ubuntu** follow the steps below instead:
```
unzip chromedriver_linux64.zip
chmod +x chromedriver
sudo mv chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
```
after this you can check chromedriver version with:
```
chromedriver --version
```
## Options
Before running the code make sure you change the below variables inside `main.py` to neccessary values:
* For `main.py` and `NewCourseAlarm.py`
  * myDEPT (contains department abbreviation to help find courses given to that department)(default value set for ceng change it to your department's code)
  * class_codes (contains departments that give NTE courses)(you can delete the department numbers that you do not want in your list)
* For `NewCourseAlarm.py`
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

Edit: Added a CNN classifier to the capacity checker with 99.8% accuracy. Currently there are no problems.
