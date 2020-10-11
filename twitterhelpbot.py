import time
from datetime import datetime
import os
from twitter import Twitter
from ff import init as browser_init
import argparse
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import urllib.parse
import utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retweet links in twitter helper bot')
    parser.add_argument('--wait', default=10, type=int)
    parser.add_argument('--continuation', action='store_true', default=False)
    parser.add_argument('--headless', action='store_true', default=False)
    parser.add_argument('--executable_path', default=r"ff\App\Firefox64\firefox.exe")
    parser.add_argument('--profile_path', default=r"ff\Data\profile")
    parser.add_argument('--history', default="history.json")

    args = parser.parse_args()

    commands = ["香港直擊", "國際戰線", "外語新聞"]
    with browser_init("https://web.telegram.org/#/im?p=@TwitterHelpBot", executable_path=args.executable_path, profile_path=args.profile_path, headless=args.headless) as browser:
        browser.wait(By.CLASS_NAME, "im_dialog", args.wait)
        time.sleep(5)
        input = browser.find_element_by_class_name("composer_rich_textarea")
        urls = []
        for command in commands:
            input.send_keys("/task")
            input.send_keys(Keys.ENTER)
            time.sleep(2)
            browser.find_elements_by_xpath(f"//button[text()='{command}...']")[-1].click()
            time.sleep(5)

            for url in [a.get_attribute('href') for a in browser.find_elements_by_xpath("(//div[@class='im_message_text'])[last()]/a")[:-1]]: 
                urls.append(urllib.parse.unquote(re.search('url=(.+)', url).group(1)))
        
        utils.retweet_all(browser, urls, args.history)

    print("bye " + str(datetime.now()))
    print("")

    quit()
