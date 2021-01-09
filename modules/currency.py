#import automagica as magic
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium

import mouse, sys, logging, time, socket, datetime, getpass



def open_browser(url):

    #logging.log(LOW_LEVEL, "defining vars for chrome")
    #PATH_TO_CHROME_PROFILE = r"C:\Users\TCUDIKEL\AppData\Local\Google\Chrome\User Data\Default"
    
    # WHOAMI
    USER = getpass.getuser()
    HOSTNAME = socket.gethostname()

    # LOGGING
    if HOSTNAME == 'TC17785555':
        DRIVER_PATH = rf"D:\Dev\dashboard-global\drivers\chromedriver.exe"
    else:
        DRIVER_PATH = "/actions/drivers/chromedriver"
    
    #logging.log(LOW_LEVEL, "getting chrome options")
    options = webdriver.ChromeOptions()
    #options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #options.add_argument('--log-level=3')
    #options.add_argument(f"user-data-dir={PATH_TO_CHROME_PROFILE}") 
    options.add_argument("--profile-directory=Default")
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-infobars')
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--disable-dev-shm-usage")

    #logging.log(LOW_LEVEL, "creating Chrome object")
    #driver = webdriver.Chrome(executable_path=PATH_TO_CHROME, chrome_options=options)
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options); time.sleep(1)

    #logging.log(LOW_LEVEL, "executing js to assign undefined to 'navigator.webdriver'")
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
    """
    })
    driver.get(url)
    return driver

def is_element_exist(driver, xpath):
    try:
        elements = False
        elements = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
    except Exception: return False
    if elements: return True

def get_element(driver, xpath_list):
    time.sleep(1)
    for xpath in xpath_list:
        #print(f"looking for xpath: {xpath}")
        if is_element_exist(driver, xpath): AVAILABLE_XPATH = xpath
    #else: raise Exception(f"failed to find available xpath on get_element_search_bar()")
    try:
        elem = driver.find_element(By.XPATH, AVAILABLE_XPATH)
    except Exception as e:
        raise Exception(f"Error on get_element(): {e}")
    return elem

def wrtite_on_elem_send_enter(search_bar, query):
    try:
        time.sleep(0.3)
        search_bar.click()
        search_bar.send_keys(query)
        search_bar.send_keys(Keys.RETURN)
    except Exception as e:
        raise Exception(f"Error on wrtite_on_elem_send_enter(): {e}")

def query_currency_price(pair):
    ### XPATH List for google search bar 
    GSB_XPATH_1 = "/html/body/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input"
    GSB_XPATH_2 = "//*[@id='tsf']/div[2]/div[1]/div[1]/div/div[2]/input"
    GSB_PRICE_XPATHS = [GSB_XPATH_1, GSB_XPATH_2]

    ### XPATH List for currency price widget
    CP_XPATH_1 = "/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div[1]/div[1]/div[2]/span[1]"
    CP_XPATH_2 = "/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div[1]/div[1]/div[2]/span[1]"
    CP_XPATH_3 = "//*[@id='knowledge-currency__updatable-data-column']/div[1]/div[2]/span[1]"
    CP_XPATH_4 = "html/body/div/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[2]/span[1]/span[1]"
    CURRENCY_PRICE_XPATHS = [CP_XPATH_1, CP_XPATH_2, CP_XPATH_3, CP_XPATH_4]

    driver = open_browser("https://www.google.com")
    search_bar = get_element(driver, GSB_PRICE_XPATHS)
    query = pair
    wrtite_on_elem_send_enter(search_bar, query)
    price = get_element(driver, CURRENCY_PRICE_XPATHS)
    CURRENCY = float(price.text.replace(".", "").replace(",","."))
    driver.quit(); driver = None
    return CURRENCY