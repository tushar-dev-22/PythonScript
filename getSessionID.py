from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

def get_evosessionid():
    # Path to your WebDriver (e.g., ChromeDriver)
    driver_path = "/home/developer/Desktop/chromedriver-linux64/chromedriver"  # Make sure this is the correct path to chromedriver
    
    # Initialize WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")  # Run in headless mode if you don't need to see the browser

    # Use Service to specify the path to ChromeDriver
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open Duelbits website (you'll log in manually)
        driver.get("https://a8r.evo-games.com/")
        print("Please log in manually in the browser...")

        time.sleep(60)  # Adjust sleep to allow enough time for manual login
        
        # Once logged in, get cookies
        cookies = driver.get_cookies()
        evosessionid = None

        print(f"All Cookies: {cookies}") 

        # Look for the EVOSESSIONID cookie
        for cookie in cookies:
            if cookie['name'] == 'EVOSESSIONID':
                print('here in the code')
                evosessionid = cookie['value']

                print(evosessionid,'--------------id')
                break

        if evosessionid:
            print(f"EVOSESSIONID: {evosessionid}")
        else:
            print("EVOSESSIONID not found.")
        
        return evosessionid

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()

# Run the function
evosessionid = get_evosessionid()
