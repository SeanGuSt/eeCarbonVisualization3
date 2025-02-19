from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
# Set Chrome options
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")

# Set the download path
download_path = 'Downloads'
if not os.path.exists(download_path):
    os.makedirs(download_path)

# Set download preferences
options.add_experimental_option("prefs", {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def refresh_page():
    driver.refresh()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='TableRow-focusBorder']"))
    )

try:
    # Navigate to the page
    driver.get('https://nrcs.app.box.com/s/s9bcdroihv1vyre70bkl336cdr13up7q')

    # Refresh the page once before searching for elements
    refresh_page()

    # Locate and click the element to open the dropdown
    target_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='TableRow-focusBorder']"))
    )
    target_element.click()

    # Wait for the dropdown to appear and locate the download option
    download_option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Download')]"))
    )
    download_option.click()

    # Wait for the download to start
    time.sleep(10)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()

#please make sure you have web_manager 4.0.2
#then try rm -rf ~/.wdm
