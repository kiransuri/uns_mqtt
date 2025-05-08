import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_battery_plant_data(num_records=1000):
    # Generate timestamps
    start_time = datetime(2024, 5, 5, 12, 0, 0)
    timestamps = [start_time + timedelta(minutes=i) for i in range(num_records)]
    
    # Initialize data dictionary
    data = {
        'timestamp': timestamps,
        # Mixing Room Sensors
        'mixing_temperature': [],
        'mixing_humidity': [],
        'mixing_pressure': [],
        'slurry_viscosity': [],
        'slurry_density': [],
        
        # Coating Line Sensors
        'coating_thickness': [],
        'coating_speed': [],
        'coating_temperature': [],
        'coating_humidity': [],
        'web_tension': [],
        
        # Drying Oven Sensors
        'oven_temperature': [],
        'oven_humidity': [],
        'air_flow_rate': [],
        'drying_time': [],
        
        # Calendering Sensors
        'calender_pressure': [],
        'calender_temperature': [],
        'calender_speed': [],
        'electrode_thickness': [],
        
        # Slitting Sensors
        'slitting_speed': [],
        'slitting_tension': [],
        'electrode_width': [],
        
        # Environmental Sensors
        'room_temperature': [],
        'room_humidity': [],
        'room_pressure': [],
        
        # Quality Control Sensors
        'electrode_resistance': [],
        'electrode_porosity': [],
        'electrode_density': [],
        
        # Energy Monitoring
        'power_consumption': [],
        'compressed_air_pressure': [],
        'cooling_water_temperature': []
    }
    
    # Base values for different parameters
    base_values = {
        'mixing_temperature': 25.0,
        'mixing_humidity': 45.0,
        'mixing_pressure': 1013.0,
        'slurry_viscosity': 5000.0,  # cP
        'slurry_density': 1.8,  # g/cm³
        
        'coating_thickness': 100.0,  # μm
        'coating_speed': 10.0,  # m/min
        'coating_temperature': 30.0,
        'coating_humidity': 40.0,
        'web_tension': 50.0,  # N
        
        'oven_temperature': 80.0,
        'oven_humidity': 20.0,
        'air_flow_rate': 100.0,  # m³/h
        'drying_time': 5.0,  # min
        
        'calender_pressure': 100.0,  # MPa
        'calender_temperature': 60.0,
        'calender_speed': 8.0,  # m/min
        'electrode_thickness': 80.0,  # μm
        
        'slitting_speed': 15.0,  # m/min
        'slitting_tension': 30.0,  # N
        'electrode_width': 100.0,  # mm
        
        'room_temperature': 23.0,
        'room_humidity': 45.0,
        'room_pressure': 1013.0,
        
        'electrode_resistance': 0.5,  # Ω
        'electrode_porosity': 30.0,  # %
        'electrode_density': 1.6,  # g/cm³
        
        'power_consumption': 100.0,  # kW
        'compressed_air_pressure': 6.0,  # bar
        'cooling_water_temperature': 20.0
    }
    
    # Generate data with realistic patterns and variations
    for i in range(num_records):
        # Add daily cycle for temperature-related parameters
        daily_cycle = 2 * np.sin(2 * np.pi * i / (24 * 60))
        
        # Mixing Room
        data['mixing_temperature'].append(round(base_values['mixing_temperature'] + daily_cycle + random.uniform(-0.5, 0.5), 2))
        data['mixing_humidity'].append(round(base_values['mixing_humidity'] + random.uniform(-2, 2), 2))
        data['mixing_pressure'].append(round(base_values['mixing_pressure'] + random.uniform(-1, 1), 2))
        data['slurry_viscosity'].append(round(base_values['slurry_viscosity'] + random.uniform(-100, 100), 2))
        data['slurry_density'].append(round(base_values['slurry_density'] + random.uniform(-0.05, 0.05), 3))
        
        # Coating Line
        data['coating_thickness'].append(round(base_values['coating_thickness'] + random.uniform(-2, 2), 2))
        data['coating_speed'].append(round(base_values['coating_speed'] + random.uniform(-0.2, 0.2), 2))
        data['coating_temperature'].append(round(base_values['coating_temperature'] + daily_cycle + random.uniform(-0.5, 0.5), 2))
        data['coating_humidity'].append(round(base_values['coating_humidity'] + random.uniform(-2, 2), 2))
        data['web_tension'].append(round(base_values['web_tension'] + random.uniform(-2, 2), 2))
        
        # Drying Oven
        data['oven_temperature'].append(round(base_values['oven_temperature'] + random.uniform(-1, 1), 2))
        data['oven_humidity'].append(round(base_values['oven_humidity'] + random.uniform(-1, 1), 2))
        data['air_flow_rate'].append(round(base_values['air_flow_rate'] + random.uniform(-5, 5), 2))
        data['drying_time'].append(round(base_values['drying_time'] + random.uniform(-0.1, 0.1), 2))
        
        # Calendering
        data['calender_pressure'].append(round(base_values['calender_pressure'] + random.uniform(-2, 2), 2))
        data['calender_temperature'].append(round(base_values['calender_temperature'] + random.uniform(-1, 1), 2))
        data['calender_speed'].append(round(base_values['calender_speed'] + random.uniform(-0.2, 0.2), 2))
        data['electrode_thickness'].append(round(base_values['electrode_thickness'] + random.uniform(-1, 1), 2))
        
        # Slitting
        data['slitting_speed'].append(round(base_values['slitting_speed'] + random.uniform(-0.5, 0.5), 2))
        data['slitting_tension'].append(round(base_values['slitting_tension'] + random.uniform(-1, 1), 2))
        data['electrode_width'].append(round(base_values['electrode_width'] + random.uniform(-0.5, 0.5), 2))
        
        # Environmental
        data['room_temperature'].append(round(base_values['room_temperature'] + daily_cycle + random.uniform(-0.5, 0.5), 2))
        data['room_humidity'].append(round(base_values['room_humidity'] + random.uniform(-2, 2), 2))
        data['room_pressure'].append(round(base_values['room_pressure'] + random.uniform(-1, 1), 2))
        
        # Quality Control
        data['electrode_resistance'].append(round(base_values['electrode_resistance'] + random.uniform(-0.05, 0.05), 3))
        data['electrode_porosity'].append(round(base_values['electrode_porosity'] + random.uniform(-1, 1), 2))
        data['electrode_density'].append(round(base_values['electrode_density'] + random.uniform(-0.05, 0.05), 3))
        
        # Energy Monitoring
        data['power_consumption'].append(round(base_values['power_consumption'] + random.uniform(-5, 5), 2))
        data['compressed_air_pressure'].append(round(base_values['compressed_air_pressure'] + random.uniform(-0.2, 0.2), 2))
        data['cooling_water_temperature'].append(round(base_values['cooling_water_temperature'] + random.uniform(-0.5, 0.5), 2))
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv('battery_plant_data.csv', index=False)
    print(f"Generated {num_records} records of battery manufacturing plant data")

if __name__ == "__main__":
    generate_battery_plant_data(1000)  # Generate 1000 records (about 16.7 hours of data) 