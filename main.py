import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def check_tickets():
    url = "https://tickets.staatstheater.bayern/bso.webshop/webticket/seatmap?eventId=38326"   # input the event url from website of your theater
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Mask automation
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver_path = "C:\Program Files\chromedriver-win64\chromedriver.exe"  # Download chrome driver and here replace with the path where the chrome driver is saved in your pc

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        # go to the page of your event and copy + paste cookie name and value from the browser
        driver.add_cookie({"name": "",
                           "value": ""})
        driver.add_cookie({"name": "JSESSIONID", "value": ""})
        driver.refresh()
        time.sleep(5)  # Wait for the page to load completely
        # Find ticket categories
        ticket_categories = driver.find_elements(By.CLASS_NAME, "inh-SeatGroupDowndown-FullOptionLine")  # change to the css selector in your
        print(f"Found {len(ticket_categories)} ticket categories.")
        for category in ticket_categories:
            category_text = category.find_element(By.CLASS_NAME, "inh-SeatGroupDowndown-NameInOptionLine").text  # change to css the selector in your website
            try:
                category.find_element(By.TAG_NAME, "s")  # Check for the <s> tag, which defines an available ticket
            except:
                # If no <s> tag is found, assume tickets are available
                print(f"Tickets are available. Go to: {url}")
                send_notification(f"Tickets available. Go to: {url}")
                return

        print("Tickets are still sold out.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

def send_notification(message):
    telegram_token = ""  # Replace with your telegram bot's token
    chat_id = ""  # Replace with your chat ID
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Notification sent successfully via Telegram!")
        else:
            print(f"Failed to send Telegram notification: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"An error occurred while sending Telegram notification: {e}")

if __name__ == "__main__":
    while True:
        check_tickets()
        time.sleep(60)  # Check every minute
