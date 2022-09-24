# Metu NTE scraper
This project was created for educational proposes and community needs.
## Getting Started
These instructions will help you get Non-Technical Elective
## Prerequisites
Python 3.x\
Google Chrome\ 
selenium - An API for python to write functional/acceptance tests using Selenium WebDriver.

you can install selenium with either pip:
```
sudo pip3 install selenium
```
or if you have anaconda:
```
conda install -c conda-forge selenium
```
## Setup
After installing the prerequisites [download the corresponding chrome webdriver from here](https://chromedriver.chromium.org/downloads) according to your chrome version. 

If you are using Windows unzip the chromedriver to your github folder. 

If you are using ubuntu follow the steps below instead:
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
Before running the code make sure you change the below variables inside 'maim.py' to neccessary values:
* dept_code (contains department code to help find courses given to that department)(default value set for ceng change it to your department's code)
* class_codes (contains departments that give NTE courses)(you can delete those that you dont want in your list)
* semester (contains year and semester for example currently set to 20221 meaning 2022-2023 fall)(change according to current semester)

## Running the code
Use below line to scrape current NTE list(it takes about 2 minutes)
```
python main.py >output
```
