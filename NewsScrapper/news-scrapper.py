from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import os, sys
import pandas as pd

application_path = os.path.dirname(sys.executable)

now = datetime.now()
month_day_year = now.strftime("%d%m%Y")


url = "your_url"
chromeDriverPath = "/path/of/chromedriver"

options = Options()
options.headless = True

driver = webdriver.Chrome(options=options)
driver.get(url)

containers = driver.find_elements(by="xpath", value='//div[@class="teaser__copy-container"]')

titles = []
subtitles = []
links = []

for container in containers:
    title = container.find_element(by="xpath", value='./a/h2').text
    subtitle = container.find_element(by="xpath", value='./a/p').text    
    link = container.find_element(by="xpath", value='./a').get_attribute("href")
    titles.append(title)
    subtitles.append(subtitle)
    links.append(link)
    
my_dict = {'title': titles, 'subtitle': subtitles, 'link': links}

df_headlines = pd.DataFrame(my_dict)
file_name =f'headline-{month_day_year}.csv'
final_path = os.path.join(application_path, file_name)
df_headlines.to_csv(final_path)

driver.quit()
