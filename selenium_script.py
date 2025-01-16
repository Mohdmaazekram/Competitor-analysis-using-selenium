# Import necessary libraries
from selenium.webdriver.edge.service import Service as EdgeService  # Import Edge service for Edge driver (not used in this code)
from selenium.webdriver.common.keys import Keys  # For handling keyboard keys
from selenium.webdriver.common.by import By  # For locating elements on the page
from google.oauth2 import service_account  # For Google service account authentication
from selenium.webdriver.support.ui import WebDriverWait  # For waiting until elements are loaded
from selenium.webdriver.support import expected_conditions as EC  # For defining conditions to wait for
from selenium.webdriver.chrome.options import Options  # For setting options to customize Chrome browser (not used)
from selenium.webdriver.chrome.service import Service  # Import Chrome driver service
from google.cloud import bigquery  # For interacting with Google BigQuery
from selenium import webdriver  # For launching the Selenium WebDriver (in this case, Chrome)
from bs4 import BeautifulSoup  # For parsing HTML (not used)
from io import StringIO  # For handling string input/output (not used)
import pandas_gbq as pg  # For exporting data to Google BigQuery using pandas
import pandas as pd  # For data manipulation
import numpy as np  # For numerical operations (not used here)
import db_dtypes  # Custom library for handling database data types (not used here)
import requests  # For making HTTP requests (not used here)
import datetime  # For handling date and time (not used here)
import socket  # For obtaining the local machine’s hostname and IP address
import json  # For parsing JSON data
import time  # For adding delays in the script execution
import re  # For regular expressions (not used here)

# Define the Google Sheets ID for extracting URLs and other data
sheet_id = '1thUUyDMiVI7I4-nW-agMD5boOV8JD2BC4uc0h11kQuM'

# Read data from the Google Sheets URL using pandas
xls = pd.ExcelFile(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx")
Url_List = pd.read_excel(xls, 'URL Input Sheet ')  # Load the sheet containing the URLs

# Set the data frame for URLs to be scraped
url_df = Url_List
url_df['index'] = url_df.index  # Add a column for index
url_df['Rand_Num'] = url_df.index.to_series().apply(lambda x: f"?{1000 + x}")  # Add a random number for URL uniqueness
url_df['New_Url'] = url_df['Url'] + url_df['Rand_Num']  # Concatenate the base URL with the random number
url_lstt = url_df.values  # Convert the DataFrame to a NumPy array for iteration

data_df = pd.DataFrame()  # Initialize an empty DataFrame to store the scraped data
failed_urls = []  # Initialize an empty list to store URLs that failed scraping

# Initialize the WebDriver (Chrome in this case)
driver_path = r'C:\Users\Maaz Shaikh\chromedriver-win64\chromedriver.exe'  # Path to the ChromeDriver executable
service = Service(driver_path)  # Initialize the service for the ChromeDriver
driver = webdriver.Chrome(service=service)  # Start the Chrome browser

# Iterate through each URL and scrape the price based on the source
for i in url_lstt:
    Price = None  # Initialize the price as None for each URL

    # If the source is 'Tatacliq', scrape the price
    if i[2] == "Tatacliq":
        try:
            driver.get(i[5])  # Navigate to the URL
            time.sleep(2)  # Wait for the page to load
            text_field = driver.find_element(By.XPATH, '//*[@id="BPDT"]/div[1]/div[2]/div[1]/div[1]/h3')  # Find the price element by XPath
            Price = text_field.text  # Get the price text
        except:
            try:
                driver.get(i[5])  # Try loading the URL again
                time.sleep(2)
                text_field = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/div[2]') 
                Price = text_field.text
            except:
                failed_urls.append(i[1])  # If scraping fails, add the URL to the failed list

    # Similar scraping logic for other sources: Amazon, Flipkart, Ajio, Myntra

    elif i[2] == "Amazon":
        try:
            driver.get(i[5])
            time.sleep(2)
            text_field = driver.find_element(By.XPATH, '//span[text()=" Currently unavailable. "]')  # Check if the item is unavailable
            Price = text_field.text
        except:
            try:
                driver.get(i[5])
                time.sleep(2)
                text_field = driver.find_element(By.XPATH, '(//span[@class="a-price-whole"])[1]')  # Scrape the price
                Price = text_field.text
            except:
                failed_urls.append(i[1])  # Add failed URL to list

    # Scraping logic for Flipkart, Ajio, and Myntra (similar to above)
    # If any of these fail, they are added to the 'failed_urls' list

    else:
        print("Error: Unsupported source")  # Handle cases where the source is not recognized
        continue  # Skip to the next iteration if the source is unsupported

    # Store the scraped data into a dictionary
    dictt = {
        "Sr_No": i[3],  # Serial number
        "Brand": i[0],  # Brand name
        "Url": i[1],  # URL of the product
        "Price": Price,  # Scraped price
        "Source": i[2]  # Source (e.g., Amazon, Flipkart)
    }

    # Convert the dictionary to a DataFrame and append it to the main DataFrame
    df = pd.DataFrame(dictt, index=[0])
    data_df = pd.concat([data_df, df], axis=0)

# Close the WebDriver when done
driver.quit()

# Google Sheets credentials for authentication
# credentials_dict = {
#   "type": "service_account",
#   "project_id": "maazgsheet",
#   "private_key_id": "de41abe0f595f991ffe9f3dfa9b443a91c8a4e64",
#   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCtrGQjJM/zbRlU\nTMuSOK4K6X+K3Y2+NNJbYsF2+n1D5FEsC0Smwxja/5tyhiGT8tqp3B2jH2+YSOT2\nK0MerKvwVlCo/qyA0jTU+bBCnR1rX9Pz8j3qZtqeDz/+LfMKUeKDiOFmpCGoIQ/D\nei34HrMTHaB1d+PIBmQM9HRf7A9mbfiYHTpSBO/KkQQlmaXzuAc6OoXloNVPowft\n2DXsfNfQVzVF14alvocCRyRyljWSOWKgNcZkVlSonIMLpJYvP5IB4tEfnKXXHUxh\n+kaEXz1XsR2fT67Qn+eAAxmg9meqdj+oXswByv985BxjK3zQ7ffMfNuMQ9j35pzd\nPLUR5m3TAgMBAAECggEAJbE99HCnXzYE4spd/iimAUFHCIzoF+lf5CyNP3TC3gq9\n4Ti62BSMnu8Nvi/FNtZkxau7lO0cK6laY+DkytH/6QPasqq/JqA4jiZ4riRqP6UH\nG7Et5eMXvGkj4tb3Ify+k/yPqtahZVtzj+HC+1AyXko2SnhQK9fTPAqL/Ut+1iRZ\nSUefVb8lvFhZFo/L18nSg0DzfRxEkm0A3gAAqDCRoqmSv7f873YnHDogt2Mna9eO\n3eRF5iZvMDjvNXn/nowfRzW1C21m7T6IOleGYYnh4raqSOFp9eOMchLCMK3xeNCP\nfyuu/SR0SxmfQHPFuFpCHeX3eJDUCr7gQYPmBWRSDQKBgQDc43IHITLHKHByZGOu\nj2S+ha12RWXsflG4eeSHExcpCG2rgyr1YLH3dcTvK/kFZdkArYi3snFYvDfWYQFK\nsEz6yB80FOcMuEb62+DK0ExYL7MLGz7Dc/KbJO7nQEnxNG1DTtZMJHHghguQ0f7G\nyz9fmrTLE4ZMjxQCksjhr4C7nwKBgQDJR6LdWYrnSARN2TRpRm+gRBtVefzpJapq\nQu+Fxf/30G5Ez/h7W4ujFEsLSQvPR3SXThilgTY7T5bRt8OSwnkkCfzX/jzJXxnk\n1XfF0dIFdirjac2JStlxOShCn04/WrjTB8EZ/OjJAxF8WR5F8asO8empIiLE+iAF\n0Kwv33GhTQKBgC8eZYiX0FkjizkbqRfnhroNkf8UtrVIDO6pMdKOg/ZA0gQwKs3F\nHrGG8ceDPc+k9jFq0ys8aWlgXRjiAICKMyGb5uwZOWBBPwLsPHuHC4IUSsEnwq+2\n4B2wNzYlRKCralNdUeFUNOaMMZNm+E43tQET41UeiRtzufUCks9xvKhJAoGBAI/o\nuQg7wjV0Zydl2bQ/WQYkS8rEalAjzwEklG53z3hWPNDURRulq2PQ2YrbEieENlcL\nzlFe3fBwCiwtkBY5FzXuMioYK0vqw++5tGXqi5e+EhIAjqTPsEHklOV1UxO3AJhZ\nXfX/vkwh9nmKmjt1+1C3I9H6hxOApi6iMMoVnv+tAoGAb7JCjO51F4L7v+Wtbj4F\npzOzGUWJANTbP801dEPGlxK7uu1rojTpfwzrvJrwGbnjpJmih4lrLHxjxYK1rGV2\nzo9GdjLcKFdUnmoKYX2eDHDNCA/WFrBIinIaXF7osHTJrpfcUuufrPoPg57sSRyo\nVFOyPnRXkhoDfcJJMdLOd/g=\n-----END PRIVATE KEY-----\n",
#   "client_email": "maazgsheet@maazgsheet.iam.gserviceaccount.com",
#   "client_id": "111090250500905014979",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/maazgsheet%40maazgsheet.iam.gserviceaccount.com",
#   "universe_domain": "googleapis.com"
# }

# # Use the provided credentials to authenticate and access Google Sheets
# credentials = ServiceAccountCredentials.from_json_keyfile_dict(
#     credentials_dict,
#     ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# )
# gc = gspread.authorize(credentials)  # Authorize with Google Sheets API

# # Open the Google Sheet by key
# sheet = gc.open_by_key('1d8JO72rUfzAPxIo7swt0DuSrNWdeXyJZosssZWHSyJw')  # Use the sheet ID

# # Select the first worksheet
# worksheet = sheet.get_worksheet(0)

# # Convert the DataFrame into a list format for updating Google Sheets
# data_as_list = data_dff.values.tolist()

# # Update the Google Sheet with the DataFrame data
# worksheet.update([data_dff.columns.values.tolist()] + data_as_list)

# # print("Data successfully added to Google Sheets!")  # Confirmation message
