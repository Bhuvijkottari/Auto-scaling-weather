from fastapi import FastAPI
import requests
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response
from apscheduler.schedulers.background import BackgroundScheduler
import os
from datetime import datetime
import sqlite3

app = FastAPI()

# ----------------------------
# Prometheus Counter
# ----------------------------
REQUEST_COUNT = Counter('weather_requests_total', 'Total weather API requests')

# ----------------------------
# Environment Variables
# ----------------------------
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # fallback
CITY = os.getenv("CITY_NAME", "Mangalore")
print("API KEY:", API_KEY)
# ----------------------------
# SQLite DB for Historical Data
# ----------------------------
conn = sqlite3.connect("weather_history.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS weather (
    timestamp TEXT,
    city TEXT,
    temperature REAL,
    condition TEXT
)
""")
conn.commit()

def save_weather(temperature, condition):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO weather VALUES (?, ?, ?, ?)", (timestamp, CITY, temperature, condition))
    conn.commit()

# ----------------------------
# Discord Alert
# ----------------------------
def send_alert(message):
    if not WEBHOOK_URL:
        print("Discord webhook not set!")
        return
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
        print("Alert sent:", message)
    except Exception as e:
        print("Failed to send alert:", e)

# ----------------------------
# Weather Check Function
# ----------------------------
def check_weather_and_alert():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()
        print(response)  
        if response.get("cod") != 200:
          return {"error": "Failed to fetch weather", "details": response}


        temperature = response["main"]["temp"]
        condition = response["weather"][0]["description"]

        # Save to DB for historical graphs
        save_weather(temperature, condition)

        # Alert condition
        if temperature > 35:
            message = f"⚠ WEATHER ALERT\nCity: {CITY}\nTemp: {temperature}°C\nCondition: {condition}"
            send_alert(message)
        else:
            print(f"Weather normal: {temperature}°C, {condition}")

    except Exception as e:
        print("Error in check_weather_and_alert:", e)

# ----------------------------
# FastAPI Endpoints
# ----------------------------
@app.get("/")
def home():
    return {"message": "Weather Monitor Running"}

@app.get("/weather")
def get_weather():
    REQUEST_COUNT.inc()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        return {"error": "Failed to fetch weather"}

    temperature = response["main"]["temp"]
    condition = response["weather"][0]["description"]

    if temperature > 35:
        alert = "High Temperature Warning!"
        send_alert(f"⚠ WEATHER ALERT\nCity: {CITY}\nTemp: {temperature}°C\nCondition: {condition}")
    else:
        alert = "Normal Weather"

    # Save to DB for historical graphs
    save_weather(temperature, condition)

    return {
        "city": CITY,
        "temperature": temperature,
        "condition": condition,
        "alert": alert
    }
@app.get("/history")
def get_history():
    cursor.execute("SELECT * FROM weather ORDER BY timestamp DESC LIMIT 20")
    rows = cursor.fetchall()

    data = []
    for r in rows:
        data.append({
            "timestamp": r[0],
            "city": r[1],
            "temperature": r[2],
            "condition": r[3]
        })

    return data

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

# ----------------------------
# Scheduler for Automatic Checks
# ----------------------------
scheduler = BackgroundScheduler()
scheduler.add_job(check_weather_and_alert, 'interval', minutes=5)
scheduler.start()