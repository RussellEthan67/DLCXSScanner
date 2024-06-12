from collections import deque
from selenium import webdriver
from urllib.parse import urlparse
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import DesiredCapabilities, FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException, UnexpectedAlertPresentException, NoAlertPresentException
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import requests
import time
import browser_cookie3
import tldextract
import pyautogui
import os

visited = set()
deep_links = set()
to_be_crawl = deque()


def deep_link(to_deep, driver):
    try:
        text = driver.find_element(By.XPATH, "//input[@type='text']")
        if text:
            text.send_keys("a")
            text.submit()
            time.sleep(1)
            deep_link = driver.current_url
            if deep_link != to_deep and "=" in deep_link:
                if deep_link not in deep_links:
                    deep_links.add(deep_link)
    except Exception:
        pass


def crawl_link(to_crawl, driver, info):
    current = driver.current_url
    parsed_url = urlparse(current)
    correct_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path.rsplit('/', 1)[0]}"
    correct_url = correct_url + "/" + to_crawl
    if to_crawl in visited or correct_url in visited:
        # Link has already been visited, skip processing
        return
    try:
        driver.get(to_crawl)
        visited.add(to_crawl)
    except InvalidArgumentException as e:
        driver.get(correct_url)
        visited.add(correct_url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links:
        link = link.get_attribute("href")
        dm = tldextract.extract(link)
        dmi = dm.domain
        if dmi == info and all(link not in a for a in [visited, to_be_crawl]):
            link = link.split('#')[0]
            if link.endswith(('.pdf', '.txt', '.png', '.jpg', '.jpeg', '.xls', '.xml', '.docx', '.doc')):
                pass
            else:
                cleaned_url = link.rstrip("#")
                to_be_crawl.append(cleaned_url)
    # If there is form contains links with selects option
    try:
        selects = driver.find_elements(By.TAG_NAME, "select")
        for select in selects:
            select_element = Select(select)
            options = select_element.options
            links = [option.get_attribute('value') for option in options]
            for link in links:
                if all(link not in a for a in [visited, to_be_crawl]):
                    link = link.split('#')[0]
                    if link.endswith(('.pdf', '.txt', '.png', '.jpg', '.jpeg', '.xls', '.xml', '.docx', '.doc')):
                        pass
                    else:
                        cleaned_url = link.rstrip("#")
                        to_be_crawl.append(cleaned_url)
    except NoSuchElementException:
        pass
    deep_link(to_crawl, driver)
    while len(to_be_crawl):
        url_to_crawl = to_be_crawl.popleft()
        crawl_link(url_to_crawl, driver, info)


def driver_init(url):
    options = webdriver.FirefoxOptions()
    options.profile = webdriver.FirefoxProfile(
        r"C:\Users\ASUS\AppData\Roaming\Mozilla\Firefox\Profiles\1ybom3sd.default-release"
    )
    driver = webdriver.Firefox(
        options=options, service=FirefoxService(GeckoDriverManager().install())
    )
    driver.get(url)
    urli = tldextract.extract(url)
    info = urli.domain
    cj = browser_cookie3.firefox()
    r = requests.get(url, cookies=cj)

    cookies = list(cj)

    for c in cookies:
        if c.domain == info:
            driver.add_cookie(
                {
                    "name": c.name,
                    "value": c.value,
                    "path": c.path,
                    "expiry": c.expires,
                    "domain": c.domain,
                }
            )
    return driver, info


def take_screenshot(url: str):
    folder_path = "C:\Users\ASUS\Desktop\Alat Skripsi\Screenshots"
    os.makedirs(folder_path, exist_ok=True)
    options = webdriver.FirefoxOptions()
    options.profile = webdriver.FirefoxProfile(
        r"C:\Users\ASUS\AppData\Roaming\Mozilla\Firefox\Profiles\1ybom3sd.default-release"
    )
    driver = webdriver.Firefox(
        options=options, service=FirefoxService(GeckoDriverManager().install())
    )
    driver.get(url)
    time.sleep(5)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_path = os.path.join(
        folder_path, f'xss_screenshot_with_alert_{timestamp}.png')
    pyautogui.screenshot(screenshot_path)
    driver.quit()
    return screenshot_path
