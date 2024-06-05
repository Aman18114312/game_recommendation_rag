import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector

def scroll_page(driver, scroll_pause_time=2):
    num_games = 0
    
    while num_games < 100:
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        selector = Selector(driver.page_source)
        num_games = len(selector.css('.itIJzb'))

    print("Scrolling completed.")

def scrape_game_details(url):
    try:
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
        selector = Selector(driver.page_source)
        driver.quit()
        description = selector.css('.bARER::text, .W4P4ne::text').get()  # Adjust the selector as per the actual HTML structure
        if not description:
            description = "No description available"
        print(f"Scraped description for {url}")
        return description
    except Exception as e:
        print(f"Failed to scrape description for {url}: {e}")
        return "Failed to fetch description"

def scrape_google_play_games():
    params = {
        'device': 'phone',  
        'hl': 'en_GB',        # language 
        'gl': 'US',            # country of the search
    }

    URL = f"https://play.google.com/store/games?device={params['device']}&hl={params['hl']}&gl={params['gl']}"

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--lang=en")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(URL)

    scroll_page(driver)
    
    selector = Selector(driver.page_source)

    games_data = []

    for result in selector.css('.itIJzb'):
        title = result.css('.OnEJge::text').get()
        link = 'https://play.google.com' + result.css('::attr(href)').get()
        category = result.css('.ubGTjb .sT93pb.w2kbF:not(.K4Wkre)::text').get()
        rating_text = result.css('.CKzsaf .w2kbF::text').get()
        rating = float(rating_text) if rating_text else None
        thumbnail = result.css('.stzEZd::attr(srcset)').get().replace(' 2x', '')

        # Scrape game details including description
        description = scrape_game_details(link)

        games_data.append({
            'Title': title,
            'Link': link,
            'Category': category,
            'Rating': rating,
            'Thumbnail': thumbnail,
            'Description': description
        })

        if len(games_data) >= 100:
            break  # Stop scraping after 100 games

    driver.quit()

    # Save extracted data to a CSV file
    with open('google_play_games1.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Link', 'Category', 'Rating', 'Thumbnail', 'Description'])
        writer.writeheader()
        writer.writerows(games_data)

    print("Extraction and CSV creation completed.")

if __name__ == "__main__":
    scrape_google_play_games()
