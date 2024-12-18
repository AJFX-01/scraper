import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)

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

# Main loop to handle code retrieval and expiration
while True:
    try:
        # Wait for the verification code to appear
        code_element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "verification-code"))
        )
        code = code_element.text
        print(f"Verification code retrieved: {code}")

        # Send the code via Mailgun API
        send_email_via_mailgun(code)

        # Wait for the "Try Again" button to appear, indicating expiration
        try_again_button = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "try-again-button"))
        )
        try_again_button.click()
        print("Code expired, generating a new one...")

    except Exception as e:
        print(f"An error occurred: {e}")
        break

# Clean up
driver.quit()
