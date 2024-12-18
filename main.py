""" SCRAp successfully """

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv()

# Read variables from .env
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

def send_email(otp_code):
    
    """Send email"""

    # Create the email content
    subject = "Your Verification Code"
    body = f"The verification code is: {otp_code}"
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
    print(f"Verification code sent to {TO_EMAIL}")

# Selenium Configuration
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)

# Login to the web app
driver.get("https://learn.uwaterloo.ca/")

# Login Interactions
driver.find_element(By.ID, "userNameInput").send_keys("your_username")
driver.find_element(By.ID, "passwordInput").send_keys("your_password")
driver.find_element(By.ID, "submitButton").click()

# Main loop to handle code retrieval and expiration
while True:
    try:
        # Wait for the verification code to appear
        code_element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "verification-code"))
        )
        code = code_element.text
        print(f"Verification code retrieved: {code}")

        # Send the code via email
        send_email(code)

        # Wait for the code to expire (e.g., 60 seconds)
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "try-again-button"))
        ).click()
        print("Code expired, generating a new one...")

    except Exception as e:
        print(f"An error occurred: {e}")
        break

# Clean up
driver.quit()