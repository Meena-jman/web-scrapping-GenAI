from selenium import webdriver 
from selenium.webdriver.common.by import By 
import time 


website_pages = [ 
            # "https://www.gsk.com", 
            # "https://www.tcs.com", 
            # "https://www.ford.com", 
            # "https://www.nespresso.com", 
            "https://www.siemens-energy.com", 
            "https://www.lenovo.com", 
            "https://www.theheinekencompany.com",
            "https://www.americanexpress.com",
            "https://www.panasonic.com"
            "https://www.starbucks.com"
            ] 
driver = webdriver.Chrome() 
def extract_links():
    navbar_links = driver.find_elements(By.CSS_SELECTOR, "nav a") 
    footer_links = driver.find_elements(By.CSS_SELECTOR, "footer a") 
    navbar_urls = [link.get_attribute("href") for link in navbar_links if link.get_attribute("href")] 
    footer_urls = [link.get_attribute("href") for link in footer_links if link.get_attribute("href")] 
    return set(navbar_urls + footer_urls) 

def extract_page_data(url):
    driver.get(url) 
    time.sleep(2) 
    try: 
        return driver.find_element(By.TAG_NAME, "body").text 
   
    except: 
        return "Could not extract data." 
for website in website_pages: 
    driver.get(website) 
    time.sleep(3) 
  
    all_urls = extract_links() 
    # domain_name = website.split("//")[-1].replace(".", "_") 
    # output_file = f"{domain_name}_scraped_data.txt"

    domain_name = website.split("//")[-1].split(".")[1] if "www." in website else website.split("//")[-1].split(".")[0]
    output_file = f"{domain_name}.txt"


    with open(output_file, "w", encoding="utf-8") as file: 
        for url in all_urls:
            page_content = extract_page_data(url) 
            file.write(f"Page: {url}\nContent:\n{page_content}\n" + "="*80 + "\n") 
            print(f"Scraped data saved to {output_file}") 
driver.quit()
