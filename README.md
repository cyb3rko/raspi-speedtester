# Raspberry Pi Speedtester

Here's my step-by-step guide on how to setup a fully automatic speedtest on your Raspberry Pi with CSV logging and optional [Cronitor](https://cronitor.io/) implementation and Google Drive Upload.

- **Base Speedtester**
    - [Preparation](#preparation)
        - [OS Installation](#os-installation)
        - [Updating your machine](#updating-your-machine)
    - [Setup](#setup)
        - [Directory](#directory)
        - [Python](#python)
        - [Speedtest CLI](#speedtest-cli)
    - [First Run](#first-run)
    - [Cron](#cron)
    - [Logging](#logging)
- [Cronitor Implementation](2%20-%20cronitor/README.md)
- Google Drive Implementation (coming soon)

---

## Preparation

### OS Installation

First of all you need to install an OS on your Raspberry Pi. If already done, [skip this part](#updating-your-machine).

Recommendation (personal preference):  
Use the official [Raspberry Pi Imager tool](https://www.raspberrypi.com/software/) to flash an OS on your Pi.  
For this use case I recommend installing Raspberry Pi Os Lite, but it works with other versions as well.  
And check the settings section in the Imager, there you can preconfig things like hostname, ssh authentication, Wifi connection, system language and keyboard layout.

### Updating your machine

Now login to your Pi (by SSH or by direct connection with a monitor and a keyboard).

Before starting to work an a project it's always a good idea to update everything installed on your Pi:

`sudo apt-get update && sudo apt-get upgrade -y`

## Setup

### Directory

Now decide where you want your speedtester files saved. I just choose a new folder called `speedtester` in my home folder:

`mkdir speedtester`  
`cd speedtester/`

### Python

Check if Python is installed (should be installed by default):

`python --version`

If not, there's enough help on the internet on how to install Python :) .

To download the `speedtester.py` script, download it directly from GitHub into the new folder:

`wget https://raw.githubusercontent.com/cyb3rko/raspi-speedtester/main/1%20-%20base/speedtest.py`

### Speedtest CLI

Next, we need to download the Speedtest CLI to actually run a speedtest.  
Go to https://www.speedtest.net/de/apps/cli, scroll down to the Download section and find the right download under 'Linux' for your architecture (for me (Raspberry Pi 3B+) it's `aarch64`).

Copy the download link, go to your speedtester folder and type

`mkdir speedtest-cli`  
`cd speedtest-cli/`
`wget YOUR_DOWNLOAD_LINK`

For me it's `wget https://install.speedtest.net/app/cli/ookla-speedtest-1.2.0-linux-aarch64.tgz`.

As we download a compressed folder we need to unpack it (into a new folder):

`tar -xf YOUR_FILE_NAME`

For me it's `tar -xf ookla-speedtest-1.2.0-linux-aarch64.tgz`.

Run a speedtest to check if the installation was successfull and to accept licenses:

`./speedtest`

You can delete the tar.gz file now if you want to:

`rm YOUR_FILE_NAME`

## First Run

Go back to your speedtester folder and create the output directory, where the speedtest results will be saved:

`cd ..`
`mkdir output`

Before we run the script we have to specify where the speedtest-cli is saved, so do

`nano speedtest.py`

and search for `home_name = "YOUR_USER"`.
Replace it with your user name you are currently working with, for example `home_name = "niko"`.

Save it by pressing CTRL + O (or take a look at the commands at the bottom of the screen) and exit by pressing CTRL + X (or again see at the bottom for the correct command).

Now it's time to run the script the first time using

`python speedtest.py`.

If everything works fine you should see the job name and after a few seconds, that the speedtest has finished.  
Check the results:

`nano output/speedtest.csv`.

## Cron

The last thing we need to do now is to tell the Pi how and when to run this script.  
We do this via a service called Crontab.  
But before installing the job, we have to make the python file executable:

`chmod +x speedtest.py`

Then we can install the cron job:

`crontab -e`

Go to the end of the file and add

`0 */4 * * * /home/YOUR_USER/speedtester/speedtest.py >> /var/log/cron/speedtester.log 2>&1`

The cron expression at the start of the line can be changed to whatever you like to, currently it executes the script every 4 hours.

[Cron Generator / Examples](https://crontab.guru/examples.html)

## Logging

To log the output of the script we specify an output in the crontab (the `>> /var/log/cron/speedtester.log 2>&1` part).  
Furthermore we have to create the file and give write permissions:

`cd /var/log`  
`sudo mkdir cron`  
`cd cron`  
`sudo nano speedtester.log`  
Type for example `Speedtester Cron Log`.  
Save and exit the file [as described above](#first-run).  
`sudo chmod 666 speedtester.log`

The script should now execute via cron job and log it's output in the file `/var/log/cron/speedtester.log`.
