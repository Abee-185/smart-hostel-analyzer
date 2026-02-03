"""
Analysis Module
This module performs statistical analysis and anomaly detection.
"""

import pandas as pd
import numpy as np


def calculate_statistics(df, consumption_col):
    """
    Calculate basic statistics for consumption data.
    
    Args:
        df (pandas.DataFrame): Input dataframe
        consumption_col (str): Name of consumption column
        
    Returns:
        dict: Dictionary containing statistics
    """
    if df is None or len(df) == 0 or consumption_col not in df.columns:
        return None
    
    stats = {
        'average': df[consumption_col].mean(),
        'maximum': df[consumption_col].max(),
        'minimum': df[consumption_col].min(),
        'median': df[consumption_col].median(),
        'std_dev': df[consumption_col].std(),
        'total': df[consumption_col].sum(),
        'count': len(df)
    }
    
    return stats


def detect_anomalies(df, consumption_col, threshold=2.0):
    """
    Detect anomalies in consumption data using standard deviation method.
    Data points beyond threshold * std_dev are considered anomalies.
    
    Args:
        df (pandas.DataFrame): Input dataframe
        consumption_col (str): Name of consumption column
        threshold (float): Number of standard deviations for anomaly threshold
        
    Returns:
        pandas.DataFrame: Dataframe with anomaly flag
    """
    if df is None or len(df) == 0 or consumption_col not in df.columns:
        return None
    
    df_anomaly = df.copy()
    
    # Calculate mean and standard deviation
    mean = df_anomaly[consumption_col].mean()
    std_dev = df_anomaly[consumption_col].std()
    
    # Define threshold boundaries
    upper_bound = mean + (threshold * std_dev)
    lower_bound = mean - (threshold * std_dev)
    
    # Flag anomalies
    df_anomaly['is_anomaly'] = (
        (df_anomaly[consumption_col] > upper_bound) | 
        (df_anomaly[consumption_col] < lower_bound)
    )
    
    df_anomaly['anomaly_type'] = 'Normal'
    df_anomaly.loc[df_anomaly[consumption_col] > upper_bound, 'anomaly_type'] = 'High Usage'
    df_anomaly.loc[df_anomaly[consumption_col] < lower_bound, 'anomaly_type'] = 'Low Usage'
    
    return df_anomaly


def get_anomalies_summary(df, consumption_col):
    """
    Get summary of detected anomalies.
    
    Args:
        df (pandas.DataFrame): Dataframe with anomaly detection results
        consumption_col (str): Name of consumption column
        
    Returns:
        dict: Summary of anomalies
    """
    if df is None or 'is_anomaly' not in df.columns:
        return None
    
    anomalies = df[df['is_anomaly'] == True]
    
    summary = {
        'total_records': len(df),
        'anomaly_count': len(anomalies),
        'anomaly_percentage': (len(anomalies) / len(df) * 100) if len(df) > 0 else 0,
        'high_usage_count': len(df[df['anomaly_type'] == 'High Usage']),
        'low_usage_count': len(df[df['anomaly_type'] == 'Low Usage'])
    }
    
    return summary


def analyze_trends(df, consumption_col):
    """
    Analyze consumption trends over time.
    
    Args:
        df (pandas.DataFrame): Input dataframe with date column
        consumption_col (str): Name of consumption column
        
    Returns:
        dict: Trend analysis results
    """
    if df is None or len(df) < 2:
        return None
    
    df_sorted = df.sort_values('date').copy()
    
    # Calculate daily change
    df_sorted['daily_change'] = df_sorted[consumption_col].diff()
    
    # Calculate percentage change
    df_sorted['pct_change'] = df_sorted[consumption_col].pct_change() * 100
    
    trends = {
        'average_daily_change': df_sorted['daily_change'].mean(),
        'max_increase': df_sorted['daily_change'].max(),
        'max_decrease': df_sorted['daily_change'].min(),
        'average_pct_change': df_sorted['pct_change'].mean(),
        'is_increasing': df_sorted[consumption_col].iloc[-1] > df_sorted[consumption_col].iloc[0]
    }
    
    return trends


def compare_blocks(df, consumption_col):
    """
    Compare consumption between different hostel blocks.
    
    Args:
        df (pandas.DataFrame): Input dataframe with hostel_block column
        consumption_col (str): Name of consumption column
        
    Returns:
        pandas.DataFrame: Comparison summary
    """
    if df is None or 'hostel_block' not in df.columns:
        return None
    
    comparison = df.groupby('hostel_block')[consumption_col].agg([
        ('Average', 'mean'),
        ('Maximum', 'max'),
        ('Minimum', 'min'),
        ('Total', 'sum'),
        ('Count', 'count')
    ]).round(2)
    
    return comparison
