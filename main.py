# -*- coding: utf-8 -*-
import time
import traceback
from coords import parse_dms
from pyscraper.selenium_utils import wait_for_xpath, get_headed_driver, wait_for_classname, wait_for_tag, wait_for_visible_id
from pyscraper.data_dump_file import DataFile
from pyscraper.selenium_utils import get_headless_driver

def get_by_region(driver, href, output):
    driver.get(href)
    print href
    wait_for_classname(driver, 'finder-listing')
    wait_for_classname(driver, 'gutter-bottom-xxs')
    dispensaries = driver.find_elements_by_class_name('finder-listing')
    for d_index in range(1, len(dispensaries)):
        print 'Dispensary', d_index
        wait_for_classname(driver, 'finder-listing')
        wait_for_classname(driver, 'gutter-bottom-xxs')
        dispensaries = driver.find_elements_by_class_name('finder-listing')
        # print(dispensary.text)
        dispensary = dispensaries[d_index]
        if 'Searching' in dispensary.text:
            break
        wait_for_tag(dispensary, 'a')
        d_link = dispensary.find_element_by_tag_name('a')
        d_link.click()
        try:
            print driver.current_url
            wait_for_tag(driver, 'iframe')
            time.sleep(1)
            iframe = driver.find_element_by_tag_name('iframe')
            driver.switch_to.frame(iframe)
            try:
                map_degrees = wait_for_xpath(driver, '//*[@id="mapDiv"]/div/div/div[9]/div/div/div/div[1]/div[1]')
            except:
                map_degrees = driver.find_element_by_xpath('//*[@id="mapDiv"]/div/div/div[9]/div/div/div/div[1]/div[1]')
            degrees = map_degrees.text
            latitude = degrees.split()[0]
            longitude = degrees.split()[1]
            coords_lat = parse_dms(latitude)
            coords_long = parse_dms(longitude)
            driver.switch_to.default_content()
            # wait_for_xpath(driver, '//*[@id="main"]/div/section/div[2]/div[2]/section[2]/div[2]/div[1]/div[2]/label/a')
            business_name = driver.find_element_by_xpath('//*[@id="main"]/div/section/div[1]/div[3]/div/h1').text
            print business_name
            address = driver.find_element_by_xpath(
                '//*[@id="main"]/div/section/div[2]/div[2]/section[2]/div[1]/div/a/label').text
            city = driver.find_element_by_xpath(
                '//*[@id="main"]/div/section/div[2]/div[2]/section[2]/div[1]/div/a/span[1]').text
            state = driver.find_element_by_xpath(
                '//*[@id="main"]/div/section/div[2]/div[2]/section[2]/div[1]/div/a/span[2]').text
            phone = driver.find_element_by_xpath(
                '//*[@id="main"]/div/section/div[2]/div[2]/section[2]/div[2]/div[1]/div[1]/label').text
            try:
                website = driver.find_element_by_xpath(
                    '//*[@id="main"]/div/section/div[2]/div[2]/section[2]/div[2]/div[1]/div[2]/label/a').get_attribute(
                    'href')
            except:
                website = ''
            print business_name, address, city, state, phone, website, str(coords_lat), str(coords_long)
            output.write_values(business_name, address, city, state, phone, website, str(coords_lat), str(coords_long))
            # print 'fuck you'
        finally:
            driver.back()


driver = get_headed_driver(no_sandbox=True)
output = DataFile('420')
with output:
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
            try:
                get_by_region(driver, href, output)
                    # print d_link.text
            except:
                traceback.print_exc()
                try:
                    get_by_region(driver, href, output)
                except:
                    continue
            print 'region done'
    finally:
        driver.close()

