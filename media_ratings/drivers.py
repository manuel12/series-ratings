from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService

import time
from timer import ParserTimer

def get_browser_options(browser):
    if(browser == "chrome"):
        options = webdriver.ChromeOptions()
    else:
        options = webdriver.FirefoxOptions()   
        options.binary_location = 'C:/Program Files/Mozilla Firefox/firefox.exe'
        
    options.page_load_strategy = 'eager'
    options.add_argument('--headless')
    options.add_argument("--log-level=3")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-extensions")
    return options
    
    
for i in range(1):
    chrome_options = get_browser_options("chrome")
    tic = time.perf_counter()
    ch_driver = webdriver.Chrome(
                executable_path="drivers/chromedriver.exe", 
                options=chrome_options) 

    ch_driver.get("https://www.imdb.com/title/tt4574334/?ref_=nv_sr_srsg_0")
    temp_page_source = ch_driver.page_source
    toc = time.perf_counter()
    ch_driver.quit()

    print(f"----------------------------------------------------------------Chrome time: {toc-tic}")


    ff_options = get_browser_options("ff")
    tic = time.perf_counter()
    ff_driver = webdriver.Firefox( 
                service=FirefoxService(executable_path="drivers/geckodriver.exe"),
                options=ff_options)


    ff_driver.get("https://www.imdb.com/title/tt4574334/?ref_=nv_sr_srsg_0")
    temp_page_source = ff_driver.page_source
    toc = time.perf_counter()
    ff_driver.quit()
    print(f"---------------------------------------------------------------FF time: {toc-tic}")
