Selenium Automation Script Documentation

This document explains the steps and code for automating Looker Studio BigQuery data source management using Selenium.

1. Find Your Chrome User Data Folder

1. Close all Chrome windows.
2. Press Win + R → paste this and press Enter:
   %LOCALAPPDATA%\Google\Chrome\User Data

3. You’ll see folders like:
   - Default
   - Profile 1
   - Profile 2

'Default' = your main Chrome profile (if you’ve never created multiple profiles).
If you use multiple profiles, open Chrome → click profile picture → “Manage profiles” → hover over profile → click '...' to see folder name.

2. Selenium Script
Below is the complete script with inline comments explaining each step:

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configure Chrome to use your profile (change path & profile accordingly)
options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\SeleniumChromeProfiles")
options.add_argument(r"--profile-directory=Profile 2")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Launch the Chrome browser with WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 30)

# Replace with your list of Looker Studio report links
for item in Link:
    driver.get(item)

    # --- Login Section ---
    # Wait for email field, enter email & submit
    email_input = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
    email_input.send_keys("your_email_here")
    email_input.send_keys(Keys.ENTER)

    # Wait for password field, enter password & submit
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
    password_input.send_keys("your_password_here")
    password_input.send_keys(Keys.ENTER)
    
    # --- Open Edit Mode ---
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="reporting-app-header"]/div/div/product-tools-header/div/reporting-product-tools-header/edit-mode-toggle-button/button'))).click()
    
    # Open menu and select "Manage added data sources"
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="body"]/div[2]/div/menu-bar/mat-toolbar/button[7]'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Manage added data sources']"))).click()
    time.sleep(3)
    
    processed_datasources = set()
    
    while True:
        # Get list of datasource rows
        rows = driver.find_elements(By.CSS_SELECTOR, "div.ng2-manage-datasource-resource-table-row")
        if not rows:
            print("No datasource rows found, exiting loop.")
            break
    
        processed_any = False
    
        for i in range(len(rows)):
            try:
                rows = driver.find_elements(By.CSS_SELECTOR, "div.ng2-manage-datasource-resource-table-row")
                if i >= len(rows):
                    break
                row = rows[i]
    
                datasource_name = row.find_element(By.CSS_SELECTOR, "div.ng2-manage-datasource-first-col").text.strip()
    
                # Skip already processed datasources
                if datasource_name in processed_datasources:
                    continue
    
                # Check connector type (BigQuery only)
                connector_texts = row.find_elements(By.CSS_SELECTOR, "div.column.w10")
                connector_type = connector_texts[0].text.strip() if connector_texts else ""
    
                if connector_type != "BigQuery":
                    continue
    
                print(f"[{i}] BigQuery detected: {datasource_name}")
    
                # Click the edit button
                edit_button = row.find_element(By.CSS_SELECTOR, "button.edit-button")
                driver.execute_script("arguments[0].click();", edit_button)
                time.sleep(2)

                # Click the "Data credentials" button
                creds_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//datasource-credentials/div/button")))
                driver.execute_script("arguments[0].click();", creds_btn)
                time.sleep(5)

                # Click the back button
                back_btn = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="body"]/div[2]/shade/div/embedded-header/div/div[1]/div')
                ))
                driver.execute_script("arguments[0].click();", back_btn)
                time.sleep(2)
    
                # Mark this datasource as processed
                processed_datasources.add(datasource_name)
                processed_any = True
                break
    
            except Exception as e:
                print(f"Error processing row {i}: {e}")
                continue
    
        if not processed_any:
            print("No more BigQuery datasources found to process.")
            break

