import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.golfnow.com/")
time.sleep(6)

# STEP 1: Close popup from iframe 13
try:
    iframe = driver.find_elements(By.TAG_NAME, "iframe")[13]
    driver.switch_to.frame(iframe)
    print("Switched to popup iframe (13)")

    spans = driver.find_elements(By.TAG_NAME, "span")
    for span in spans:
        if span.is_displayed() and span.text.strip() == "✕":
            driver.execute_script("arguments[0].click();", span)
            print("Popup closed using span.")
            break
    driver.switch_to.default_content()
except Exception as e:
    print("Failed to close popup:", e)
    driver.switch_to.default_content()

# STEP 2: Search for Toronto and go to tee time page
try:
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "fed-search-big"))
    )
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
        print("Toronto option clicked — redirecting to tee time search page.")
        time.sleep(3)
        driver.get("https://www.golfnow.com/tee-times/destination/toronto/search")
    else:
        print("Could not find Toronto option.")
except Exception as e:
    print("Search failed:", e)

# STEP 3: Open the first "View Tee Times" in a new tab
try:
    time.sleep(5)
    first_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "View Tee Times"))
    )
    course_url = first_link.get_attribute("href")
    driver.execute_script(f"window.open('{course_url}', '_blank');")
    print("Opened tee times in new tab.")
except Exception as e:
    print("Failed to open tee time link:", e)

# STEP 4: Scrape tee time info from new tab
try:
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[-1])
    print("Switched to tee time tab.")
    time.sleep(3)

    tee_time_sections = driver.find_elements(By.CLASS_NAME, "select-rate-link")
    data = []

    for section in tee_time_sections:
        try:
            time_text = section.find_element(By.CLASS_NAME, "time-meridian").text
            price_text = section.find_element(By.CLASS_NAME, "price").text.replace("\n", "")
            rate_name = section.find_element(By.CLASS_NAME, "rateName").text
            data.append({
                "time": time_text.strip(),
                "price": price_text.strip(),
                "rate_name": rate_name.strip()
            })
        except Exception as e:
            print("Skipping bad section:", e)

    df = pd.DataFrame(data)
    df.to_csv("tee_times_data.csv", index=False)
    print("Saved to tee_times_data.csv")
except Exception as e:
    print("Scraping tee time data failed:", e)

driver.quit()
