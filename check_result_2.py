import time

while True:
    try:
        response = requests.get(URL, timeout=20)

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, "html.parser")
            page_text = soup.get_text().lower()

            for keyword in KEYWORDS:
                if keyword.lower() in page_text:

                    message = (
                        "1st Semester Result Notification Found\n\n"
                        f"Matched:\n{keyword}"
                    )

                    send_telegram_message(message)

                    break

            print("Checked successfully")

        else:
            print(f"Website error: {response.status_code}")

    except Exception as e:
        print(e)

    time.sleep(1800)
