# -*- coding: utf-8 -*-
import time
from coords import parse_dms
from pyscraper.selenium_utils import wait_for_xpath, get_headed_driver, wait_for_classname, wait_for_tag, wait_for_visible_id
driver = get_headed_driver()
try:
    driver.get('https://www.leafly.com/finder/browse')
    # time.sleep(5)


    # THE FUCK MODALS SECTION
    eligible = wait_for_classname(driver, 'modal-content')
    twenty_one = eligible.find_element_by_tag_name('label')
    continue_button = eligible.find_element_by_tag_name('button')
    twenty_one.click()
    continue_button.click()
    print 'passed first modal'
    time.sleep(2)
    sign_up = wait_for_classname(driver, 'modal-content', time=60)
    close = sign_up.find_element_by_tag_name('i')
    close.click()
    print 'passed second modal'

    # driver.get('https://www.leafly.com/finder/browse')
    hrefs = []
    rows = driver.find_elements_by_class_name('spacer-bottom-md')
    for index, row in enumerate(rows[1:]):
        if 'Calgary' in row.text:
            print 'CANADA', index
            break
        links = row.find_elements_by_tag_name('a')
        if len(links) < 1:
            continue
        for link in links:
            hrefs.append(link.get_attribute('href'))

    for href in hrefs:
        driver.get(href)
        wait_for_classname(driver, 'finder-listing')
        wait_for_classname(driver, 'gutter-bottom-xxs')
        dispensaries = driver.find_elements_by_class_name('finder-listing')
        for dispensary in dispensaries[1:]:
            # print(dispensary.text)
            if 'Searching' in dispensary.text:
                break
            wait_for_tag(dispensary, 'a')
            d_link = dispensary.find_element_by_tag_name('a')
            d_link.click()
            try:
                wait_for_tag(driver, 'iframe')
                # time.sleep(3)
                iframe = driver.find_element_by_tag_name('iframe')
                driver.switch_to.frame(iframe)
                map_degrees = wait_for_xpath(driver, '//*[@id="mapDiv"]/div/div/div[9]/div/div/div/div[1]/div[1]')
                degrees = map_degrees.text
                latitude = degrees.split()[0]
                longitude = degrees.split()[1]
                coords_lat = parse_dms(latitude)
                coords_long = parse_dms(longitude)
                driver.switch_to.default_content()
                business_name = driver.find_element_by_xpath('//*[@id="main"]/div/section/div[1]/div[3]/div/h1').text
                address = driver.find_element_by_xpath('//*[@id="main"]/div/section/div[2]/div[2]/section[2]/div[1]/div/a/label').text
                city = driver.find_element_by_xpath('//*[@id="main"]/div/section/div[2]/div[2]/section[2]/div[1]/div/a/span[1]').text
                state = driver.find_element_by_xpath('//*[@id="main"]/div/section/div[2]/div[2]/section[2]/div[1]/div/a/span[2]').text
                phone = driver.find_element_by_xpath('//*[@id="main"]/div/section/div[2]/div[2]/section[2]/div[2]/div[1]/div[1]/label').text
                website = driver.find_element_by_xpath('//*[@id="main"]/div/section/div[2]/div[2]/section[2]/div[2]/div[1]/div[2]/label/a').get_attribute('href')
                print 'fuck you'
            finally:
                driver.back()
            print d_link.text
        print 'd'
finally:
    driver.close()

