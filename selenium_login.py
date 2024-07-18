from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.by import By

import time
import os


def click_button(element):
    action = ActionChains(driver)
    action.click(on_element=element)
    action.perform()
    time.sleep(3)


def set_secret(name, value):
    if name == "_csrf":
        with open("secrets.yaml", "r") as secrets_yaml:
            secrets = secrets_yaml.read()
            secrets = secrets.replace("CSRF_VALUE", value)

        with open("secrets.yaml", "w") as secrets_yaml:
            secrets_yaml.write(secrets)
    elif name == "session":
        with open("secrets.yaml", "r") as secrets_yaml:
            secrets = secrets_yaml.read()
            secrets = secrets.replace("SESSION_VALUE", value)

        with open("secrets.yaml", "w") as secrets_yaml:
            secrets_yaml.write(secrets)


driver = webdriver.Firefox()

driver.get("https://pp-services.signin.education.gov.uk/")

start_button = driver.find_element(By.LINK_TEXT, "Start now")

click_button(start_button)

username = os.getenv("USER")
password = os.getenv("PASSWORD")

username_box = driver.find_element(By.ID, "username")
username_box.send_keys(username)

password_box = driver.find_element(By.ID, "password")
password_box.send_keys(password)

login_button = driver.find_element(By.XPATH, "//button[@class='govuk-button']")

click_button(login_button)

print(driver.title)


if driver.title == "Access DfE services":
    for cookie in driver.get_cookies():
        print(f"Cookie Name: {cookie['name']}\nCookie Value: {cookie['value']}")

        set_secret(cookie['name'], cookie['value'])


# TODO run gospider --site https://pp-services.signin.education.gov.uk --cookie "session=; _csrf=" --blacklist "(\.(js|png|ico|css|1)|session\/end|signout)" --output ./ -vv --debug --json -d 4
# TODO parse json / get URLs
# TODO run nuclei -l URLS.txt -sf secrets.yaml

driver.quit()



