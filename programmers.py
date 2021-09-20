from selenium import webdriver
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import time

URL = "https://programmers.co.kr/job?page=1&min_salary=&min_career=&min_employees=&order=recent&tags="
LINK = "https://programmers.co.kr"
PAUSE_TIME = 2

def get_jobs(tag):
    url = f"{URL}{tag}"
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(executable_path="chromedriver", options = options)
    driver.get(url=url)
    jobs = []
    while True:
        time.sleep(PAUSE_TIME)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        positions = soup.find_all("li",{"class":"list-position-item"})
        for position in positions:
            title = position.find("h5")
            if title:
                link = title.find("a")["href"]
                title = title.find("a").text.strip() 
                
            company = position.find("h6")
            if company:
                company = [text for text in company.stripped_strings]
                company = company[0]

            location = position.find("li",{"class":"location"})
            if location:
                location = location.text.strip()

            job = {
                "title" : title,
                "company" : company,
                "location" : location,
                "link" : f"{LINK}{link}"
            }
            jobs.append(job)
            

        pages = soup.find_all("li",{"class":"page-item"})
        next_page = pages[-1]
        if "disabled" in next_page["class"]:
            break
        
        pagination = driver.find_element_by_class_name("pagination")
        next = driver.find_element_by_css_selector(".pagination li:last-child")
        ActionChains(driver).move_to_element(pagination).click(next).perform()
    
    driver.close()
    return jobs

