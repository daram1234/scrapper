
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver import ActionChains

URL = "https://www.wanted.co.kr/search?query="
LINK = "https://www.wanted.co.kr"
PAUSE_TIME = 2

def get_jobs(query):
    url = f"{URL}{query}"
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(executable_path="chromedriver", options = options)
    driver.get(url=url)
    jobs = []

    last_height = driver.execute_script("return document.body.scrollHeight")         
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(PAUSE_TIME)                                                
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:       
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source,"html.parser")
    job_cards = soup.find_all("div",{"class":"_3D4OeuZHyGXN7wwibRM5BJ"})

    for job_card in job_cards:
        title = job_card.find("div",{"class":"job-card-position"})
        if title:
            title = title.text.strip()
        
        link = job_card.find("a")["href"]

        company = job_card.find("div",{"class":"job-card-company-name"})
        if company:
            company = company.text.strip()
        
        location = job_card.find("div",{"class":"job-card-company-location"})
        if location:
            l = [text for text in location.stripped_strings]
            location = f"{l[0]} {l[-1]}"

        job = {
            "title" : title,
            "company" : company,
            "location" : location,
            "link" : f"{LINK}{link}"
        }

        jobs.append(job)

    driver.close()
    return jobs

