import requests
import sqlite3
from datetime import datetime

DB_PATH = "data/waste.db"

def fetch_ics(uprn: str):
    url = "https://www.east-ayrshire.gov.uk/WasteCalendarICSDownload"

    data = {
        "uprn": uprn,
        "captchaResponse": ""
    }

    response = requests.post(url, data=data)

    if "BEGIN:VCALENDAR" not in response.text:
        raise Exception("Failed to retrieve ICS")

    return response.text


def parse_ics(ics_text: str):
    events = []
    lines = ics_text.splitlines()

    current_event = {}

    for line in lines:
        line = line.strip()

        if line == "BEGIN:VEVENT":
            current_event = {}

        elif line.startswith("DTSTART"):
            date = line.split(":")[1]
            # Convert to readable date
            date = datetime.strptime(date, "%Y%m%d").date()
            current_event["date"] = str(date)

        elif line.startswith("SUMMARY"):
            current_event["type"] = line.split(":")[1]

        elif line == "END:VEVENT":
            if "date" in current_event and "type" in current_event:
                events.append((current_event["date"], current_event["type"]))

    return events


def store_events(events):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS collections (
        date TEXT,
        type TEXT
    )
    """)

    cur.execute("DELETE FROM collections")
    cur.executemany("INSERT INTO collections VALUES (?, ?)", events)

    conn.commit()
    conn.close()


def update_database(uprn: str):
    ics = fetch_ics(uprn)
    events = parse_ics(ics)
    store_events(events)
    return len(events)
