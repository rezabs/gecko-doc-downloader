import config
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

def print_info(row_key, document_name, link2doc, date_of_document, doc_link):
    """Prints the value of row_key followed by the strings 
       "Document Name:", document_name, link2doc, and date_of_document 
       concatenated together. Then prints the string "Link:" 
       followed by the value of doc_link."""
    # Print the extracted information
    info = f"{row_key} Document Name: {document_name} - {link2doc} - {date_of_document}"
    link = f"Link: {doc_link}"
    print(info)
    print(link)
    print()
    return


# The function performs the following steps:
#   It opens the link_element by simulating a key press combination (Ctrl + click) 
#   using the ActionChains class from the selenium library.
#   It switches to the newly opened tab.
#   It waits for the page to load for 20 seconds.
#   It finds and clicks the download button on the page.
#   It waits for the download to complete for 20 seconds.
#   It closes the current tab.
#   It switches back to the original tab.
# If any exception occurs during this process, it prints an error message 
# and follows the same steps to close the tab and switch back to the original tab.
def download_document(driver, link_element):
    try:        
        # Open the link_element in a new tab
        action_chains = ActionChains(driver)
        action_chains.key_down(Keys.CONTROL).click(link_element).key_up(Keys.CONTROL).perform()
        ### another option
        # driver.execute_script("window.open(arguments[0], '_blank')", link_element.get_attribute("href"))


        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])
        
        # Wait for the page to load
        time.sleep(20)  # Adjust the sleep duration as needed
        
        # Initiate the download
        download_button = driver.find_element(By.XPATH, '//a[@title="Download"]')
        download_button.click()
        ### another option
        # driver.find_element(By.CSS_SELECTOR, 'a[title="Download"]').click()
        
        # Wait for the download to complete
        time.sleep(20)  # Adjust the sleep duration as needed

    except Exception as e:
        print(f"Error: {e}")

    # Close the current tab
    driver.close()
    # Switch back to the original tab
    driver.switch_to.window(driver.window_handles[0])
    return

def main() -> None:
    # Get the address from the config.ini file
    address, login_title, documents_tab = config.read_config()

    # Set up the Selenium webdriver
    #driver = config.load_chrome_driver()
    with config.load_chrome_driver() as driver:

        # Navigate to the webpage
        driver.get(f"{address}")

        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "title")))

        # Check if the user is logged in
        is_logged_in = False

        while not is_logged_in:
            # Get the page title
            page_title = driver.title
            
            # Check if the page title indicates that the user is signed in
            if f"{login_title}" not in page_title:
                is_logged_in = True
            else:
                # Wait for a certain interval before checking again
                time.sleep(1)

        # Wait for the "Documents" link to be visible
        # then
        # Find the Documents tab by its label
        documents_link = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'//a[contains(text(), "{documents_tab}")]')))

        # Click on the Documents tab
        documents_link.click()

        # Wait for the "View All" link to appear and then click on it
        try:
            view_all_link = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.LINK_TEXT, "View All")))

            # Execute JavaScript to click on the "View All" link
            driver.execute_script("arguments[0].click();", view_all_link)
        except TimeoutException:
            print("The 'View All' link did not appear within 1 minute.")

        # Wait until the "Hide" link is visible
        hide_link = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//a[text()='Hide']")))

        # Find the table rows that represent each item
        # Wait for the table rows to be visible
        item_rows = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//tr[@data-row-key-value]")))

        # print(len(item_rows))
        # print(item_rows[1].get_attribute('innerHTML'))
        # document_name = item_rows[1].find_element(By.XPATH, './/th[@data-label="Document Type"]')
        # print(document_name)
        # Loop through each item row and extract the desired information
        for item_row in item_rows[1:]:
            # Extract the Document Name
            document_name = lambda item_row: item_row.find_element(By.XPATH, './/th[@data-label="Document Type"]//lightning-base-formatted-text').text.strip()

            # Extract the Link2Doc
            link2doc = lambda item_row: item_row.find_element(By.XPATH, './/td[@data-label="Link"]//lightning-formatted-url/a').text.strip()

            # Find the <a> element
            link_element = item_row.find_element(By.XPATH, './/td[@data-label="Link"]//lightning-formatted-url/a')

            # Extract the DateOfDocument
            date_of_document = item_row.find_element(By.XPATH, './/td[@data-label="Date Uploaded"]//lightning-formatted-date-time').text.strip()

            # Print the extracted information
            print_info(item_row.get_attribute('data-row-key-value'), document_name, link2doc, date_of_document, link_element.get_attribute('href'))

            # Call download function
            download_document(driver,link_element)


        # Close the current browser window, but keep the WebDriver session alive
        driver.close()

        # Close the webdriver
        driver.quit()

if __name__ == "__main__":
    main()
