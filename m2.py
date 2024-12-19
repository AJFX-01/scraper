""" Ly """

import os
import pickle
from datetime import datetime
import requests
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

# Selenium Configuration
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Start maximized
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

# Function to load cookies if they exist
def load_cookies():
    try:
        with open("cookies.pkl", "rb") as cookie_file:
            cookies = pickle.load(cookie_file)
            for cookie in cookies:
                driver.add_cookie(cookie)
            print("Cookies loaded successfully.")
    except FileNotFoundError:
        print("No cookies found, logging in manually.")
    except Exception as e:
        print(f"Error loading cookies: {e}")

# Function to save cookies
def save_cookies():
    cookies = driver.get_cookies()
    with open("cookies.pkl", "wb") as cookie_file:
        pickle.dump(cookies, cookie_file)
    print("Cookies saved successfully.")

# Login to the web app if cookies don't exist
driver.get("https://learn.uwaterloo.ca/")
load_cookies()


if len(driver.get_cookies()) == 0:
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

    # Wait for login to complete, then save cookies
    WebDriverWait(driver, 20).until(EC.url_changes(driver.current_url))
    save_cookies()

# Main loop to handle code retrieval, sending email, and scraping data
browser_trusted = False  # Flag to check if browser has been trusted
authentication_completed = False  # Flag to track if the authentication is complete

while True:
    try:
        # Check if we are on the authenticated page by inspecting the URL or specific element
        current_url = driver.current_url
        if "https://learn.uwaterloo.ca/d2l/home" in current_url or driver.find_elements(By.ID, "dropdown-button"):
            print("Already authenticated, proceeding to dropdown...")
            dropdown_button = wait.until(
                EC.element_to_be_clickable((By.ID, "d2l-uid-22"))
            )
            dropdown_button.click()

            # Scrape data from the dropdown
            items = driver.find_elements(By.CSS_SELECTOR, "ul.vui-list li.dl2-datalist-item")
            for item in items:
                try:
                    title = item.find_element(By.CSS_SELECTOR, "a.dl2-link").text
                    due_date = item.find_element(By.CSS_SELECTOR, "span.vui-emphasis").text
                    print(f"Title: {title}, Due Date: {due_date}")
                except NoSuchElementException:
                    print("Item not found.")
                    continue

            last_item = items[-1]
            try:
                fuzzy_date = last_item.find_element(
                    By.CSS_SELECTOR, "abbr.d2l-fuzzy").get_attribute("title")
                # Parse the date to ensure it's the same day
                last_date = datetime.strptime(fuzzy_date, "%B %d at %I:%M %p").date()
                today = datetime.now().date()

                if last_date != today:
                    print("Last item is not from today. Stopping load more.")
                    break
            except NoSuchElementException:
                print("No fuzzy date found in the last item. Stopping load more.")
                break

            # Check if "Load More" button exists and handle it
            load_more_button = driver.find_element(By.CLASS_NAME, "d2l-load-more")
            if load_more_button:
                last_item = items[-1]
                last_date = last_item.find_element(By.CSS_SELECTOR, "abbr.d2l-fuzzy").get_attribute("title")
                if "December 14" in last_date:  # Replace "December 14" with the desired date format
                    load_more_button.click()
                    browser_trusted = True  # Mark the browser as trusted
            authentication_completed = True  # Authentication is already done
        else:
            # Wait for the verification code to appear (if not authenticated)
            code_element = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "verification-code"))
            )
            code = code_element.text
            print(f"Verification code retrieved: {code}")

            # Send the code via Mailgun API
            send_email_via_mailgun(code)

            # Wait for the "Trust This Browser" button to appear if not already trusted
            if not browser_trusted:
                try:
                    trust_browser_button = wait.until(
                        EC.presence_of_element_located((By.ID, "trust-browser-button"))
                    )
                    trust_browser_button.click()
                    print("Browser trusted, proceeding...")

                    dropdown_button = wait.until(
                        EC.element_to_be_clickable((By.ID, "d2l-uid-22"))
                    )
                    dropdown_button.click()

                    # Scrape data from the dropdown
                    items = driver.find_elements(By.CSS_SELECTOR, "ul.vui-list li.dl2-datalist-item")
                    for item in items:
                        try:
                            title = item.find_element(By.CSS_SELECTOR, "a.dl2-link").text
                            due_date = item.find_element(By.CSS_SELECTOR, "span.vui-emphasis").text
                            print(f"Title: {title}, Due Date: {due_date}")
                        except NoSuchElementException:
                            print("Item not found.")
                            continue

                    last_item = items[-1]
                    try:
                        fuzzy_date = last_item.find_element(
                            By.CSS_SELECTOR, "abbr.d2l-fuzzy").get_attribute("title")
                        # Parse the date to ensure it's the same day
                        last_date = datetime.strptime(fuzzy_date, "%B %d at %I:%M %p").date()
                        today = datetime.now().date()

                        if last_date != today:
                            print("Last item is not from today. Stopping load more.")
                            break
                    except NoSuchElementException:
                        print("No fuzzy date found in the last item. Stopping load more.")
                        break

                    # Check if "Load More" button exists and handle it
                    load_more_button = driver.find_element(By.CLASS_NAME, "d2l-load-more")
                    if load_more_button:
                        last_item = items[-1]
                        last_date = last_item.find_element(By.CSS_SELECTOR, "abbr.d2l-fuzzy").get_attribute("title")
                        if "December 14" in last_date:  # Replace "December 14" with the desired date format
                            load_more_button.click()
                            browser_trusted = True  # Mark the browser as trusted

                except TimeoutException:
                    print("Trust browser button not found or expired. Proceeding to the next step.")

        #If authentication is completed, proceed to dropdown button
        if authentication_completed:
            dropdown_button = wait.until(
                EC.element_to_be_clickable((By.ID, "d2l-uid-22"))
            )
            dropdown_button.click()

            # Scrape data from the dropdown
            items = driver.find_elements(By.CSS_SELECTOR, "ul.vui-list li.dl2-datalist-item")
            for item in items:
                try:
                    title = item.find_element(By.CSS_SELECTOR, "a.dl2-link").text
                    due_date = item.find_element(By.CSS_SELECTOR, "span.vui-emphasis").text
                    print(f"Title: {title}, Due Date: {due_date}")
                except NoSuchElementException:
                    print("Item not found.")
                    continue

            last_item = items[-1]
            try:
                fuzzy_date = last_item.find_element(
                    By.CSS_SELECTOR, "abbr.d2l-fuzzy").get_attribute("title")
                # Parse the date to ensure it's the same day
                last_date = datetime.strptime(fuzzy_date, "%B %d at %I:%M %p").date()
                today = datetime.now().date()

                if last_date != today:
                    print("Last item is not from today. Stopping load more.")
                    break
            except NoSuchElementException:
                print("No fuzzy date found in the last item. Stopping load more.")
                break

            # Check if "Load More" button exists and handle it
            load_more_button = driver.find_element(By.CLASS_NAME, "d2l-load-more")
            if load_more_button:
                last_item = items[-1]
                last_date = last_item.find_element(By.CSS_SELECTOR, "abbr.d2l-fuzzy").get_attribute("title")
                if "December 14" in last_date:  # Replace "December 14" with the desired date format
                    load_more_button.click()

        # If the code expired, check for the "Try Again" button to regenerate the code
        try:
            try_again_button = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "try-again-button"))
            )
            print("Code expired, generating a new one...")
            try_again_button.click()
            continue  # Retry the process after clicking "Try Again" to get a new code

        except TimeoutException:
            print("No 'Try Again' button found. Proceeding with next steps.")

    except Exception as e:
        print(f"An error occurred: {e}")
        break

# Clean up
driver.quit()
