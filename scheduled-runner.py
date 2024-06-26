import schedule
import time
import subprocess

def run_script():
    try:
        subprocess.run(["python", "scripttorun.py"], check=True)
        print("Script called successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Schedule the script to run every 30 minutes
schedule.every(30).minutes.do(run_script)

# Run indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)
