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

# Selenium Configuration
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 50)

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