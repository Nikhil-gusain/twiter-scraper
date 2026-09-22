# Twitter Scraper

A Python web-automation project built with Selenium to experiment with collecting and processing Twitter/X data.

## What it does

The project automates browser interaction, collects page data, processes the extracted content, and stores structured results.

## Workflow

```
Browser automation
      ↓
Open target pages
      ↓
Collect page elements
      ↓
Process response
      ↓
Convert data to JSON
```

## Project structure

- `tweetscraper.py` - main scraping workflow
- `Elements.py` - page element definitions
- `reqmaker.py` - request/data handling helpers
- `T2json.py` - data conversion
- `Responsemessages.py` - response messages
- `test.py` - testing/experimentation
- `jsondata/` - generated data

## Tech

- Python
- Selenium
- Web automation
- JSON

## Status

This is a learning project focused on browser automation and data extraction. Websites can change their structure, so selectors and workflows may require updates.

## Why I built it

I wanted to understand how browser automation can turn repetitive web interaction and data collection into a programmable workflow.
