from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import re

url = "http://www.chemspider.com/"
#Examples of CAS Numbers
cas = {'564483-18-7', '1160861-53-9'}


driver = webdriver.Chrome()
driver.get(url)
html_str = driver.page_source
f = open('cas.csv', 'w+')  # Output as a csv file
f.write("\"CAS\", \"Name\", \"SMILES\"\n")
for i in cas:
    quest = driver.find_element_by_xpath('/html/body/form/header/div/div[2]/label/input')
    quest.send_keys(i)
    driver.find_element_by_xpath('/html/body/form/header/div/div[2]/label/button/img').click()
    try:
        found = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/form/div[5]/div[1]/div[1]/div[1]/h3')))
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/form/div[5]/div[1]/div[2]/div[1]/div[2]/div/ul/li[2]/p/button')))
    except:
        f.write('\"%s\",\"0\",\"0\"\n' % i)
    else:
        if found.text == 'Found 1 result':  # if there is two results, you should decide it by yourself, so the result will not output here
            name = driver.find_element_by_xpath('/html/body/form/div[5]/div[1]/div[2]/div[1]/h1/span').text
            SMILES = driver.find_element_by_xpath(
                '/html/body/form/div[5]/div[1]/div[2]/div[1]/div[2]/div/ul/li[2]/p/button')
            text = SMILES.get_attribute('onmouseover')
            Sm = re.search(r"this, '(.*)', 'SMILES',", text)
            f.write('\"%s\",\"%s\",\"%s\"\n' % (i, name, Sm.group(1)))
            print(i)
        else:
            f.write('\"%s\",\"0\",\"0\"\n' % i)
f.close()
driver.close()
