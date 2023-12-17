import configparser
from selenium import webdriver

def load_chrome_driver():
    """This sets up the Chrome Driver and returns it as an object"""
    chrome_options = webdriver.ChromeOptions() 
    
    # Keeps the browser open
    chrome_options.add_experimental_option("detach", True)
    
    #### OPTION
    # Browser is displayed in a custom window size
    # chrome_options.add_argument("window-size=1500,1000")
    
    # Removes the "This is being controlled by automation" alert / notification
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    
    return webdriver.Chrome(options=chrome_options)

def read_config():
    """This reads .ini file and returns address, login_title, documents_tab"""
    try:
        # As the goal is to call this function once at the beginning of the code, we can create the object here, 
        # and we don't check the existance of the file
        # Otherwise
        # Separate ConfigParser Creation: Instead of creating a new ConfigParser object every time the read_config() function is called, 
        # you can create the ConfigParser object outside the function and pass it as a parameter. 
        # This can improve performance if the function is called multiple times.
        config = configparser.ConfigParser()
        config.read('config.ini')
        address = config.get('Settings', 'address')
        login_title = config.get('Options', 'login_title')
        documents_tab = config.get('Options', 'documents_tab')
    except configparser.Error as e:
        print(f"Error reading config.ini file: {e}")
        # Handle the error, such as providing default values or exiting the program
        address = ''
        login_title = ''
        documents_tab = ''
        
    return address, login_title, documents_tab 
