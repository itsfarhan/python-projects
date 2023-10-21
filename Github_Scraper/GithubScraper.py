from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Get the target URL and search text from the user
target_url = input("Enter URL to scrape: ")
search_text = input("Enter text to search for: ")

chromedriver_path = "/home/th3uns33n/Downloads/chromedriver_linux64/chromedriver"
driver = webdriver.Chrome()
driver.get(target_url)

# Wait for the page to load (you might need to customize the waiting time)
driver.implicitly_wait(10)

# Get the page source after waiting for the JavaScript to load
page_source = driver.page_source

# Parse the page source using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find repositories using BeautifulSoup
repositories = soup.find_all(class_='repo')

for repo in repositories:
    repo_name = repo.text.strip()
    print("Repository:", repo_name)
    
    # Navigate to the repository page using Selenium
    repo_link = driver.find_element(By.LINK_TEXT, repo_name)
    repo_link.click()
    
    # Get the page source of the repository page
    repo_page_source = driver.page_source
    
    # Parse the repository page using BeautifulSoup
    repo_soup = BeautifulSoup(repo_page_source, 'html.parser')
    
    # Find specific file links in the repository page using BeautifulSoup
    file_links = repo_soup.find_all(class_='js-navigation-open')
    
    for file_link in file_links:
        file_name = file_link.text.strip()
        file_url = f"{target_url}/{repo_name}/blob/main/{file_name}"
        # Check if the search text is in the file content
        if search_text in file_url:
            print("File Link:", file_url)

# Close the WebDriver
driver.quit()