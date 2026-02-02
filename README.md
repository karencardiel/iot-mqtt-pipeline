# IoT Data Ingestion Pipeline

> Real-time sensor data processing using MQTT protocol

## Overview

Complete IoT pipeline that simulates sensors, transmits data through CloudAMQP (MQTT broker), stores in PostgreSQL, and visualizes in real-time with Streamlit.

**Key Features:**
▸ Real-time processing with 2-second refresh  
▸ Cloud MQTT broker with encryption  
▸ Zero message loss  
▸ 150-300ms average latency  

## Architecture

```
Sensor Simulator → CloudAMQP → Subscriber → PostgreSQL → Dashboard
```

## Installation

```bash
# Clone repository
git clone https://github.com/karencardiel/iot-mqtt-pipeline
cd iot-mqtt-pipeline

# Install dependencies
pip3 install paho-mqtt psycopg2-binary streamlit pandas streamlit-autorefresh python-dotenv

# Create database
createdb iot_pipeline
psql iot_pipeline < schema.sql
```

## Configuration

Create `.env` file:

```env
MQTT_BROKER=your-instance.lmq.cloudamqp.com
MQTT_USER=your-username
MQTT_PASS=your-password
MQTT_PORT=8883

DB_HOST=localhost
DB_NAME=iot_pipeline
DB_USER=your_user
DB_PASSWORD=your_password
```

**Important:** Add `.env` to `.gitignore`

## Usage

Run in separate terminals:

```bash
# Terminal 1 - Subscriber
python3 subscriber.py

# Terminal 2 - Publisher
python3 publisher.py

# Terminal 3 - Dashboard
python3 -m streamlit run dashboard.py
```

Dashboard: `http://localhost:xxxx`

## Database Schema

```sql
CREATE TABLE lake_raw_data_int (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(255),
    payload TEXT,
    value INTEGER,
    ts TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE lake_raw_data_float (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(255),
    payload TEXT,
    value FLOAT,
    ts TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```

## Dashboard

<img width="1305" height="739" alt="image" src="https://github.com/user-attachments/assets/579dc146-1aac-43e1-a980-043891ecf37e" />

The Streamlit dashboard provides real-time visualization with:

**Components:**
▸ **KPI Metrics** - Most recent sensor values  
▸ **Time-Series Charts** - Area chart for integers, line chart for floats  
▸ **Raw Data Table** - Last N records (configurable 5-100)  
▸ **Auto-Refresh** - Updates every 2 seconds automatically 
