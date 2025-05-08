# Battery Manufacturing Plant Monitoring System

A real-time monitoring system for battery manufacturing plants using MQTT for data transmission and a web-based dashboard for visualization.

## Features

- Real-time sensor data simulation for battery manufacturing processes
- MQTT-based data transmission
- Modern web dashboard with real-time updates
- Comprehensive monitoring of multiple manufacturing processes:
  - Mixing Process
  - Coating Process
  - Drying Process
  - Calendering Process
  - Quality Control
  - Energy Monitoring

## Prerequisites

- Python 3.8 or higher
- MQTT Broker (Mosquitto)
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kiransuri/uns_mqtt.git
cd uns_mqtt
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Install and start Mosquitto MQTT broker:
```bash
# For macOS (using Homebrew)
brew install mosquitto
brew services start mosquitto
```

## Usage

1. Generate sensor data:
```bash
python generate_sensor_data.py
```
This will create a `battery_plant_data.csv` file with simulated sensor data.

2. Start the sensor simulator:
```bash
python sensor_simulator.py
```
This will start publishing sensor data to the MQTT broker.

3. Start the web dashboard:
```bash
python web_dashboard.py
```
The dashboard will be available at `http://localhost:5001`

## Project Structure

```
uns_mqtt/
├── generate_sensor_data.py    # Generates realistic sensor data
├── sensor_simulator.py        # MQTT publisher for sensor data
├── web_dashboard.py          # Flask web server and MQTT subscriber
├── requirements.txt          # Python dependencies
├── battery_plant_data.csv    # Generated sensor data
└── templates/
    └── index.html           # Web dashboard template
```

## MQTT Topic Structure

The system uses a standardized MQTT topic structure:
```
battery_plant/{plant_id}/process/{process_id}/sensor/{sensor_type}
```

Example topics:
- `battery_plant/1/process/mixing/sensor/temperature`
- `battery_plant/1/process/coating/sensor/thickness`
- `battery_plant/1/process/drying/sensor/humidity`

## Sensor Data

The system simulates various sensor readings including:
- Temperature (°C)
- Humidity (%)
- Pressure (hPa)
- Viscosity (cP)
- Density (g/cm³)
- Thickness (μm)
- Speed (m/min)
- Web Tension (N)
- Air Flow (m³/h)
- Power (kW)
- And more...

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- MQTT Protocol
- Flask Web Framework
- Bootstrap for the dashboard UI 