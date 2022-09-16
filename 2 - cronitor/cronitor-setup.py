import cronitor

cronitor.api_key="YOUR_API_KEY"
cronitor.Monitor.put(
    key="speedtester",
    type="job",
    schedule="0 */4 * * *" # Or whatever interval you want
)
