import paho.mqtt.client as mqtt
import json
import time
import pandas as pd
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "battery_plant_simulator"

# Standardized MQTT Topic Structure
# Format: battery_plant/{plant_id}/process/{process_id}/sensor/{sensor_type}
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

class BatteryPlantSimulator:
    def __init__(self):
        self.client = mqtt.Client(MQTT_CLIENT_ID)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.data = None
        self.current_index = 0
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT broker")
        else:
            logger.error(f"Failed to connect to MQTT broker with code: {rc}")

    def on_publish(self, client, userdata, mid):
        logger.debug(f"Message {mid} published successfully")

    def load_data(self, csv_file='battery_plant_data.csv'):
        try:
            self.data = pd.read_csv(csv_file)
            logger.info(f"Loaded {len(self.data)} records from {csv_file}")
        except Exception as e:
            logger.error(f"Error loading CSV file: {e}")
            raise

    def publish_sensor_data(self):
        if self.data is None:
            logger.error("No data loaded. Please load data first.")
            return

        if self.current_index >= len(self.data):
            logger.info("Reached end of data, restarting from beginning")
            self.current_index = 0

        row = self.data.iloc[self.current_index]
        
        # Publish mixing room data
        self.publish_sensor_value(TOPICS['mixing']['temperature'], row['mixing_temperature'])
        self.publish_sensor_value(TOPICS['mixing']['humidity'], row['mixing_humidity'])
        self.publish_sensor_value(TOPICS['mixing']['pressure'], row['mixing_pressure'])
        self.publish_sensor_value(TOPICS['mixing']['viscosity'], row['slurry_viscosity'])
        self.publish_sensor_value(TOPICS['mixing']['density'], row['slurry_density'])
        
        # Publish coating line data
        self.publish_sensor_value(TOPICS['coating']['thickness'], row['coating_thickness'])
        self.publish_sensor_value(TOPICS['coating']['speed'], row['coating_speed'])
        self.publish_sensor_value(TOPICS['coating']['temperature'], row['coating_temperature'])
        self.publish_sensor_value(TOPICS['coating']['humidity'], row['coating_humidity'])
        self.publish_sensor_value(TOPICS['coating']['web_tension'], row['web_tension'])
        
        # Publish drying oven data
        self.publish_sensor_value(TOPICS['drying']['temperature'], row['oven_temperature'])
        self.publish_sensor_value(TOPICS['drying']['humidity'], row['oven_humidity'])
        self.publish_sensor_value(TOPICS['drying']['air_flow'], row['air_flow_rate'])
        self.publish_sensor_value(TOPICS['drying']['drying_time'], row['drying_time'])
        
        # Publish calendering data
        self.publish_sensor_value(TOPICS['calendering']['pressure'], row['calender_pressure'])
        self.publish_sensor_value(TOPICS['calendering']['temperature'], row['calender_temperature'])
        self.publish_sensor_value(TOPICS['calendering']['speed'], row['calender_speed'])
        self.publish_sensor_value(TOPICS['calendering']['thickness'], row['electrode_thickness'])
        
        # Publish slitting data
        self.publish_sensor_value(TOPICS['slitting']['speed'], row['slitting_speed'])
        self.publish_sensor_value(TOPICS['slitting']['tension'], row['slitting_tension'])
        self.publish_sensor_value(TOPICS['slitting']['width'], row['electrode_width'])
        
        # Publish environmental data
        self.publish_sensor_value(TOPICS['environmental']['temperature'], row['room_temperature'])
        self.publish_sensor_value(TOPICS['environmental']['humidity'], row['room_humidity'])
        self.publish_sensor_value(TOPICS['environmental']['pressure'], row['room_pressure'])
        
        # Publish quality control data
        self.publish_sensor_value(TOPICS['quality']['resistance'], row['electrode_resistance'])
        self.publish_sensor_value(TOPICS['quality']['porosity'], row['electrode_porosity'])
        self.publish_sensor_value(TOPICS['quality']['density'], row['electrode_density'])
        
        # Publish energy monitoring data
        self.publish_sensor_value(TOPICS['energy']['power'], row['power_consumption'])
        self.publish_sensor_value(TOPICS['energy']['air_pressure'], row['compressed_air_pressure'])
        self.publish_sensor_value(TOPICS['energy']['water_temperature'], row['cooling_water_temperature'])

        self.current_index += 1

    def publish_sensor_value(self, topic, value):
        timestamp = datetime.now().isoformat()
        payload = {
                "timestamp": timestamp,
            "value": value,
            "unit": self.get_unit_for_topic(topic)
        }
        self.client.publish(topic, json.dumps(payload))
        logger.debug(f"Published to {topic}: {payload}")

    def get_unit_for_topic(self, topic):
        if 'temperature' in topic:
            return '°C'
        elif 'humidity' in topic:
            return '%'
        elif 'pressure' in topic:
            return 'hPa'
        elif 'viscosity' in topic:
            return 'cP'
        elif 'density' in topic:
            return 'g/cm³'
        elif 'thickness' in topic:
            return 'μm'
        elif 'speed' in topic:
            return 'm/min'
        elif 'tension' in topic:
            return 'N'
        elif 'air_flow' in topic:
            return 'm³/h'
        elif 'drying_time' in topic:
            return 'min'
        elif 'resistance' in topic:
            return 'Ω'
        elif 'porosity' in topic:
            return '%'
        elif 'width' in topic:
            return 'mm'
        elif 'power' in topic:
            return 'kW'
        elif 'air_pressure' in topic:
            return 'bar'
        return ''

    def run(self, interval=1):
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT)
            self.client.loop_start()
            
            logger.info("Starting battery plant sensor data publishing...")
            while True:
                self.publish_sensor_data()
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Stopping battery plant simulator...")
        except Exception as e:
            logger.error(f"Error in battery plant simulator: {e}")
        finally:
            self.client.loop_stop()
            self.client.disconnect()

if __name__ == "__main__":
    simulator = BatteryPlantSimulator()
    simulator.load_data()
    simulator.run() 