"""
Data Loader Module
This module handles loading data from CSV files.
Simulates IoT data ingestion without actual hardware.
"""

import pandas as pd
import os


def load_electricity_data(file_path='data/electricity_data.csv'):
    """
    Load electricity consumption data from CSV file.
    
    Args:
        file_path (str): Path to the electricity data CSV file
        
    Returns:
        pandas.DataFrame: Loaded electricity data
    """
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Successfully loaded {len(df)} electricity records")
        return df
    except FileNotFoundError:
        print(f"❌ Error: File not found - {file_path}")
        return None
    except Exception as e:
        print(f"❌ Error loading electricity data: {e}")
        return None


def load_water_data(file_path='data/water_data.csv'):
    """
    Load water consumption data from CSV file.
    
    Args:
        file_path (str): Path to the water data CSV file
        
    Returns:
        pandas.DataFrame: Loaded water data
    """
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Successfully loaded {len(df)} water records")
        return df
    except FileNotFoundError:
        print(f"❌ Error: File not found - {file_path}")
        return None
    except Exception as e:
        print(f"❌ Error loading water data: {e}")
        return None


def get_latest_data(df, n=10):
    """
    Get the latest n records from the dataframe.
    Simulates real-time data monitoring.
    
    Args:
        df (pandas.DataFrame): Input dataframe
        n (int): Number of latest records to retrieve
        
    Returns:
        pandas.DataFrame: Latest n records
    """
    if df is None or len(df) == 0:
        return None
    return df.tail(n)


def check_data_files():
    """
    Check if data files exist and are readable.
    
    Returns:
        dict: Status of each data file
    """
    files = {
        'electricity': 'data/electricity_data.csv',
        'water': 'data/water_data.csv'
    }
    
    status = {}
    for key, path in files.items():
        status[key] = os.path.exists(path)
    
    return status
