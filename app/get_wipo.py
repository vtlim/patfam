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
        mydata = mydata.text
    except NoSuchElementException as e:
        return "UNDEFINED"

    # === extract priority data ===
    # get text bt "Priority Data" and "Publication Language"
    # use re.DOTALL to search over multiple lines
    priority_data = re.search(r'Priority Data(.*?)Publication Language',
        mydata, re.DOTALL).group(1)

    # split the priority data, of form: 09/418,640 15.10.1999 US
    clean_priority_data = priority_data.split()[0].rstrip()

    # remove any spaces, punctuation (keep numbers/letters)
    clean_priority_data = re.sub(r'[^a-zA-Z0-9]', '', clean_priority_data)

    # === extract application number ===
    # if navigated to target page, the input provided must've been pubno
    app_num = re.search(r'International Application No.(.*?)International Filing Date',
        mydata, re.DOTALL).group(1)

    return clean_priority_data, app_num.strip()


def get_wipo_identifiers(input_num, doc_type):

    front_page_url = "https://patentscope.wipo.int/search/en/search.jsf"
    target_page_prefix = "https://patentscope.wipo.int/search/en/detail.jsf?docId="
    use_in_url = False

    # if pubNo, circumvent the search page and use pubNo in URL directly
    if (input_num[:2].lower() == "wo") and (doc_type == "publication"):

        pub_num_pieces = input_num[2:].split('/')

        # TODO generalize this
        # add leading two digits of year, separate 1980-1999 and 2000-2079
        if len(pub_num_pieces[0]) == 2:
            if int(pub_num_pieces[0]) >= 80:
                pub_num_pieces[0] = str(19) + str(pub_num_pieces[0])
            else:
                pub_num_pieces[0] = str(20) + str(pub_num_pieces[0])

        # add padding zeros in beginning if < 6 digits
        if len(pub_num_pieces[1]) < 6:
            num_zeros = 6 - len(pub_num_pieces[1])
            pub_num_pieces[1] = num_zeros*str(0) + str(pub_num_pieces[1])

        doc_id = "WO" + str(pub_num_pieces[0]) + str(pub_num_pieces[1])
        if len(doc_id) == 12:
            use_in_url = True

    # create a chrome webdriver
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)

    if use_in_url:
        target_url = target_page_prefix + doc_id
        print(f"\tNavigating directly to {target_url}")
        obtain_target_page(driver, target_url)

    else:
        print(f"\tSearching {input_num} on {front_page_url}")
        navigate_front_page(driver, front_page_url, input_num)

    # assuming we're on target page, scrape biblio info
    # return is "UNDEFINED" if not on the target page or biblio missing
    clean_priority_data, app_num = navigate_target_page(driver)

    if clean_priority_data == "UNDEFINED":
        return clean_priority_data

    return { "parent": [clean_priority_data], "child": [], "uncategorized": [app_num] }

