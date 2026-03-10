# Auto-Scaling Weather Monitor 

## Overview

Auto-Scaling Weather Monitor is a **cloud-native microservice project** that fetches real-time weather data, monitors API traffic, stores historical data, and sends alerts when weather conditions exceed thresholds.

The system also demonstrates **DevOps practices such as containerization, monitoring, and CI/CD automation**.

This project was built to simulate how modern backend systems are **monitored and deployed in production environments**.

---

## Features

###  Weather Monitoring

* Fetches real-time weather data using the OpenWeather API.
* Displays current temperature and weather conditions for a selected city.

### Alert System

* Sends automatic alerts to **Discord** when temperature crosses a defined threshold.
* Helps simulate real-world alerting systems used in production monitoring.

### System Monitoring

* Tracks API request counts using **Prometheus metrics**.
* Provides live monitoring of system activity.

###  Visualization

* **Grafana dashboards** visualize API traffic and system metrics.
* Helps observe system behavior under different loads.

###  Historical Weather Storage

* Weather data is stored in **SQLite**.
* Allows analysis of past weather trends.

### Containerized Application

* The entire application is packaged using **Docker** for easy deployment.

###  CI/CD Automation

* **GitHub Actions pipeline** automatically:

  * Builds a Docker image
  * Pushes the image to Docker Hub
  * Sends deployment notifications to Discord

---

## System Architecture

User Request
↓
FastAPI Weather Service
↓
Fetch Weather from OpenWeather API
↓
Store Data in SQLite Database
↓
Prometheus Collects Metrics
↓
Grafana Displays Monitoring Dashboard
↓
Discord Sends Alerts and Deployment Notifications

---

## Tech Stack

| Tool            | Purpose                        |
| --------------- | ------------------------------ |
| FastAPI         | Backend microservice framework |
| OpenWeather API | Weather data provider          |
| SQLite          | Store historical weather data  |
| Prometheus      | Collect system metrics         |
| Grafana         | Visualize monitoring data      |
| Docker          | Containerization               |
| GitHub Actions  | CI/CD pipeline                 |
| Discord Webhook | Alert notifications            |

---

## API Endpoints

### Get Current Weather

```
GET /weather
```

Returns:

* city
* temperature
* weather condition
* alert status

---

### Get Historical Weather Data

```
GET /history
```

Returns recent stored weather records.

---

### Prometheus Metrics

```
GET /metrics
```

Used by Prometheus to collect system metrics.

---

## Installation & Setup

### Clone Repository

```
git clone https://github.com/yourusername/Auto-scaling-weather.git
cd weather-monitor
```

### Install Dependencies

```
pip install -r requirements.txt
```

### Run the Application

```
python -m uvicorn app.main:app --reload
```

Application will run at:

```
http://localhost:8000
```

---

## Monitoring

Prometheus:

```
http://localhost:9090
```

Grafana:

```
http://localhost:3000
```

---

## CI/CD Pipeline

The GitHub Actions pipeline automatically runs when code is pushed.

Pipeline steps:

1. Build Docker image
2. Push image to Docker Hub
3. Send deployment notification to Discord

---

## Future Improvements

* Kubernetes auto-scaling deployment
* Advanced weather analytics
* Frontend dashboard for weather trends
* Multi-city monitoring

---

