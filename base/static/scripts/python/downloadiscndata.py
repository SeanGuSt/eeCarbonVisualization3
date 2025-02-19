from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

# Set up Chrome options
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration

# Create the WebDriver instance
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Set download behavior via Chrome DevTools Protocol
    download_path = '/Users/shreeranjitharaviprakash/PycharmProjects/Seleniumproject/'
    if not os.path.exists(download_path):
        os.makedirs(download_path)  # Create directory if it does not exist

    params = {
        'behavior': 'allow',
        'downloadPath': download_path
    }
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

    # Open the URL
    driver.get('https://portal.edirepository.org/nis/mapbrowse?scope=edi&identifier=1160&revision=1')

    # Wait for the download button to be clickable and click it
    wait = WebDriverWait(driver, 20)
    download_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@name="ISCN3_layer.csv"]')))
    download_button.click()
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    wait = WebDriverWait(driver, 20)
    download_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@name="ISCN3_profile.csv"]')))
    download_button.click()
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    wait = WebDriverWait(driver, 20)
    download_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@name="ISCN3_citation.csv"]')))
    download_button.click()
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    download_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@name="ISCN3_dataset.csv"]')))
    download_button.click()
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    # Wait for the download link to be clickable and click it
    download_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Download"]')))
    download_link.click()
    # Wait to ensure the download starts
    time.sleep(20)  # Adjust this as needed

finally:
    # Close the WebDriver
    driver.quit()