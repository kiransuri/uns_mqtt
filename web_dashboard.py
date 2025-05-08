from flask import Flask, render_template
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "battery_plant_dashboard"

# Standardized MQTT Topic Structure
TOPIC_BASE = "battery_plant/1"
TOPICS = {
    'mixing': {
        'temperature': f"{TOPIC_BASE}/process/mixing/sensor/temperature",
        'humidity': f"{TOPIC_BASE}/process/mixing/sensor/humidity",
        'pressure': f"{TOPIC_BASE}/process/mixing/sensor/pressure",
        'viscosity': f"{TOPIC_BASE}/process/mixing/sensor/viscosity",
        'density': f"{TOPIC_BASE}/process/mixing/sensor/density"
    },
    'coating': {
        'thickness': f"{TOPIC_BASE}/process/coating/sensor/thickness",
        'speed': f"{TOPIC_BASE}/process/coating/sensor/speed",
        'temperature': f"{TOPIC_BASE}/process/coating/sensor/temperature",
        'humidity': f"{TOPIC_BASE}/process/coating/sensor/humidity",
        'web_tension': f"{TOPIC_BASE}/process/coating/sensor/web_tension"
    },
    'drying': {
        'temperature': f"{TOPIC_BASE}/process/drying/sensor/temperature",
        'humidity': f"{TOPIC_BASE}/process/drying/sensor/humidity",
        'air_flow': f"{TOPIC_BASE}/process/drying/sensor/air_flow",
        'drying_time': f"{TOPIC_BASE}/process/drying/sensor/drying_time"
    },
    'calendering': {
        'pressure': f"{TOPIC_BASE}/process/calendering/sensor/pressure",
        'temperature': f"{TOPIC_BASE}/process/calendering/sensor/temperature",
        'speed': f"{TOPIC_BASE}/process/calendering/sensor/speed",
        'thickness': f"{TOPIC_BASE}/process/calendering/sensor/thickness"
    },
    'slitting': {
        'speed': f"{TOPIC_BASE}/process/slitting/sensor/speed",
        'tension': f"{TOPIC_BASE}/process/slitting/sensor/tension",
        'width': f"{TOPIC_BASE}/process/slitting/sensor/width"
    },
    'environmental': {
        'temperature': f"{TOPIC_BASE}/process/environmental/sensor/temperature",
        'humidity': f"{TOPIC_BASE}/process/environmental/sensor/humidity",
        'pressure': f"{TOPIC_BASE}/process/environmental/sensor/pressure"
    },
    'quality': {
        'resistance': f"{TOPIC_BASE}/process/quality/sensor/resistance",
        'porosity': f"{TOPIC_BASE}/process/quality/sensor/porosity",
        'density': f"{TOPIC_BASE}/process/quality/sensor/density"
    },
    'energy': {
        'power': f"{TOPIC_BASE}/process/energy/sensor/power",
        'air_pressure': f"{TOPIC_BASE}/process/energy/sensor/air_pressure",
        'water_temperature': f"{TOPIC_BASE}/process/energy/sensor/water_temperature"
    }
}

# Store latest sensor data
sensor_data = {
    'mixing': {
        'temperature': None,
        'humidity': None,
        'pressure': None,
        'viscosity': None,
        'density': None
    },
    'coating': {
        'thickness': None,
        'speed': None,
        'temperature': None,
        'humidity': None,
        'web_tension': None
    },
    'drying': {
        'temperature': None,
        'humidity': None,
        'air_flow': None,
        'drying_time': None
    },
    'calendering': {
        'pressure': None,
        'temperature': None,
        'speed': None,
        'thickness': None
    },
    'slitting': {
        'speed': None,
        'tension': None,
        'width': None
    },
    'environmental': {
        'temperature': None,
        'humidity': None,
        'pressure': None
    },
    'quality': {
        'resistance': None,
        'porosity': None,
        'density': None
    },
    'energy': {
        'power': None,
        'air_pressure': None,
        'water_temperature': None
    }
}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker")
        # Subscribe to all topics
        for process, sensors in TOPICS.items():
            for sensor, topic in sensors.items():
                client.subscribe(topic)
                logger.info(f"Subscribed to {topic}")
    else:
        logger.error(f"Failed to connect to MQTT broker with code: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        topic_parts = msg.topic.split('/')
        
        # Extract process and sensor type from topic
        process = topic_parts[3]  # e.g., 'mixing', 'coating', etc.
        sensor_type = topic_parts[-1]  # e.g., 'temperature', 'humidity', etc.
        
        # Update sensor data
        sensor_data[process][sensor_type] = {
            'value': payload['value'],
            'unit': payload['unit'],
            'timestamp': payload['timestamp']
        }
        logger.debug(f"Updated {process} {sensor_type}: {payload}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

# Set up MQTT client
client = mqtt.Client(MQTT_CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message

@app.route('/')
def index():
    return render_template('index.html', sensor_data=sensor_data)

@app.route('/api/sensor-data')
def get_sensor_data():
    return sensor_data

def start_mqtt_client():
    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_start()
    except Exception as e:
        logger.error(f"Error connecting to MQTT broker: {e}")

if __name__ == '__main__':
    start_mqtt_client()
    app.run(debug=True, use_reloader=False, port=5001) 