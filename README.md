# Factory Sensor MQTT Simulator and Dashboard

This project simulates factory sensor data and provides a real-time web dashboard for monitoring. It uses MQTT for data transmission and Flask for the web interface.

## Features

- Simulates multiple factory sensors (temperature, pressure, humidity, vibration, power)
- Uses standardized MQTT topic structure
- Real-time data streaming from CSV file
- Web dashboard with live updates
- Comprehensive logging

## Prerequisites

- Python 3.8+
- MQTT Broker (e.g., Mosquitto)
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd uns_mqtt
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install and start MQTT broker (Mosquitto):
```bash
# On macOS with Homebrew:
brew install mosquitto
brew services start mosquitto

# On Ubuntu/Debian:
sudo apt-get install mosquitto
sudo systemctl start mosquitto
```

## Usage

1. Generate sensor data:
```bash
python generate_sensor_data.py
```

2. Start the sensor simulator:
```bash
python sensor_simulator.py
```

3. Start the web dashboard:
```bash
python web_dashboard.py
```

4. Access the dashboard at `http://localhost:5000`

## Project Structure

- `sensor_simulator.py`: MQTT publisher for sensor data
- `web_dashboard.py`: Flask web application for data visualization
- `generate_sensor_data.py`: Script to generate sample sensor data
- `templates/`: HTML templates for the web dashboard
- `requirements.txt`: Python package dependencies

## MQTT Topic Structure

The project uses a standardized MQTT topic structure:
```
factory/{factory_id}/zone/{zone_id}/sensor/{sensor_type}
```

Example: `factory/1/zone/1/sensor/temperature`

## License

MIT License 