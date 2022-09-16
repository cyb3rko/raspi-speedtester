# Cronitor Implementation

This is the guide on how to implement Cronitor into your speedtester.

- Base Speedtester
- **Cronitor Implementation**
    - [Setup](#setup)
    - [Update Speedtester](#update-speedtester)
    - [Update Cron](#update-cron)
- Google Drive Implementation

---

## Setup

If you don't have a Cronitor account, create one on [cronitor.io](https://cronitor.io).

To make calls to Cronitor, we then need your API key:
- Go to 'Settings'
- Go to 'API'
- Copy your key (if there are multiple, copy the one that can 'Configure Monitors')

Go to your local speedtester folder and download the `cronitor-setup.py` file:

`wget https://raw.githubusercontent.com/cyb3rko/raspi-speedtester/main/2%20-%20cronitor/cronitor-setup.py`

Open it via `nano cronitor-setup.py`, fill in your user name, your API key and save/exit the file.

By executing the file with `python cronitor-setup.py` a new monitor should appear on [cronitor.io](https://cronitor.io).

## Update Speedtester

To make Cronitor calls on every speedtest you need to download the slightly modified speedtest file `speedtest-cronitor.py`:

`wget https://raw.githubusercontent.com/cyb3rko/raspi-speedtester/main/2%20-%20cronitor/speedtest-cronitor.py`

Make the file executable:

`chmod +x speedtest-cronitor.py`

## Update Cron

The last step is to update your cron job:

`crontab -e`

Change `/home/YOUR_USER/speedtester/speedtest.py` to `/home/YOUR_USER/speedtester/speedtest-cronitor.py`