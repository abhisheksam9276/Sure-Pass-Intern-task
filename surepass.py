import pandas as pd
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import json

def get_catcha():
    captcha = input("Enter Capctha: ")
    return captcha

def main(dl_no, dob):

    from webdriver_manager.chrome import ChromeDriverManager
    executable_path = {'executable_path': ChromeDriverManager().install()}
    driver = webdriver.Chrome(**executable_path)
    driver.get("https://parivahan.gov.in/rcdlstatus/?pur_cd=101")
    dl_input = '//*[@id="form_rcdl:tf_dlNO"]'
    dob_input = '//*[@id="form_rcdl:tf_dob_input"]'
    check_status = '//*[@id="form_rcdl:j_idt43"]/span'
    captcha_input = '//*[@id="form_rcdl:j_idt32:CaptchaID"]'

    driver.find_element_by_xpath(dl_input).send_keys(dl_no)
    driver.find_element_by_xpath(dob_input).send_keys(dob)
    captcha = get_catcha()
    driver.find_element_by_xpath(captcha_input).send_keys(captcha)
    driver.find_element_by_xpath(check_status).click()
    driver.implicitly_wait(2)
    captcha_status = '//*[@id="form_rcdl:j_idt13"]/div'

    
    try:
        driver.find_element_by_xpath(captcha_status)
        print("wrong Captcha")
        main(dl_no,dob)
    except:
        name_tag = driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt124"]/table[1]/tbody/tr[2]/td[1]/span')
        name_value = driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt124"]/table[1]/tbody/tr[2]/td[2]')
        doi_tag = driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt124"]/table[1]/tbody/tr[3]/td[1]/span')
        doi_value = driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt124"]/table[1]/tbody/tr[3]/td[2]')
        doe_tag = 'Date of Expiry'
        doe_value = driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt124"]/table[2]/tbody/tr[1]/td[3]')
        cov_tag = driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt187:j_idt190"]/span')
        cov_value = driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt187_data"]/tr/td[2]')
        cov_cat_tag = driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt187:j_idt188"]/span')
        cov_cat_value = driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt187_data"]/tr/td[1]')
        cov_issue_date_tag = driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt187:j_idt192"]/span')
        cov_issue_date_value = driver.find_element_by_xpath('//*[@id="form_rcdl:j_idt187_data"]/tr/td[3]')


        data = { name_tag.text : name_value.text,
                     doi_tag.text : doi_value.text,
                     doe_tag : doe_value.text,
                     cov_tag.text : cov_value.text,
                     cov_cat_tag.text : cov_cat_value.text,
                     cov_issue_date_tag.text : cov_issue_date_value.text
                }

        out_list = []
        for key in data:
            out_list.append(key)
            out_list.append(data[key])
        json_file = open('out.json','w')
        json.dump(out_list,json_file)
        json_file.close()

        print(out_list)




    driver.quit()

if __name__ == "__main__":
    dl_no = input("Enter Driving License Number :")
    dob = input ("Enter Date of Birth :")
    main(dl_no, dob)
