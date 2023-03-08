#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import csv
import time

driver_path = "/opt/brave.com/chromedriver"
browser_path = "/opt/brave.com/brave/brave"

meetings_uri = "http://url8366.eventpt.com/ls/click?upn=UOxl2ZR7g7Zo4e65Le9g9RLAMsRI7J6RGu2VI4ckmQMilEDFUmhNUPXM2auBzAn1YkwkW8vrAku9I3skbUkA6BhxRshiScFfj5Ijjsd-2B7cbz1Q5-2FA-2BZUAYoibCH2kyspyjgZcKdZpOeM88ghIcVf60-2BP-2F2FN-2BP2icieGJXad0vUya2Uw6cSLWUGP9xhtWoBaYklLR6ipxG3EiBbA4sV8Ow-3D-3DAEvZ_uAGIKxVHnzoGVmPcnUwHmUO3oyuWp5ypUQ6ICqQVxqVqo9QU4UjR3jYEWbT4wJ87mZCZ-2FxPTch-2BJA45J3WCtvzENa-2Bvm-2Bx185uzabmgRtQqG1dw78QFm3SeoL3ttvvcO-2FhiC8i2eu1xulXoExImbMIis9wGsy5pJ-2BDUWrXOgeyGxuH4U6XUOmLmxYSpbf-2BVM0KJU4aOE5A8fQkC5HQQ9Ym5QH8JE8-2FRce48fdXYb9PQ-3D"

header = ['org', 'url', 'description', 'type', 'stage', 'headcount', 'participants']

participant_header = ['id', 'name', 'linkedin', 'job title', 'market', 'sectors', 'functions']

def org_info(i, driver):
    return driver.find_element(By.XPATH, '//div[@data-index="'+str(i)+'"]')

def scrap_organization(org, driver, i, writer_participants):
    row = []
    a = org.find_element(By.XPATH, './/a[@class="link link--asBtn-md selection_card_participantDetails_link"]')
    row.append(a.text)
    row.append(a.get_attribute('href'))
    org_element = org.find_elements(By.XPATH, './/div[@class="selection_card_dataRow"]')
    row.append(org_element[0].find_element(By.XPATH, './/abbr').text)
    try:
        li_elements = org_element[1].find_elements(By.TAG_NAME, 'li')
        otype = ''
        for li_element in li_elements:
            otype += li_element.text + ' '
        row.append(otype)
    except Exception:
        row.append('-')
    try:
        row.append(org_element[1].find_element(By.XPATH, './/abbr').text)
    except Exception:
        row.append('-')
    try:
        row.append(org_element[2].find_element(By.XPATH, './/abbr').text)
    except Exception:
        row.append('-')
    # Participant button
    button = org.find_element(By.XPATH, '//div[@data-index="'+str(i)+'"]//button[@class="btn smooth btn--md btn--primary"]')
    driver.execute_script("arguments[0].scrollIntoView();", button)
    button.click()
    try:
        # Linked in button
        buttons = org.find_elements(By.XPATH, "//div[@class='selection_card_participantDetails']//button[@class='btn smooth btn--md btn--link']")
        for b in buttons:
            row_parts = ['-', '-', '-','-', '-', '-', '-']
            row_parts[0] = i

            driver.execute_script("arguments[0].scrollIntoView();", b)
            b.click()

            # LinkedIn data
            a = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, './/a[@class="link link--asBtn-md participant_details_actions_linkedin"]')))
            name = driver.find_element(By.XPATH, '//span[@class="name"]')
            jobt = driver.find_element(By.XPATH, '//span[@class="job_title"]')

            row_parts[1] = name.text
            row_parts[2] = a.get_attribute('href')
            row_parts[3] = jobt.text
            
            parent_div = driver.find_element(By.CLASS_NAME, "slider_body")

            values = parent_div.find_elements(By.CLASS_NAME, "form_value")
            labels = parent_div.find_elements(By.CLASS_NAME, "form_label")

            for value, label in zip(values, labels):
                if "Markets" in label.text:
                    row_parts[4] = value.text
                if "Sectors" in label.text:
                    row_parts[5] = value.text
                if "Function" in label.text:
                    row_parts[6] = value.text
                    
            print(*row_parts)
            writer_participants.writerow(row_parts)

            closebutton = org.find_element(By.XPATH, '//button[@class="slider_close btn smooth btn--md btn--iconOnly"]')
            closebutton.click()
            time.sleep(1)
    except Exception:
        pass
    # Add participants ID
    row.append(i)
    driver.execute_script("arguments[0].scrollIntoView();", button)
    time.sleep(0.5)
    button.click()
    time.sleep(0.5)
    #print(row)
    return (row)

def the_scrap():
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    options.binary_location = browser_path

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(meetings_uri)

    # Find the button element and click it
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn--link') and contains(text(), 'Update')]")))
    button.click()

    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'topNote_toggle')]")))
    button.click()

    virtuoso_scroller = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-id="virtuoso-scroller"]')))
    i = 0
    with open('orgs.csv', 'w', newline='') as csvfile, open('participants.csv', 'w', newline='') as csvparts:
        writer = csv.writer(csvfile)
        writer_participants = csv.writer(csvparts)
        writer_participants.writerow(participant_header)
        writer.writerow(header)
        while True:
            try:
                org = org_info(i, driver)
                row = scrap_organization(org, driver, i, writer_participants)
                writer.writerow(row)
                #print(i, *row)
                i += 1
            except NoSuchElementException:
                pass
            driver.execute_script("arguments[0].scrollTop += 100;", virtuoso_scroller)    
    
    # Close the webdriver
    time.sleep(200)
    driver.quit()


if __name__ == '__main__':
    the_scrap()
