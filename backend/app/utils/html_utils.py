import requests
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def check_is_it_url(text):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, text) is not None


def get_page_content(url):
    driver_path = os.getenv("SEL_DRIVER_PATH", "/home/serip/chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
    browser.get(url)
    timeout = 5
    try:
        element = EC.presence_of_element_located((By.CLASS_NAME, 'job-description'))
        WebDriverWait(browser, timeout).until(element)
    except TimeoutException:
        print("timeout")
    return browser.page_source


def parse_job_description_from_html(html):
    parsed_html = BeautifulSoup(html, "html.parser")
    div = parsed_html.body.find('div', attrs={'class': 'job-description'})
    for elem in parsed_html.find_all(["a", "p", "div", "h3", "br", "li"]):
        elem.append('\n')
    return div.text
