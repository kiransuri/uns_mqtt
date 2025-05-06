import paho.mqtt.client as mqtt
import time
import random
import json
from datetime import datetime
import csv
import os

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

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def read_csv_data(file_path):
    """Read sensor data from CSV file."""
    data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def add_random_variation(value, variation_percent=1):
    """Add random variation to a value."""
    variation = float(value) * (variation_percent / 100)
    return float(value) + random.uniform(-variation, variation)

def simulate_sensor_data():
    # Create MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    
    # Connect to MQTT broker
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    
    # Read initial data from CSV
    csv_file = os.path.join(os.path.dirname(__file__), 'sensor_data.csv')
    sensor_data = read_csv_data(csv_file)
    data_index = 0
    
    try:
        while True:
            # Get current row of data
            current_data = sensor_data[data_index]
            
            # Add random variation to each value
            temp_zone1 = round(add_random_variation(current_data['temperature_zone1']), 2)
            temp_zone2 = round(add_random_variation(current_data['temperature_zone2']), 2)
            pressure_zone1 = round(add_random_variation(current_data['pressure_zone1']), 2)
            pressure_zone2 = round(add_random_variation(current_data['pressure_zone2']), 2)
            humidity_zone1 = round(add_random_variation(current_data['humidity_zone1']), 2)
            humidity_zone2 = round(add_random_variation(current_data['humidity_zone2']), 2)
            vibration_machine1 = round(add_random_variation(current_data['vibration_machine1']), 2)
            vibration_machine2 = round(add_random_variation(current_data['vibration_machine2']), 2)
            power_line1 = round(add_random_variation(current_data['power_line1']), 2)
            power_line2 = round(add_random_variation(current_data['power_line2']), 2)
            
            # Create and publish data for each sensor
            timestamp = datetime.now().isoformat()
            
            # Temperature data
            client.publish(SENSOR_TOPICS["temperature"]["zone1"], json.dumps({
                "value": temp_zone1,
                "unit": "°C",
                "timestamp": timestamp,
                "sensor_type": "temperature",
                "location": "zone1"
            }))
            
            client.publish(SENSOR_TOPICS["temperature"]["zone2"], json.dumps({
                "value": temp_zone2,
                "unit": "°C",
                "timestamp": timestamp,
                "sensor_type": "temperature",
                "location": "zone2"
            }))
            
            # Pressure data
            client.publish(SENSOR_TOPICS["pressure"]["zone1"], json.dumps({
                "value": pressure_zone1,
                "unit": "hPa",
                "timestamp": timestamp,
                "sensor_type": "pressure",
                "location": "zone1"
            }))
            
            client.publish(SENSOR_TOPICS["pressure"]["zone2"], json.dumps({
                "value": pressure_zone2,
                "unit": "hPa",
                "timestamp": timestamp,
                "sensor_type": "pressure",
                "location": "zone2"
            }))
            
            # Humidity data
            client.publish(SENSOR_TOPICS["humidity"]["zone1"], json.dumps({
                "value": humidity_zone1,
                "unit": "%",
                "timestamp": timestamp,
                "sensor_type": "humidity",
                "location": "zone1"
            }))
            
            client.publish(SENSOR_TOPICS["humidity"]["zone2"], json.dumps({
                "value": humidity_zone2,
                "unit": "%",
                "timestamp": timestamp,
                "sensor_type": "humidity",
                "location": "zone2"
            }))
            
            # Vibration data
            client.publish(SENSOR_TOPICS["vibration"]["machine1"], json.dumps({
                "value": vibration_machine1,
                "unit": "mm/s",
                "timestamp": timestamp,
                "sensor_type": "vibration",
                "location": "machine1"
            }))
            
            client.publish(SENSOR_TOPICS["vibration"]["machine2"], json.dumps({
                "value": vibration_machine2,
                "unit": "mm/s",
                "timestamp": timestamp,
                "sensor_type": "vibration",
                "location": "machine2"
            }))
            
            # Power data
            client.publish(SENSOR_TOPICS["power"]["line1"], json.dumps({
                "value": power_line1,
                "unit": "kW",
                "timestamp": timestamp,
                "sensor_type": "power",
                "location": "line1"
            }))
            
            client.publish(SENSOR_TOPICS["power"]["line2"], json.dumps({
                "value": power_line2,
                "unit": "kW",
                "timestamp": timestamp,
                "sensor_type": "power",
                "location": "line2"
            }))
            
            print(f"Published sensor data at {timestamp}")
            
            # Move to next row, loop back to start if at end
            data_index = (data_index + 1) % len(sensor_data)
            time.sleep(2)  # Publish every 2 seconds
            
    except KeyboardInterrupt:
        print("Stopping sensor simulator...")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    simulate_sensor_data() 