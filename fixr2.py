import json
import time
import smtplib
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ================= Configuration =================
URL = "https://fixr.co/organiser/timepiece"
SEEN_FILE = "seen_events.json"

RUNS = 120        # 120 minutes = 2 hours
INTERVAL = 60     # seconds

# Email settings
EMAIL_FROM = "" # REMOVED FROM PUBLIC
EMAIL_TO = "" # REMOVED FROM PUBLIC 
EMAIL_PASSWORD = ""  # Gmail app password REMOVED FROM PUBLIC 
SMTP_SERVER = "" # REMOVED FROM PUBLIC
SMTP_PORT = # REMOVED FROM PUBLIC
# =================================================

def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

# ---------- Email notification function ----------
def email_new_event(name, href):
    day = name.split()[0] if name else ""
    if "Timepiece" in name:
        short_name = f"{day} Timepiece"
    else:
        short_name = day

    msg = EmailMessage()
    msg['Subject'] = f"New Event: {short_name}"
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg.set_content(f"New event detected:\n\n{name}\nhttps://fixr.co{href}")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"📧 Email sent for: {short_name}")
    except Exception as e:
        print("⚠ Failed to send email:", e)

# ================= Main Loop =================
for i in range(RUNS):
    print(f"\n⏱ Run {i+1}/{RUNS}")

    # ---------- Selenium Scraping ----------
    driver = webdriver.Safari()
    driver.get(URL)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/event/']"))
    )

    time.sleep(3)

    links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/event/']")

    events = []
    for link in links:
        name = link.text.strip()
        href = link.get_attribute("href")
        if name and href:
            events.append((name, href.replace("https://fixr.co", "")))

    driver.quit()

    print("Events found on page:")
    for e in events:
        print(e)

    # ---------- Check for new events ----------
    seen = load_seen()

    for name, href in events:
        if href not in seen:
            print(f"🔔 New event found: {name}\n   https://fixr.co{href}")
            email_new_event(name, href)
            seen.add(href)

    save_seen(seen)
    print("Check complete.")

    if i < RUNS - 1:
        time.sleep(INTERVAL)