# Teleolx

## Introduction

Welcome to Teleolx! I am proud to present my Telegram bot designed for a variety of use cases, from collectors hunting for rare items to scalpers aiming to buy out market goods, or simply handymen searching for specific spare parts.

## How It Works

Teleolx operates by periodically downloading JSON data from the OLX portal based on a specified search phrase—in this example, "xperia". The bot saves this data in a database and, if a new ad is unique, it sends a notification via Telegram.

## Configuration

To function correctly, Teleolx requires a configuration file for your Telegram bot and chat ID. This file must be named `teleolx.cred` and placed in the directory where `main.py` is located. The content of the file should be in JSON format:

```json
{
  "TOKEN": "your bot token here",
  "CHAT_ID": "your chat id here"
}
```

## Troubleshooting

If you encounter any issues while using the bot, such as difficulties in preparing a JSON request for a specific phrase, lack of a server to run the bot, or any other problems, please feel free to contact me via Telegram at [https://arcyfix.t.me/](https://arcyfix.t.me/).

Thank you for using Teleolx!
