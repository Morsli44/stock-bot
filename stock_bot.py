import os
import time
import requests
from playwright.sync_api import sync_playwright

URL = "https://gold.razer.com/global/en/silver/redeem/summary/imo-usd5-gift-card%C2%A0-android-"
NAME = "IMO USD5 Gift Card"
TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

INTERVAL = 180   # ثانية (3 دقائق)
ROUNDS = 100     # 100 فحص = حوالي 5 ساعات


def notify(text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": text},
            timeout=15,
        )
    except Exception as e:
        print("Telegram error:", e)


def check(browser):
    page = browser.new_page()
    try:
        page.goto(URL, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(5000)
        body = page.inner_text("body").upper()
    finally:
        page.close()
    if "ORDER TOTAL" not in body:
        return None
    return "OUT OF STOCK" not in body


with sync_playwright() as p:
    browser = p.chromium.launch()
    for i in range(ROUNDS):
        start = time.time()
        try:
            state = check(browser)
        except Exception as e:
            print("Error:", e)
            state = None

        if state is True:
            notify(
                "🟩🟩🟩🟩🟩🟩🟩\n"
                "🟢 متاح الآن ✅🔥\n"
                "🟩🟩🟩🟩🟩🟩🟩\n\n"
                f"{NAME}\n{URL}"
            )
            print("available")
        elif state is False:
            notify(
                "🟥🟥🟥🟥🟥🟥🟥\n"
                "🔴 غير متاح حاليًا ❌\n"
                "🟥🟥🟥🟥🟥🟥🟥\n\n"
                f"{NAME}"
            )
            print("out of stock")
        else:
            notify("🟧🟧🟧\n🟠 تعذّر قراءة الصفحة ⚠️")
            print("not readable")

        if i < ROUNDS - 1:
            time.sleep(max(0, INTERVAL - (time.time() - start)))
    browser.close()
