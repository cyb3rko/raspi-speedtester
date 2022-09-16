import cronitor
import csv
import os
import re
import subprocess
import time

# =======================================

home_name = "YOUR_USER"
cronitor_api_key = "YOUR_API_KEY"

# =======================================

output = ""


def run_speedtest(iteration):
    try:
        println(f"Running speedtest {iteration}...")
        response = subprocess.run([f"/home/{home_name}/speedtester/speedtest-cli/speedtest", "--progress=no"], capture_output=True, text=True).stdout
        println(f"Speedtest finished. Response:\r\n{response}")

        ping = re.search("Latency:\s+(.*?)\s", response, re.MULTILINE)
        download = re.search("Download:\s+(.*?)\s", response, re.MULTILINE)
        upload = re.search("Upload:\s+(.*?)\s", response, re.MULTILINE)

        println("Data extracted:")
        ping = ping.group(1)
        println(f"Ping: {ping} ms")
        download = download.group(1)
        println(f"Download: {download} Mbps")
        upload = upload.group(1)
        println(f"Upload: {upload} Mbps")

        println("Saving data to csv...")
        csv_path=f"/home/{home_name}/speedtester/output/speedtest.csv"
        f = open(csv_path, 'a+')
        writer = csv.writer(f)
        if os.stat(csv_path).st_size == 0:
            println("Writing headers...")
            writer.writerow(["Date", "Time", "Ping (ms)", "Download (Mbps)", "Upload (Mbps)"])
        println("Writing entries...")
        writer.writerow([time.strftime('%Y-%m-%d'), time.strftime('%H:%M:%S'), ping, download, upload])
        return True
    except Exception as e:
        println(f"Error: {e}")
        return False


def println(line):
    global output
    output += f"{line}\r\n"


cronitor.api_key = cronitor_api_key
monitor = cronitor.Monitor("speedtester")
monitor.ping(state="run")

timestamp = time.strftime("%Y-%m-%d - %H:%M:%S")
print(f"\r\nJob {timestamp}")
iteration = 0
success = False
while success == False:
    iteration += 1
    if iteration <= 3:
        success = run_speedtest(iteration)
    else:
        break

if success == True:
    monitor.ping(state="complete")
    print("Speedtester successfully finished!")
else:
    monitor.ping(state="fail")
    println("Speedtester failed to run!")
    print(output)
