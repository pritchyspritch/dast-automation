from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time
import os
import subprocess
import yaml
import platform
import json
import argparse


def set_secret(name, value):
    if name == "_csrf":
        os.environ["CSRF"] = value
        with open("secrets.yaml", "r") as secrets_yaml:
            secrets = secrets_yaml.read()
            secrets = secrets.replace("CSRF_VALUE", value)

        with open("secrets.yaml", "w") as secrets_yaml:
            secrets_yaml.write(secrets)
    elif name == "session":
        os.environ["SESSION"] = value
        with open("secrets.yaml", "r") as secrets_yaml:
            secrets = secrets_yaml.read()
            secrets = secrets.replace("SESSION_VALUE", value)

        with open("secrets.yaml", "w") as secrets_yaml:
            secrets_yaml.write(secrets)


def run_gospider():
    with open("secrets.yaml", "r") as secrets_yaml:
        yaml_secrets = yaml.safe_load(secrets_yaml)
        cookies_list = yaml_secrets["static"][0]["cookies"]

    for cookie in cookies_list:
        if cookie["key"] == "session":
            session = cookie["value"]
        elif cookie["key"] == "_csrf":
            csrf = cookie["value"]

    gospider = subprocess.run(f"gospider --site https://pp-services.signin.education.gov.uk --cookie 'session={session}; _csrf={csrf}' --blacklist '(\.(js|png|ico|css|1)|session\/end|signout)' --output ./ -vv --debug --json -d 4", shell=True)


def get_spider_urls():
    with open("pp-services_signin_education_gov_uk", "r") as urls_file:
        urls = urls_file.readlines()
    
    urls_list = []
    for url in urls:
        url_json = json.loads(url)

        match url_json["type"]:
            case "subdomain":
                if url_json["output"].endswith("signin.education.gov.uk"):
                    urls_list.append(f"https://{url_json['output']}")
            case "url":
                urls_list.append(url_json["output"])
            case "form":
                if url_json["output"].endswith(".ico"):
                    continue
                elif url_json["output"].endswith(".png"):
                    continue
                elif "css" in url_json["output"]:
                    continue
                elif "signin.education.gov.uk" not in url_json["output"]:
                    continue
                else:
                    urls_list.append(url_json['output'])
            case "javascript":
                continue
    
    with open("urls.txt", "w") as output_urls:
        for url in list(set(urls_list)):
            output_urls.write(f"{url}\n")


def run_nuclei():
    nuclei = subprocess.run("nuclei -l urls.txt -sf secrets.yaml -json-export nuclei_output.json", shell=True)


def dfe_login():
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)


    driver.get("https://pp-services.signin.education.gov.uk/")

    WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.LINK_TEXT, "Start now"))).click()


    username = os.getenv("USER")
    password = os.getenv("PASSWORD")

    username_box = driver.find_element(By.ID, "username")
    username_box.send_keys(username)

    password_box = driver.find_element(By.ID, "password")
    password_box.send_keys(password)

    password_box.send_keys(Keys.ENTER)


    time.sleep(3)
    print(driver.title)


    if driver.title == "Access DfE services":
        for cookie in driver.get_cookies():
            print(f"Cookie Name: {cookie['name']}\nCookie Value: {cookie['value']}")

            set_secret(cookie['name'], cookie['value'])

        driver.quit()
        
        # Run the spider and nuclei from python if local - do in actions steps in github
        if platform.system() == "Darwin":
            run_gospider()
            get_spider_urls()
            run_nuclei()

    else:
        driver.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Can be dfe-login, spider, or nuclei")

    args = parser.parse_args()

    if args.command == "dfe-login":
        dfe_login()
    elif args.command == "spider":
        run_gospider()
    elif args.command == "nuclei":
        get_spider_urls()
        run_nuclei()




