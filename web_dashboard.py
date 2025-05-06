from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
socketio = SocketIO(app)

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883

# Sensor topics
SENSOR_TOPICS = {
    "temperature": {
        "zone1": "factory/zone1/temperature",
        "zone2": "factory/zone2/temperature"
    },
    "pressure": {
        "zone1": "factory/zone1/pressure",
        "zone2": "factory/zone2/pressure"
    },
    "humidity": {
        "zone1": "factory/zone1/humidity",
        "zone2": "factory/zone2/humidity"
    },
    "vibration": {
        "machine1": "factory/machine1/vibration",
        "machine2": "factory/machine2/vibration"
    },
    "power": {
        "line1": "factory/power/line1",
        "line2": "factory/power/line2"
    }
}

# Store latest sensor data
sensor_data = {
    "temperature": {
        "zone1": {"value": 0, "unit": "°C", "timestamp": ""},
        "zone2": {"value": 0, "unit": "°C", "timestamp": ""}
    },
    "pressure": {
        "zone1": {"value": 0, "unit": "hPa", "timestamp": ""},
        "zone2": {"value": 0, "unit": "hPa", "timestamp": ""}
    },
    "humidity": {
        "zone1": {"value": 0, "unit": "%", "timestamp": ""},
        "zone2": {"value": 0, "unit": "%", "timestamp": ""}
    },
    "vibration": {
        "machine1": {"value": 0, "unit": "mm/s", "timestamp": ""},
        "machine2": {"value": 0, "unit": "mm/s", "timestamp": ""}
    },
    "power": {
        "line1": {"value": 0, "unit": "kW", "timestamp": ""},
        "line2": {"value": 0, "unit": "kW", "timestamp": ""}
    }
}

def on_connect(client, userdata, flags, rc):
    logger.info(f"Connected to MQTT broker with result code {rc}")
    # Subscribe to all sensor topics
    for sensor_type, locations in SENSOR_TOPICS.items():
        for location, topic in locations.items():
            client.subscribe(topic)
            logger.debug(f"Subscribed to topic: {topic}")

def on_message(client, userdata, msg):
    try:
        logger.debug(f"Received message on topic: {msg.topic}")
        data = json.loads(msg.payload.decode())
        sensor_type = data.get("sensor_type")
        location = data.get("location")
        
        if sensor_type and location:
            sensor_data[sensor_type][location] = {
                "value": data["value"],
                "unit": data["unit"],
                "timestamp": data["timestamp"]
            }
            logger.debug(f"Updated {sensor_type} {location}: {data['value']} {data['unit']}")
            
            # Emit the updated data to all connected web clients
            socketio.emit('sensor_update', sensor_data)
    except Exception as e:
        logger.error(f"Error processing message: {e}")

@app.route('/')
def index():
    logger.info("Rendering index page")
    return render_template('index.html', data=sensor_data)

@app.route('/test')
def test():
    return "Test route is working!"

def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        logger.info(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    except Exception as e:
        logger.error(f"Failed to connect to MQTT broker: {e}")
        raise
    
    client.loop_start()
    return client

if __name__ == '__main__':
    logger.info("Starting web dashboard...")
    mqtt_client = start_mqtt_client()
    socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0', port=5001) 