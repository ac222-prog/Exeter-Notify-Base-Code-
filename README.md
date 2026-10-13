# Exeter-Notify-Base-Code-
# Fixr Event Scraper & Email Notifier

A Python script that automatically monitors a [Fixr Organiser Page](https://fixr.co/organiser/timepiece) for new event drops and sends immediate email notifications when a new event is detected.

---

## Features

- **Automated Monitoring:** Periodically checks the venue page at custom intervals.
- **Duplicate Prevention:** Tracks seen events in a local `seen_events.json` file to ensure you only get notified about new events once.
- **Email Notifications:** Dispatches automated email alerts via SMTP when new events appear.
- **Browser Automation:** Uses Selenium with Safari WebDriver for dynamic page rendering.

---

## Prerequisites

- **Python 3.x** installed on your system.
- **macOS** with Safari installed.
- An email account with SMTP access (e.g., a Gmail account with an App Password).

---

## Setup & Installation

### 1. Install Required Python Libraries

Run the following command in your terminal:

```bash
pip install selenium