import asyncio
import json
import sqlite3
import requests
from telegram import Bot  # pip python-telegram-bot

# Ustawienia bota Telegram (z pliku teleolx.cred)
TOKEN = ""
CHAT_ID = ""

# Ustawienia pliku bazy danych SQLite
DATABASE_FILE = "olxads.db"

# Ustawienia częstotliwości wykonania... uruchom co 3 minuty
FREQUENCY = 3


def read_credentials():
    with open("teleolx.cred", "r") as f:
        data = json.load(f)
        global TOKEN, CHAT_ID
        TOKEN = data["TOKEN"]
        CHAT_ID = data["CHAT_ID"]


def create_table():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS olxads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT,
            price TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def log_error(error_message):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO errors (error_message)
        VALUES (?)
    """, (error_message,))
    conn.commit()
    conn.close()


def save_offer(title, url, price):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    # Sprawdzanie, czy wiersz jest unikalny przed zapisem
    c.execute("""
        SELECT *
        FROM olxads
        WHERE title = ? AND url = ? AND price = ?
    """, (title, url, price))
    if c.fetchone() is None:
        c.execute("""
            INSERT INTO olxads (title, url, price)
            VALUES (?, ?, ?)
        """, (title, url, price))
        conn.commit()

        conn.close()
        return True
    else:
        conn.close()
        return False


async def send_notification(title, link, price):
    try:
        bot = Bot(token=TOKEN)
        if title == "Błąd!":
            # Komunikat o błędzie
            message = f"{title}\n\n{price}"
        else:
            # Komunikat o nowym ogłoszeniu
            message = f"Znaleziono nowe ogłoszenie:\n\n{title}\nCena: {price}\n\nLink: {link}"
        await bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        message = f"Error sending notification: {str(e)}"
        log_error(message)


async def check_olx():
    url = ("https://www.olx.pl/api/v1/offers/?offset=0&limit=40&query=xperia&category_id=99"
           "&sort_by=created_at%3Adesc&last_seen_id=837650251&filter_refiners=spell_checker"
           "&sl=1851b370720x52bd11c2")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Sprawdzenie, czy nie ma błędów HTTP w odpowiedzi

        data = response.json()

        if "data" in data:
            for item in data["data"]:
                title = item["title"]
                link = item["url"]
                price = item['params'][0]['value']['label']

                # Zapisywanie tylko unikalnych ofert do bazy danych
                if save_offer(title, link, price):
                    # Wysyłanie powiadomienia do Telegram tylko dla unikalnych ofert
                    await send_notification(title, link, price)
    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching data from OLX: {str(e)}"
        log_error(error_message)
        # Dodaj wysyłanie powiadomienia na Telegram o wystąpieniu błędu
        await send_notification("Błąd!", "", error_message)


async def main():
    while True:
        await check_olx()
        await asyncio.sleep(FREQUENCY * 60)


if __name__ == "__main__":
    create_table()
    read_credentials()  # Odczytaj dane uwierzytelniające z pliku
    asyncio.run(main())
