from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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
        # Step 1: Open Duelbits login page
        driver.get("https://duelbits.com/en")  # Replace with the actual Duelbits login URL
        print("Logging in to Duelbits...")

        login_button_1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]"))  # Replace with the correct selector
        )
        login_button_1.click()
        print("Login modal is now open.")

        

        # Step 2: Locate the username, password fields and login button
        username_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.NAME, "email"))  # Replace with the correct element
        )
        password_field = WebDriverWait(driver,20).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        )  # Replace with the correct element
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]"))  # Replace with the correct selector
        )  # Replace with the correct element

        # time.sleep(10)

        # Step 3: Enter login credentials and submit the form
        username_field.send_keys("jayhanda@gmail.com")  # Replace with your username

        time.sleep(10)
        password_field.send_keys("Jay$@Handa/22")  # Replace with your password


        time.sleep(50)
        # # Step 4: Handle potential overlapping elements
        try:
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element((By.CLASS_NAME, "styles_dsButton__a1yGJ styles_dsColor-ghost__C11QU ds-btn-md styles_ds-btn-md__2iCTh styles_HeaderGhostColor__2ybal styles_HeaderBtnHeight__1w3c8 styles_HeaderLoggedOutBtn__GE_Wo"))
            )
            print("Overlapping element is gone.")
        except Exception as e:
            print("No overlapping element found or error occurred:", e)


        # Step 6: Click the login button using JavaScript if normal click fails
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
            time.sleep(1)  # Small delay before clicking
            driver.execute_script("arguments[0].click();", login_button)
            print("Login button inside modal clicked.")
        except Exception as e:
            print("Failed to click login button:", e)

        # # Step 5: Remove 'disabled' attribute from login button (if present)
        # driver.execute_script("arguments[0].removeAttribute('disabled')", login_button)
        # print("Removed 'disabled' attribute from the login button.")

        # Step 6: Click the login button using JavaScript
        # driver.execute_script("arguments[0].click();", login_button)
        # print("Login button inside modal clicked.")
        # Step 4: Wait for login to complete (use a reasonable wait)
        # time.sleep(30)  # Adjust the sleep if needed or replace with an explicit wait

        # Step 5: Now navigate to a8r.evo-games.com after login
        driver.execute_script("window.open('https://a8r.evo-games.com/', '_blank');")
        print("Opened https://a8r.evo-games.com/ in a new tab.")

        # Step 7: Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])
        print("Switched to the new tab.")

        # Step 6: Wait a bit for cookies to be set (if needed)
        time.sleep(5)  # Adjust as needed

        # Step 7: Get cookies and extract the EVOSESSIONID
        cookies = driver.get_cookies()
        evosessionid = None

        print(f"All Cookies: {cookies}")

        # Step 8: Look for the EVOSESSIONID cookie
        for cookie in cookies:
            if cookie['name'] == 'EVOSESSIONID':
                evosessionid = cookie['value']
                print(f"EVOSESSIONID: {evosessionid}")
                break

        if not evosessionid:
            print("EVOSESSIONID not found.")

        return evosessionid

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Step 9: Close the browser
        driver.quit()

# Run the function
evosessionid = get_evosessionid()