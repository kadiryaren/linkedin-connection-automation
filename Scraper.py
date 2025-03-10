import psutil
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import pickle
import os
import random

def monitor_resources(process):
    try:
        # Get process information
        memory_info = process.memory_info()
        cpu_percent = process.cpu_percent(interval=1)
        gpu_percent = "N/A"  # GPU monitoring is not directly supported by psutil
        disk_usage = psutil.disk_usage('/').percent

        print(f"Memory Usage: {memory_info.rss / (1024 * 1024):.2f} MB")
        print(f"CPU Usage: {cpu_percent}%")
        print(f"GPU Usage: {gpu_percent}")
        print(f"Disk Usage: {disk_usage}%")
    except psutil.NoSuchProcess:
        print("Process not found")

# Path to the directory containing the extension
extension_path = os.path.abspath("chrome_extension")

options = Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--load-extension=" + extension_path)

driver = webdriver.Chrome(options=options)

if __name__ == "__main__":
    driver.get("https://www.twitch.tv/burobir")
    
    # Get the process ID of the Chrome driver
    process = psutil.Process(driver.service.process.pid)
    
    # Monitor resources every 5 seconds
    try:
        while True:
            monitor_resources(process)
            time.sleep(5)
    except KeyboardInterrupt:
        print("Monitoring stopped.")

    # Save cookies if needed
    # pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))  
    driver.close()