#!/usr/bin/env python3
import sys, traceback
import time
import re

from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request

def is_match(url):
    pattern = re.compile(r'https://.*/.*.png')
    return pattern.match(url)

def get_page_i(url, i):
    return "{}/read/page/{}".format(url, i)

def get_scrambled_img_links(url):

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-web-security')
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)

    driver.get(get_page_i(url, 1))
    driver.find_element_by_class_name('js-close').click()
    while True:
        driver.find_element_by_css_selector('*').send_keys(Keys.LEFT)
        if driver.current_url == url + '/read/page/end':
            break
        time.sleep(.5)
    imgs = []
    for request in driver.requests:
        if request.response:
            # print(
                    # request.path,
                    # request.response.status_code,
                    # request.response.headers['Content-Type']
                    # )
            if is_match(request.path):
                imgs.append(request.path)

    driver.close()
    return imgs

def get_imgs(imgs):
    for i, link in enumerate(imgs):
        urllib.request.urlretrieve(link, "{}.png".format(i))

if __name__ == "__main__":
    URL = sys.argv[1]
    imgs = get_scrambled_img_links(URL)
    get_imgs(imgs)