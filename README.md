# Gecko (salesforce) Document Download Automation
A python script that automates a web scraping task using Selenium WebDriver.

## Summary
It loads a web page, waits for specific elements to appear, checks if the user is logged in, interacts with the page to find and click on certain links, extracts information from table rows, and performs some actions on the extracted data. Finally, it closes the browser window and quits the WebDriver.
## Technologies
* **Python:** Used as the primary programming language for scripting and automation.
* **Selenium WebDriver:** Employed to automate web interactions, such as navigating to web pages, finding elements, clicking, and performing actions.
* **ConfigParser:** A Python module utilized for reading configuration data from the config.ini file.
* **ActionChains:** Part of Selenium WebDriver used for performing complex user interactions like keyboard shortcuts (e.g., Ctrl + click).
## Install Selenium
pip install selenium
## Description
The code is a Python script that uses the Selenium WebDriver library to automate web scraping tasks. It performs the following steps:

1. The main() function is defined. This is the entry point of the script.

2. The config.read_config() function is called to read configuration settings from a config.ini file. It returns the address of the web page to scrape, the title of the login page, and the label of the "Documents" tab.

3. The Selenium WebDriver is set up using config.load_chrome_driver(). This function returns a WebDriver instance that controls a Chrome browser. The with statement is used to ensure that the WebDriver is properly closed after the script finishes executing.

4. The WebDriver navigates to the web page specified in the configuration settings using the driver.get() method.

5. The script waits for the page to load by using the WebDriverWait class and presence_of_element_located() Expected Condition. It waits for the presence of a <title> element on the page.

6. The script checks if the user is logged in by checking the page title against the login page title from the configuration settings.

7. If the user is not logged in, the script waits until the user is logged in.

8. Once the user is logged in, the script waits for the "Documents" link to be visible on the page. And the script clicks on the "Documents" tab by calling the click() method on the documents_link element.

9. The script waits for the "View All" link to appear on the page using another WebDriverWait call.

10. If the "View All" link appears within 60 seconds, the script clicks on it using JavaScript execution (driver.execute_script()). If the link does not appear within the timeout period, a timeout exception is caught and a message is printed.

11. The script finds all the table rows that represent each item using presence_of_all_elements_located().

11. The script loops through each item row, starting from the second row (index 1, the first row is the header), and extracts information from each row.

12. Various pieces of information, such as the document name, link to the document, and date of upload, are extracted from each item row using XPath queries.

13. The download_document() custom function is called to download the document associated with each item row. This function takes the WebDriver instance and the link element as arguments and performs the necessary actions to download the document in a new tab.

14. After processing all the item rows, the script closes the current browser window using driver.close(), but keeps the WebDriver session alive.

15. Finally, the script quits the WebDriver using driver.quit().