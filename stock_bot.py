import os
import requests
from playwright.sync_api import sync_playwright

URL = "https://gold.razer.com/global/en/silver/redeem/summary/imo-usd5-gift-card%C2%A0-android-"
TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def notify(text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text},
        timeout=15,
    )


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(URL, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(5000)
    body = page.inner_text("body").upper()
    browser.close()

print(body[:1500])

if "ORDER TOTAL" not in body:
    print("Page not readable")
elif "OUT OF STOCK" in body:
    print("Out of stock")
else:
    notify("🔥 IMO USD5 Gift Card أصبح متاحًا الآن!\n" + URL)
    print("Notification sent")
