# Caratlane PLP Scraping.ipynb


import logging
from oauth2client.service_account import ServiceAccountCredentials
from glob import glob
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
import concurrent.futures
from io import StringIO
import pandas_gbq as pg
import smtplib
import pandas as pd
import numpy as np
import db_dtypes
import requests
import random
import socket
import json
import time
import re
import os
import io

# Logging setup
logging.basicConfig(filename='caratlane_scraping.log', level=logging.INFO)
logging.info("Caratlane scraping script started.")

sub = 'Caratlane Scraping'
username = 'maaz.ekram@candere.com'
password = 'rivi dvht delj kgrp'

# recipients
recipients = ['maaz.ekram@candere.com']

emaillist = [elem.strip().split(',') for elem in recipients]
msg = MIMEMultipart()
msg['Subject'] = sub
msg['From'] = 'maaz.ekram@candere.com'

sheet_id = '1BUd0V1lZg8Kpaw_dPGMNKB7UWVbialiV278jNBFWW7I'
xls = pd.ExcelFile(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx")
df = pd.read_excel(xls,'Sheet1')
# df = df.iloc[0:1]

# Function to classify product type
def product_type_class(x):
    try:
        if ((x == "JR") or (x == "UR") or (x == "SR") or (x == "JC")):
            return "Ring"
        elif (x == "UG") or (x == "JG"):
            return "Charm"
        elif (x == "JE") or (x == "UE")  or (x == "SE"):
            return "Earrings"
        elif (x == "JN") or (x == "SN") or (x == "UN"):
            return "Nose Pin"
        elif (x == "JP") or (x == "UP"):
            return "Pendant"
        elif (x == "UT") or (x == "JT") or (x == "SP") or (x == "ST"):
            return "Bracelet"
        elif (x == "UU") :
            return "Chain"
        elif (x == "JS") or (x == "SS") or (x == "US"):
            return "Mangalsutra"
        elif (x == "UL") or (x == "JL") or (x == "SL"):
            return "Necklace"
        elif (x == "JB") :
            return "Bangle"
        elif (x == "JM") :
            return "Tanmaniya"
        elif (x == "UD") :
            return "Charm Builder"
        elif (x == "MS") :
            return "Sets"
        elif (x == "UZ") :
            return "Baby Bangles"
        elif (x == "UH") :
            return "Nath"
        elif (x == "UC") :
            return "Adjustable Ring"
        else:
            return "Others"
    except Exception as e:
        logging.error(f"Error in product_type_class: {e}")
        return "Unknown"

Store_url_lst = []
Store_Name_lst = []
names_lst = []
price_lst = []
url_lst = []
sku_lst = []
abc_lst = []
iamge_lst = []

# Loop through Store Links and scrape data
for i in df['Store Links'].values:
    try:
        logging.info(f"Processing Store Link: {i}")
        Store_Url = i
        Store_Name = re.findall(r'https:\W+www.caratlane.com\Wstores\W(.*?)\Wcatalog\W', i)

        Store_url_lst.append(Store_Url)
        Store_Name_lst.append(Store_Name)

        urll2 = i + '?baseOffset=' if re.findall(r"", i) else i + '.?baseOffset='
        count_data = requests.get(urll2).text
        total_count = re.findall(r',"count":(\d*),"url":', str(count_data))[0]

        for items in range(0, int(total_count), 20):
            final_url = urll2 + str(items)
            data = requests.get(final_url).text
            Image = re.findall(r'itemProp="image" content=(.*?).jpg', str(data))
            namee = re.findall(r'class="css-x56fp3">([^<]*)', str(data))
            price = re.findall(r'"price" content="(\d+)', str(data))
            urlls = re.findall(r'Product"><link itemProp="url" href="([^"]*)', str(data))
            sku = re.findall(r'meta itemProp="sku" content="([^"]*)', str(data))
            abc = re.findall(r'href="www.caratlane.com\Wstores\W(.*?)\Wcatalog"', str(data)) * len(sku)

            names_lst.append(namee)
            price_lst.append(price)
            url_lst.append(urlls)
            sku_lst.append(sku)
            abc_lst.append(abc)
            iamge_lst.append(Image)

        logging.info(f"Scraped {len(names_lst)} products.")

    except Exception as e:
        logging.error(f"Error scraping data for {i}: {e}")

# Processing scraped data
try:
    sku_lstt_1 = []
    sku_lstt = [item for sublist in sku_lst for item in sublist]
    sku_lstt_1.append(sku_lstt)

    base_url = "https://cdn.caratlane.com/media/catalog/product"
    images_urlss = [f"{base_url}{path if path.endswith('.jpg') else f'{path}.jpg'}" for sublist in iamge_lst for path in sublist]

    names_lstt_1 = []
    names_lstt = [item for sublist in names_lst for item in sublist]
    names_lstt_1.append(names_lstt)

    price_lstt = [item for sublist in price_lst for item in sublist]
    price_lst1 = [price_lstt[i] for i in range(0, len(price_lstt), 2)]

    url_lstt_1 = []
    url_lstt = [item for sublist in url_lst for item in sublist]
    url_lstt_1.append(url_lstt)

    abc_lstt_1 = []
    abc_lstt = [item for sublist in abc_lst for item in sublist]
    abc_lstt_1.append(abc_lstt)


    data_dff = pd.DataFrame({
        "Name": names_lstt,
        "Price": price_lst1,
        "SKU": sku_lstt,
        "Product_Url": url_lstt,
        "Store_Url": abc_lstt,
        "Images_urlss": images_urlss
    })
    data_dff['Date'] = str(datetime.now())
    data_dff = data_dff[['Date'] + [col for col in data_dff.columns if col != 'Date']]
    data_dff = data_dff.astype("string")

    key_path = {

    }

    credentials = service_account.Credentials.from_service_account_info(
    key_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )


    client = bigquery.Client(
    credentials=credentials,
    project=credentials.project_id
    )

    pg.to_gbq(data_dff, 'github_scraping.Caratlane_Scraping_store_plp_data',project_id="daton-candere",if_exists = 'append',credentials = credentials)

    logging.info(f"Data processed successfully. Total products scraped: {len(data_dff)}")
    # print(data_dff)

except Exception as e:
    logging.error(f"Error processing data: {e}")

# Send the email with results
try:
    html = f"""
            <html>
            <h4> Scraping Successfully Completed <br></br>
            <br></br>
            Data & Time: {datetime.now()} <br></br>
            <br></br>
            Total Products Scraped:</b> {len(data_dff)} <br></br>
            </h4> <p></p> <br></br>
            </html>
            """
    part1 = MIMEText(html, 'html')
    msg.attach(part1)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('maaz.ekram@candere.com', 'rivi dvht delj kgrp')
    server.sendmail(msg['From'], emaillist, msg.as_string())
    server.close()

    logging.info("Email sent successfully.")

except Exception as e:
    logging.error(f"Error sending email: {e}")

logging.info("Caratlane scraping script finished.")
