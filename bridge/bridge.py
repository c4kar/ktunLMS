import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class ChromeBridge:
    """
    A class to connect to and interact with an already running Chrome instance.
    """

    def __init__(self, port=5678):
        """
        Initializes the ChromeBridge and connects to the Chrome instance.

        Args:
            port (int): The remote debugging port Chrome was launched with.
        """
        print("--- Chrome Bridge ---")
        print("Connecting to Chrome instance on port {}...".format(port))
        
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            print("✅ Successfully connected to Chrome.")
            print(f"   - Current URL: {self.driver.current_url}")
            print(f"   - Current Title: {self.driver.title}")
        except Exception as e:
            print(f"❌ Connection Failed: Could not connect to Chrome on port {port}.")
            print("   Please ensure Chrome was started with the remote debugging flag.")
            print(f"   Example: chrome.exe --remote-debugging-port={port} --user-data-dir=\"C:\\ChromeDevSession\"")
            self.driver = None

    def is_connected(self):
        """Checks if the WebDriver is connected."""
        return self.driver is not None

    def find_element(self, by, value, timeout=10):
        """
        Finds and returns a web element.

        Args:
            by: The Selenium locator strategy (e.g., By.ID, By.CSS_SELECTOR).
            value: The value of the locator.
            timeout (int): Maximum time to wait for the element.

        Returns:
            WebElement or None if not found.
        """
        if not self.is_connected(): return None
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            print(f"❌ Element not found using ({by}, '{value}') within {timeout}s.")
            return None

    def get_text(self, by, value):
        """
        Retrieves the text content of an element.

        Args:
            by: The locator strategy.
            value: The locator value.

        Returns:
            The text of the element as a string, or None if not found.
        """
        element = self.find_element(by, value)
        if element:
            return element.text
        return None

    def set_text(self, by, value, text):
        """
        Clears an input field and types text into it.

        Args:
            by: The locator strategy.
            value: The locator value.
            text: The text to type into the element.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        element = self.find_element(by, value)
        if element:
            try:
                element.clear()
                element.send_keys(text)
                print(f"✅ Text set for element ({by}, '{value}').")
                return True
            except Exception as e:
                print(f"❌ Failed to set text for element ({by}, '{value}'): {e}")
                return False
        return False

    def click_element(self, by, value):
        """
        Clicks a web element.

        Args:
            by: The locator strategy.
            value: The locator value.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        element = self.find_element(by, value, timeout=5) # Use a shorter timeout for clicks
        if element:
            try:
                # Wait for the element to be clickable
                clickable_element = self.wait.until(
                    EC.element_to_be_clickable((by, value))
                )
                clickable_element.click()
                print(f"✅ Clicked element ({by}, '{value}').")
                return True
            except Exception as e:
                print(f"❌ Failed to click element ({by}, '{value}'): {e}")
                return False
        return False

    def close(self):
        """
        The 'close' method in this context doesn't close the browser,
        but detaches the driver from it.
        """
        if self.is_connected():
            self.driver.quit()
            print("ℹ️ WebDriver detached from Chrome. The browser remains open.")
            self.driver = None

def how_to_start_chrome():
    """Prints instructions on how to start Chrome for bridging."""
    print("\n--- How to use this script ---")
    print("1. Close all currently running Chrome instances.")
    print("2. Open a command prompt or terminal.")
    print("3. Run Chrome with the remote debugging flag. Choose a port (e.g., 9222).")
    print('   Example on Windows:')
    print('   "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir=\"C:\\ChromeDevSession\"')
    print("   Example on macOS:")
    print("   /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222 --user-data-dir=\"/tmp/ChromeDevSession\"")
    print("4. Manually navigate to the webpage you want to interact with.")
    print("5. Run this Python script.")


if __name__ == '__main__':
    # This is an example of how to use the ChromeBridge.
    how_to_start_chrome()
    
    print("\nAttempting to connect to Chrome in 5 seconds...")
    time.sleep(5)

    # Create a bridge to the Chrome instance running on port 9222
    bridge = ChromeBridge(port=9222)

    if bridge.is_connected():
        print("\n--- Interaction Example ---")
        
        # Example 1: Get text from the CAPTCHA image in otomasyon.py context
        # This assumes you have navigated to https://yemekhane.ktun.edu.tr/User/Login
        print("\nLooking for CAPTCHA image...")
        captcha_img = bridge.find_element(By.ID, "img_captcha")
        if captcha_img:
            print("✅ Found CAPTCHA image element.")
            # We can't get text from an image, but we can get attributes
            print(f"   - Image source: {captcha_img.get_attribute('src')}")
        
        # Example 2: Fill out the CAPTCHA code received from another source
        # This simulates the part of otomasyon.py where the user provides the code
        captcha_code_from_user = "1234" # Replace with the actual code
        print(f"\nAttempting to fill CAPTCHA with '{captcha_code_from_user}'...")
        if bridge.set_text(By.ID, "CAPTCHA", captcha_code_from_user):
             print("   -> Successfully filled the CAPTCHA input.")
        else:
             print("   -> Failed to fill CAPTCHA. Is the element ID 'CAPTCHA' correct and visible?")

        # The driver will detach, but the browser will remain open.
        bridge.close()
