import os
import traceback
import time
import csv
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

def scraper():
    """ The main scrapping code """
    # Selenium Configuration
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 50)
    messages = {}

    # Login to the web app
    driver.get(os.getenv("TARGET_URL"))

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
                    try:
                        div_elements = wait.until(
                            EC.presence_of_all_elements_located((
                                By.CSS_SELECTOR, "div.d2l-navigation-s-notification"))
                        )
                    except TimeoutException:
                        print("Timeout waiting for div elements with shadow DOM")
                        continue
                    except NoSuchElementException:
                        print("No div elements with shadow DOM found")
                        continue

                    # Iterate through each div to find the specific button inside the shadow DOM
                    for div_element in div_elements:
                        try:
                            # Locate the d2l-navigation-dropdown-button-icon inside the div
                            d2l_button_element = div_element.find_element(
                                By.CSS_SELECTOR, "d2l-navigation-dropdown-button-icon")
                            shadow_root = get_shadow_root(driver, d2l_button_element)

                            # Try to locate the button with a unique ID (e.g., 'd2l-uid-191')
                            button_id = shadow_root.find_element(
                                By.CSS_SELECTOR, "button").get_attribute("aria-label")
                            print(f"Found button with id: {button_id}")

                            if button_id == "Update alerts":
                                button = shadow_root.find_element(By.ID,
                                            "button[aria-label='Update alerts']")
                                button.click()
                                print(f"Button {button_id} clicked successfully!")
                                dropdown_found = True
                                break

                        except Exception as inner_e:
                                    # Handle case where the button or shadow root is not found in this specific div
                            print(f"Error interacting with div: {inner_e}")
                            continue

                except Exception as e:
                    error_type = type(e).__name__
                    print(f"An error of type '{error_type}' occurred: {e}")

            # Scrape data from the dropdown
            try:

                try:
                    dropdown_content = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "d2l-dropdown-content"))
                    )
                    print(dropdown_content.get_attribute("innerHTML"))
                    print("Dropdown content found.")
                    div2_class = wait.until(
                        EC.presence_of_element_located((By.ID, "AB_DL_PH_Grades"))
                    )
                    print(div2_class.get_attribute("innerHTML"))
                    items = div2_class.find_element(
                        By.CLASS_NAME, "vui-list")
                    print(items.get_attribute("innerHTML"))
                    print("Items found.")

                    # Locate all <li> elements within the <ul>
                    li_tags = items.find_elements(By.CLASS_NAME, "d2l-datalist-item")

                    # Extract data for each item
                    for i, li_tag in enumerate(li_tags, start=1):
                        
                        try:
                            title = li_tag.find_element(By.CLASS_NAME, "d2l-link").text
                            due_date = li_tag.find_element(By.CLASS_NAME, "vui-emphasis").text
                            print(f"Title: {title}, Due Date: {due_date}")
                            messages[i] = {"title": title, "duedate": due_date}
                        except NoSuchElementException as e:
                            print(f"Error extracting item details: {e}")
                            continue
                    print(messages)
                    with open("messages.csv", mode="w", newline="", encoding="utf-8") as csv_file:
                        writer = csv.writer(csv_file)
                        writer.writerow(["No", "title", "duedate"])
                        for i,  details in messages.items():
                            writer.writerow([i, details["title"], details["duedate"]])
                        print("Data saved to messages.csv")
                    return messages
                except TimeoutException:
                    print("Dropdown content not found.")
                    break
                except NoSuchElementException:
                    print("No dropdown content found.")
                    break
            except Exception as e:
                error_type = type(e).__name__
                print(f"An error of type '{error_type}' occurred: {e}")
                
                # Optionally log the full stack trace
                print("\nStack Trace:")
                traceback.print_exc()
        except Exception as e:
            error_type = type(e).__name__
            print(f"An error of type '{error_type}' occurred: {e}")
            # Optionally log the full stack trace
            traceback.print_exc()
            break