from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess
import sys
import json
import os

secrets = "secrets.json"

with open(secrets) as f:
    keys = json.loads(f.read())

def get_secret(setting, keys=keys):
    try:
        return keys[setting]
    except KeyError:
        msg = f"Set the {setting} environment variable"
        raise ValueError(msg)


def export():
    url = 'https://www.overleaf.com/login'
    cookie_name = 'overleaf_session2'
    download_script = 'download_project.sh'

    driver = webdriver.Firefox()
    driver.get(url)

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )

    email_input.send_keys(get_secret("EMAIL"))
    password_input.send_keys(get_secret("PASSWORD"))
    elements = driver.find_elements(By.CLASS_NAME, 'btn-primary')
    login_button = elements[0]
    login_button.click()
    time.sleep(15) # in case of captcha

    cookies = driver.get_cookies()

    for cookie in cookies:
        if cookie['name'] == cookie_name:
            session = cookie['value']
            subprocess.call([f"./{download_script}", session])
            driver.quit()

export()
