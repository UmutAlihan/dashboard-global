import automagica as magic
import sys

def get_btcusd():
    # TODO:
    ## wrap with try-catches for robust execution
    browser = magic.activities.Chrome(); get_browser_foreground(browser)
    browser.browse_to("https://www.google.com")
    search_bar = browser.find_element_by_xpath("//*[@id='tsf']/div[2]/div[1]/div[1]/div/div[2]/input") #605, 413
    get_browser_foreground(browser)
    mouse.move(605, 413, duration=1) # move mouse to searchbar
    mouse.click()
    while(not (search_bar.is_displayed() and search_bar.is_enabled()) ):
        magic.wait(1)
    search_bar.send_keys("btcusd")
    search_button = browser.find_element_by_xpath("//*[@id='tsf']/div[2]/div[1]/div[2]/div[2]/div[2]/center/input[1]")
    while(not (search_button.is_displayed() and search_button.is_enabled()) ):
        magic.wait(1)
    search_button.click()
    value = browser.find_element_by_xpath("//*[@id='knowledge-currency__updatable-data-column']/div[1]/div[2]/span[1]")
    mouse.move(270,352, duration=1.2) # move movuse to bitcoin value
    BTCUSD = float(value.text.replace(".","").replace(",",".")) # convert "10.164,60" str to fload value
    magic.wait(2);browser.close()
    print(BTCUSD)
    return BTCUSD
    
get_btcusd()