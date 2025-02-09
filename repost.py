import time
import pickle
import os

from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

driver = webdriver.Edge(options=Options(), service=Service(EdgeChromiumDriverManager().install()))

def login():
    with open("credential.txt", "r") as file:
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

    driver.quit()

# Load content
with open('group_links.txt', 'r', encoding='utf-8') as f:
    group_links = f.read().splitlines()

with open('content.txt', 'r', encoding='utf-8') as f:
    post_content = f.read()

# Assuming the images are in the /Images folder
image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Images")

# Login to Facebook
url = "https://www.facebook.com/"
driver.get(url)
time.sleep(2)  # Wait for the page to load

try:
    # Load cookies from file
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
    post_area = driver.find_element(By.XPATH, "//div[@aria-label = 'Bạn viết gì đi...' and @contenteditable='true']")  # Find the post area using the new criteria
    post_area.send_keys(post_content)
    time.sleep(2)  # Wait for the content to be entered

    # Upload images
    image_input_collapse = driver.find_element(By.XPATH, "//div[@aria-label = 'Ảnh/video']")
    image_input_collapse.click()
    for image in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image)
        upload_input = driver.find_element(By.XPATH, "//input[@accept='image/*,image/heif,image/heic,video/*,video/mp4,video/x-m4v,video/x-matroska,.mkv']")
        upload_input.send_keys(image_path)
        time.sleep(5)
    
    # Post the content
    post_button = driver.find_element(By.XPATH, "//div[@aria-label='Đăng']")
    post_button.click()
    time.sleep(5)  # Wait for the post to be submitted

input("Press Enter to exit...")

# Close the WebDriver
driver.quit()

