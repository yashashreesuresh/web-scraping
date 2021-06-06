from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from shutil import which

chrome_options = Options()
chrome_options.add_argument("--headless")

path = which("./chromedriver")
print(path)

driver = webdriver.Chrome(executable_path=path, options=chrome_options)
driver.get("https://duckduckgo.com/")

search_input = driver.find_element_by_id("search_form_input_homepage")
search_input.send_keys("Hello World!")

# Search by clicking the search button
# search_btn = driver.find_element_by_id("search_button_homepage")
# search_btn.click()

# Search using pressing ENTER key
search_input.send_keys(Keys.ENTER)

print(driver.page_source)

driver.close()