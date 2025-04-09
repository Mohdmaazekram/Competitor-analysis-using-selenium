**Project Details : Automated Web Scraping & ETL for Competitor Pricing Analysis**

In this project, I implemented an automated ETL **(Extract, Transform, Load) pipeline to streamline competitor pricing analysis using Python, Selenium, BigQuery, and Looker Studio.**

* **Extract :** I used Selenium with Python to scrape pricing and product data from multiple competitor websites. This automated data extraction replaced manual efforts and ensured real-time access to updated competitor information.

* **Transform :** After extraction, I performed data cleaning, formatting, and schema design within BigQuery to ensure consistency and usability. This step included handling missing values, normalizing data formats, and defining proper field types and table structures.

* **Load :** The cleaned and structured data was loaded into a BigQuery table, which I scheduled to automatically append new data daily through a scheduled job, ensuring continuous updates with minimal manual intervention.

Finally, I built a dynamic dashboard in **Looker Studio** connected to the **BigQuery** table. This dashboard provided real-time visualization and insights into **competitor pricing trends**, helping the business make informed pricing decisions and stay competitive in the market.

This project showcases how automation and data engineering practices can be combined to create an end-to-end solution for data-driven strategy and decision-making.

**Instructions for Setting Up a Python Script with Task Scheduler**


**1. Create a Folder:**

* First, create a new folder on your local disk where you will store your Python script. For example, create a folder named Mktplace_image_link_scraping on your Desktop.

**2. Upload Your Python Script:**

* Upload your Python script (for example, Schedule_test.py) into the folder you just created.

**3. Create a Batch File (if required):**

* If you need a batch file to run the script, create a .bat file in the same folder.
* In the batch file, make sure to include the following line:
arduino
"C:\Users\Maaz Shaikh\anaconda3\python.exe" "C:\Users\Maaz Shaikh\Desktop\Mktplace_image_link_scraping\Schedule_test.py" "C:\Users\Maaz Shaikh\json_service_key.json"

* This line specifies the Python interpreter (from Anaconda) to run your script and includes the path to any required arguments (e.g., a JSON file).

**4. Open Task Scheduler and Create a New Task:**

* Open **Task Scheduler** on your system.
* In the **Task Scheduler Library**, click on Create Task to set up a new task.

**5. Configure Task Settings:**

* In the **General** tab:
  
  * Give your task a name (e.g., Mktplace Image Scraping).
  * Check the option **Run whether the user is logged on or not.**
  * Check the option **Run with highest privileges** to ensure the task runs with administrative rights.

**6. Set Triggers:**

* Go to the **Triggers** tab.
* Click **New** to define when the task should run. Set the conditions based on your preference (e.g., daily, monthly, or specific time and date).
  
**7. Set the Action:**

* In the **Actions** tab, click **New** to create an action for running your script.
  
    * In the **Program/script** field:
      
        * Enter the path to your Python interpreter. To find the Python path, open **Command Prompt (CMD)** and type where python. This will show the installed Python path (e.g., C:\Users\YourUsername\anaconda3\python.exe).

    * In the **Add arguments** field:
      
        * Enter the path to your Python script (e.g., "C:\Users\Maaz Shaikh\Desktop\Mktplace_image_link_scraping\Schedule_test.py").

    * In the Start in field:
      
        * Enter the folder path where your Python script is located (e.g., C:\Users\Maaz Shaikh\Desktop\Mktplace_image_link_scraping).

**8. Set Conditions and Settings:**

* In the **Conditions** tab, leave the default settings unless you need specific changes.
* In the **Settings** tab, configure the settings as per your needs (e.g., allowing the task to run on a specific network connection or stopping it if it runs too long).

**9. Finalize the Task:**

* Click **OK** to save the task.
* You will be prompted to enter your password (if required) to complete the creation of the scheduled task.

**10. Test the Task:**

* After setting up the task, right-click on it in the Task Scheduler Library and click **Run** to test if the task executes correctly.
* Check if the Python script runs as expected and completes the required task.
