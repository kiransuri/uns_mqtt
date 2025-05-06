import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sensor_data(num_records=1000):
    # Generate timestamps
    start_time = datetime(2024, 5, 5, 12, 0, 0)
    timestamps = [start_time + timedelta(minutes=i) for i in range(num_records)]
    
    # Initialize data dictionary
    data = {
        'timestamp': timestamps,
        'temperature_zone1': [],
        'temperature_zone2': [],
        'pressure_zone1': [],
        'pressure_zone2': [],
        'humidity_zone1': [],
        'humidity_zone2': [],
        'vibration_machine1': [],
        'vibration_machine2': [],
        'power_line1': [],
        'power_line2': []
    }
    
    # Generate base values with realistic patterns
    base_temp = 25.0
    base_pressure = 1013.0
    base_humidity = 45.0
    base_vibration = 2.0
    base_power = 250.0
    
    # Generate data with realistic patterns and variations
    for i in range(num_records):
        # Temperature: Daily cycle with small random variations
        daily_cycle = 2 * np.sin(2 * np.pi * i / (24 * 60))  # 24-hour cycle
        data['temperature_zone1'].append(round(base_temp + daily_cycle + random.uniform(-0.5, 0.5), 2))
        data['temperature_zone2'].append(round(base_temp + daily_cycle + random.uniform(-0.5, 0.5), 2))
        
        # Pressure: Small variations around base value
        data['pressure_zone1'].append(round(base_pressure + random.uniform(-1, 1), 2))
        data['pressure_zone2'].append(round(base_pressure + random.uniform(-1, 1), 2))
        
        # Humidity: Gradual changes with small variations
        data['humidity_zone1'].append(round(base_humidity + random.uniform(-2, 2), 2))
        data['humidity_zone2'].append(round(base_humidity + random.uniform(-2, 2), 2))
        
        # Vibration: Random spikes with base level
        data['vibration_machine1'].append(round(base_vibration + random.uniform(-0.5, 0.5), 2))
        data['vibration_machine2'].append(round(base_vibration + random.uniform(-0.5, 0.5), 2))
        
        # Power: Gradual changes with small variations
        data['power_line1'].append(round(base_power + random.uniform(-10, 10), 2))
        data['power_line2'].append(round(base_power + random.uniform(-10, 10), 2))
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv('sensor_data.csv', index=False)
    print(f"Generated {num_records} records of sensor data")

if __name__ == "__main__":
    generate_sensor_data(1000)  # Generate 1000 records (about 16.7 hours of data) 