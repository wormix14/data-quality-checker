# Data Quality Checker Bot

Telegram bot built with `aiogram` and **Great Expectations** (`validator.py`) to validate data quality across **Bronze**, **Silver**, and **Gold** Medallion architecture layers as part of a Data Engineering project.

## Data Sources

- **Live Mode (Microsoft Fabric):** Set `BRONZE_TAXI_PATH`, `SILVER_TAXI_PATH`, and `GOLD_TAXI_PATH` (`abfss://...`) in `.env` and authenticate via Azure CLI (`az login`) to validate live Delta tables from OneLake.
- **Local Mode:** Leave the `_TAXI_PATH` variables empty in `.env` — the bot automatically falls back to reading cached `.parquet` samples stored in `data/`.

## Setup & Run
**Clone the repository and install dependencies:**
```bash
git clone <https://github.com/wormix14/data-quality-checker.git>
cd data-quality-checker
python -m venv venv
venv\Scripts\activate (On windows)
pip install -r requirements.txt
```
**Create .env**
```bash
cp .env.example .env
```
**Set telegram-bot token inside .env**
```bash
BOT_TOKEN=
```
**Run the bot**
```bash
python bot.py
```
**Start the bot in telegram**
```bash
/start
```
**Commands availble to validate each layer**
```bash
/bronze 
/silver
/gold
```
