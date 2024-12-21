import os
import traceback
import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read variables from .env
MAILGUN_API_URL = os.getenv("MAILGUN_API_URL") 
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")  # Your Mailgun API key
FROM_EMAIL = os.getenv("FROM_EMAIL")  # Sender's email address
TO_EMAIL = os.getenv("TO_EMAIL")  # Recipient's email address
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

def get_shadow_root(driver, element):
    return driver.execute_script("return arguments[0].shadowRoot", element)

def send_email_via_mailgun(otp_code):
    """Send email via Mailgun API."""
    try:
        response = requests.post(
            MAILGUN_API_URL,
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": FROM_EMAIL,
                "to": [TO_EMAIL],
                "subject": "Your Verification Code",
                "text": f"The verification code is: {otp_code}"
            }
        )
        if response.status_code == 200:
            print(f"Verification code sent to {TO_EMAIL}")
        else:
            print(f"Failed to send email: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred while sending email: {e}")

options = webdriver.ChromeOptions()
options.headless = False
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 60)

# Login to the web app
driver.get("https://learn.uwaterloo.ca/")

# Input username
username_input = driver.find_element(By.ID, "userNameInput")
username_input.send_keys(USERNAME)

# Click the "Next" button
next_button = driver.find_element(By.ID, "nextButton")
next_button.click()

# Wait for the password input to appear
password_input = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "passwordInput"))
)
password_input.send_keys(PASSWORD)

# Click the login button
login_button = driver.find_element(By.ID, "submitButton")
login_button.click()

while True:
    try:
        # Wait for the verification code to appear
        code_element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "verification-code"))
        )
        code = code_element.text
        print(f"Verification code retrieved: {code}")
        trust_browser_button = wait.until(
            EC.presence_of_element_located((By.ID, "trust-browser-button"))
        )
        trust_browser_button.click()
        print("Browser trusted, proceeding...")

        # Retry logic for finding the dropdown button
        dropdown_found = False
        while not dropdown_found:
            try:
    # Wait for the presence of all the div elements containing the shadow DOM
                div_elements = wait.until(
                      EC.presence_of_all_elements_located(
                          (By.CSS_SELECTOR, "div.d2l-navigation-s-notification"))
                  )

                  # Iterate through each div to find the specific button inside the shadow DOM
                for div_element in div_elements:
                    try:
                        # Locate the d2l-navigation-dropdown-button-icon inside the div
                        d2l_button_element = div_element.find_element(
                            By.CSS_SELECTOR, "d2l-navigation-dropdown-button-icon")
                        shadow_root = get_shadow_root(driver, d2l_button_element)

                        # Try to locate the button with a unique ID (e.g., 'd2l-uid-191')
                        button_id = shadow_root.find_element(
                            By.CSS_SELECTOR, "button").get_attribute("id")
                        print(f"Found button with id: {button_id}")
                        # Locate the button using the id directly
                        if button_id == "d2l-uid-22":  # Replace with the appropriate id or logic
                            button = shadow_root.find_element(
                                By.ID, button_id)
                            button.click()
                            print(f"Button {button_id} clicked successfully!")
                            dropdown_found = True  # Stop after clicking the first matching button (remove if you want to continue)
                            break  # Stop after clicking the first matching button (remove if you want to continue)

                    except Exception as inner_e:
                                  # Handle case where the button or shadow root is not found in this specific div
                        print(
                            f"Error interacting with div: {inner_e}")
                        continue

            except Exception as e:
                error_type = type(e).__name__
                print(f"An error of type '{error_type}' occurred: {e}")

        # Scrape data from the dropdown
        items = driver.find_elements(By.CLASS_NAME, "ul.vui-list li.dl2-datalist-item")
        print("found items")
        for item in items:
            try:
                title = item.find_element(
                    By.CSS_SELECTOR, "a.dl2-link").text
                due_date = item.find_element(
                    By.CSS_SELECTOR, "span.vui-emphasis").text
                print(f"Title: {title}, Due Date: {due_date}")
            except NoSuchElementException:
                print("Item not found.")
                continue

        # Check the last item's fuzzy date
        last_item = items[-1]
        try:
            fuzzy_date = last_item.find_element(
                By.CSS_SELECTOR, "abbr.d2l-fuzzy").get_attribute("title")
            last_date = datetime.strptime(fuzzy_date, "%B %d at %I:%M %p").date()
            today = datetime.now().date()

            if last_date != today:
                print("Last item is not from today. Stopping load more.")
                break
        except NoSuchElementException:
            print("No fuzzy date found in the last item. Stopping load more.")
            break

        # Handle "Load More" button
        try:
            load_more_button = driver.find_element(By.CLASS_NAME, "d2l-load-more")
            if load_more_button:
                load_more_button.click()
        except NoSuchElementException:
            print("No 'Load More' button found. Ending loop.")
            break

    except NoSuchElementException as e:
        print(f"An explicit element error occurred: {e}")
        break  # Stop the loop as the required element isn't found

    except Exception as e:
        error_type = type(e).__name__
        print(f"An error of type '{error_type}' occurred: {e}")
        
        # Optionally log the full stack trace
        print("\nStack Trace:")
        traceback.print_exc()