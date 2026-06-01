import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import os

# =====================================
# CONFIG
# =====================================

NOTICE_URL = "https://egov.uok.edu.in/results/results.aspx?rtype=3&rs=2"

# CHANGE THIS LATER TO 1ST SEM
TARGET_TEXT = "b. tech 1st semester regular batch 2025 and backlog batches held in dec 25 - jan 26"

COLLEGE_CODE = "sme"

BOT_TOKEN = os.environ["BOT_TOKEN2"]
CHAT_ID = os.environ["CHAT_ID2"]

# =====================================
# TELEGRAM
# =====================================

def send_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN2}/sendMessage"

    data = {
        "chat_id": CHAT_ID2,
        "text": message
    }

    response = requests.post(url, data=data)

    print(response.text)


def send_pdf(file_path):

    url = f"https://api.telegram.org/bot{BOT_TOKEN2}/sendDocument"

    with open(file_path, "rb") as f:

        files = {
            "document": f
        }

        data = {
            "chat_id": CHAT_ID2
        }

        response = requests.post(
            url,
            data=data,
            files=files
        )

        print(response.text)

# =====================================
# FIND NOTIFICATION
# =====================================

def notification_exists():

    print("Checking notification page...")

    response = requests.get(
        NOTICE_URL,
        timeout=30
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    page_text = soup.get_text("\n").lower()

    if TARGET_TEXT.lower() in page_text:

        print("Notification found")
        return True

    print("Notification not found")
    return False

# =====================================
# PLAYWRIGHT AUTOMATION
# =====================================

def download_pdf():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        context = browser.new_context(
            accept_downloads=True
        )

        page = context.new_page()

        print("Opening notification page...")

        page.goto(
            NOTICE_URL,
            timeout=120000,
            wait_until="domcontentloaded"
        )

        page.wait_for_timeout(10000)

        print("Searching notification row...")

        row = page.locator(
            f"text={TARGET_TEXT}"
        ).first

        row.wait_for(timeout=30000)

        print("Notification row found")

        print("Finding matching View button...")

        view_button = row.locator(
             "xpath=ancestor::tr//a[contains(text(),'View')]"
          )

        print("Clicking correct View button...")

        view_button.click()


        page.wait_for_load_state("networkidle")

        page.wait_for_timeout(5000)

        print("Selecting college...")

        page.wait_for_selector(
            "#cphMain_ddlColleges",
            timeout=30000
        )

        page.select_option(
            "#cphMain_ddlColleges",
            value=COLLEGE_CODE
        )

        page.wait_for_timeout(3000)

        print("Clicking College View button...")

        page.click("#cphMain_btnColleges")

        page.wait_for_load_state("networkidle")

        page.wait_for_timeout(5000)

        print("Clicking Print Result...")

        with page.expect_download(
            timeout=60000
        ) as download_info:

            page.click(
                "#cphMain_btnPrintResults"
            )

        download = download_info.value

        pdf_name = "result.pdf"

        download.save_as(pdf_name)

        print("PDF downloaded successfully")

        browser.close()

        return pdf_name

# =====================================
# MAIN
# =====================================

def main():

    send_message(
        "Starting result automation..."
    )

    if not notification_exists():

          send_message(
              "Result notification not found"
          )

        return

    send_message(
        "Result notification found"
    )

    try:

        pdf_file = download_pdf()

    except Exception as e:

        print(e)

        send_message(
            f"Automation failed:\n{e}"
        )

        return

    send_message(
        "Sending PDF..."
    )

    send_pdf(pdf_file)

    send_message(
        "Result PDF sent successfully"
    )

# =====================================

if __name__ == "__main__":
    main()
