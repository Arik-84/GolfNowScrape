import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.golfnow.com/")
time.sleep(6)

#Close popup
try:
    iframe = driver.find_elements(By.TAG_NAME, "iframe")[13]
    driver.switch_to.frame(iframe)
    spans = driver.find_elements(By.TAG_NAME, "span")
    for span in spans:
        if span.is_displayed() and span.text.strip() == "✕":
            driver.execute_script("arguments[0].click();", span)
            break
    driver.switch_to.default_content()
except:
    driver.switch_to.default_content()

#Search for Toronto
try:
    search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fed-search-big")))
    for char in "Toronto":
        search_input.send_keys(char)
        time.sleep(0.1)

    time.sleep(3)
    clicked = driver.execute_script("""
        const anchors = Array.from(document.querySelectorAll("a"));
        const target = anchors.find(a => a.dataset.expoption && a.dataset.expoption.includes("Toronto"));
        if (target) {
            target.scrollIntoView();
            target.click();
            return "clicked";
        } else {
            return null;
        }
    """)
    if clicked == "clicked":
        time.sleep(3)
        driver.get("https://www.golfnow.com/tee-times/destination/toronto/search")
except Exception as e:
    print("Search failed:", e)

#Scroll to bottom to load all courses
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

#Scrape all course tee times
all_data = []
visited = set()
view_links = driver.find_elements(By.PARTIAL_LINK_TEXT, "View Tee Times")

for i, link in enumerate(view_links):
    try:
        course_url = link.get_attribute("href")
        if course_url in visited:
            continue
        visited.add(course_url)

        driver.execute_script(f"window.open('{course_url}', '_blank');")
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "select-rate-link"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        try:
            course_name = soup.find("h1", itemprop="name").text.strip()
            addr = soup.find("address", itemprop="address")
            address_parts = [
                addr.find("span", {"itemprop": "streetAddress"}).text,
                addr.find("span", {"itemprop": "addressLocality"}).text,
                addr.find("span", {"itemprop": "addressRegion"}).text,
                addr.find("span", {"itemprop": "postalCode"}).text
            ]
            full_address = ", ".join(address_parts)
        except:
            course_name = "Unknown Course"
            full_address = "Unknown Address"

        tee_time_sections = driver.find_elements(By.CLASS_NAME, "select-rate-link")
        for section in tee_time_sections:
            try:
                time_text = section.find_element(By.CLASS_NAME, "time-meridian").text.strip()
                price_text = section.find_element(By.CLASS_NAME, "price").text.replace("\n", "").strip()
                rate_name = section.find_element(By.CLASS_NAME, "rateName").text.strip()
                digits = ''.join(filter(str.isdigit, price_text))
                price_clean = "${:.2f}".format(int(digits)/100) if digits else "N/A"

                all_data.append({
                    "course_name": course_name,
                    "address": full_address,
                    "time": time_text,
                    "price": price_clean,
                    "rate_name": rate_name
                })
            except:
                continue
    except Exception as e:
        print(f"Skipping course due to error: {e}")
    finally:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)

# Save to CSV
df = pd.DataFrame(all_data)
df.to_csv("all_toronto_tee_times_cleaned.csv", index=False)
print("Saved all course data to all_toronto_tee_times_cleaned.csv")
driver.quit()
