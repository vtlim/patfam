#!/usr/bin/env python3

import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


# set chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


def obtain_target_page(driver, target_url):
    driver.get(target_url)
    return True

def navigate_front_page(driver, front_page_url, input_num):
    driver.get(front_page_url)

    inputElement = driver.find_element_by_id("simpleSearchForm:fpSearch:input")
    inputElement.send_keys(input_num)
    inputElement.send_keys(Keys.ENTER)

    return True


def navigate_target_page(driver):

    search_class = "ps-biblio-data--biblio-card"
    try:
        mydata = driver.find_element_by_class_name(search_class)
    except NoSuchElementException as e:
        return "UNDEFINED"

    # get text bt "Priority Data" and "Publication Language"
    priority_data = re.search('Priority Data(.*)Publication Language',
        mydata).group(1)

    # split the priority data, of form: 09/418,640 15.10.1999 US
    clean_priority_data = priority_data.split()[0]

    return clean_priority_data


def get_wipo_identifiers(input_num, doc_type):

    front_page_url = "https://patentscope.wipo.int/search/en/search.jsf"
    target_page_prefix = "https://patentscope.wipo.int/search/en/detail.jsf?docId="
    use_in_url = False

    # if pubNo, circumvent the search page and use pubNo in URL directly
    # works whether the number is WO2007* or WO07*
    if (input_num[:2].lower() == "wo") and (doc_type == "publication"):
        try:
            float(input_num[2:])
            use_in_url = True
        except ValueError:
            pass

    # create a chrome webdriver
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)

    if use_in_url:
        target_url = target_page_prefix + input_num
        print(f"  Going to {target_url}")
        obtain_target_page(driver, target_url)

    else:
        print(f"  Searching {input_num} on {front_page_url}")
        navigate_front_page(driver, front_page_url, input_num)

    # assuming we're on target page, scrape biblio info
    # return is "UNDEFINED" if not on the target page or biblio missing
    clean_priority_data = navigate_target_page(driver)

    if clean_priority_data == "UNDEFINED":
        return clean_priority_data

    return { "parent": [clean_priority_data], "child": [], "uncategorized": [] }

