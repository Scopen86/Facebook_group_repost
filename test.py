import time
import pickle
import os
import argparse

from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

# Create an argument parser
parser = argparse.ArgumentParser(description="Facebook group repost script")
parser.add_argument("-l", "--login", action="store_true", help="Force login, even if cookies exist")
parser.add_argument("--credential_file", nargs='?', default="credential.txt", help="Path to the credential file")
parser.add_argument("--group_links_file", nargs='?', default="group_links.txt", help="Path to the group links file")
parser.add_argument("--content_file", nargs='?', default="content.txt", help="Path to the content file")
args = parser.parse_args()

driver = webdriver.Edge(options=Options(), service=Service(EdgeChromiumDriverManager().install()))
driver.maximize_window()  # Maximize the browser window

def login():
    with open(args.credential_file, "r") as file:
        email, password = file.read().splitlines()

    url = "https://www.facebook.com/"

    driver.get(url)

    email_elem = driver.find_element(By.ID, "email")
    pass_elem = driver.find_element(By.ID, "pass")
    login_btn = driver.find_element(By.NAME, "login")

    email_elem.send_keys(email)
    time.sleep(2)
    pass_elem.send_keys(password)
    time.sleep(3)
    login_btn.click()
    input("Press Enter to continue...")

    # Save cookies to a file
    with open("cookies.pkl", "wb") as file:
        pickle.dump(driver.get_cookies(), file)


# Load content
with open(args.group_links_file, 'r', encoding='utf-8') as f:
    group_links = f.read().splitlines()

with open(args.content_file, 'r', encoding='utf-8') as f:
    post_content = f.read()

# Assuming the images are in the /Images folder
image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Images")

# Login to Facebook
url = "https://www.facebook.com/"
driver.get(url)
time.sleep(2)  # Wait for the page to load

# Load cookies from file
if args.login:
    login()
else:
    try:
        with open("cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()
    except FileNotFoundError:
        login()

# Loop through each group link
for index, group_link in enumerate(group_links):
    driver.get(group_link)
    time.sleep(5)  # Wait for the page to load

    # Find the post input area using the parent div of the placeholder text
    post_placeholder = driver.find_element(By.XPATH, "//span[contains(text(), 'Bạn viết gì đi...')]/parent::div")
    post_placeholder.click()  # Click on the parent div first
    time.sleep(2)  # Wait for the post area to load
    post_area = driver.find_element(By.XPATH, "//div[contains(@aria-label, '...') and @contenteditable='true']")  # Find the post area using the new criteria
    post_area.send_keys(post_content)
    time.sleep(2)  # Wait for the content to be entered

    # Upload images
    image_input_collapse = driver.find_element(By.XPATH, "//div[@aria-label='Ảnh/video']")
    image_input_collapse.click()
    time.sleep(2)  # Wait for the image input to expand
    
    for image in os.listdir(image_dir):
        upload_input = driver.find_element(By.XPATH, "//input[@accept='image/*,image/heif,image/heic,video/*,video/mp4,video/x-m4v,video/x-matroska,.mkv' and @type='file']")
        image_path = os.path.join(image_dir, image)
        upload_input.send_keys(image_path)
        time.sleep(5)
    
    # Post the content
    post_button = driver.find_element(By.XPATH, "//div[@aria-label='Đăng']")
    post_button.click()
    time.sleep(5)  # Wait for the post to be submitted

input("Press Enter to exit...")

# Close the WebDriver
driver.quit()

