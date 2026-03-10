import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("weather_history.db")
cursor = conn.cursor()

cursor.execute("SELECT timestamp, temperature FROM weather")
rows = cursor.fetchall()

timestamps = [r[0] for r in rows]
temps = [r[1] for r in rows]

plt.plot(timestamps, temps)
plt.xticks(rotation=45)
plt.title("Temperature History")
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.show()