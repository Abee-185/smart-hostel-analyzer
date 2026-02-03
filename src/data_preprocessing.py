"""
Data Preprocessing Module
This module handles data cleaning, transformation, and preparation.
"""

import pandas as pd
import numpy as np


def preprocess_data(df):
    """
    Preprocess the data by parsing dates, sorting, and cleaning.
    
    Args:
        df (pandas.DataFrame): Raw dataframe
        
    Returns:
        pandas.DataFrame: Processed dataframe
    """
    if df is None or len(df) == 0:
        return None
    
    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # Parse date column
    df_clean['date'] = pd.to_datetime(df_clean['date'])
    
    # Sort by date and hostel block
    df_clean = df_clean.sort_values(['hostel_block', 'date']).reset_index(drop=True)
    
    # Remove duplicates if any
    df_clean = df_clean.drop_duplicates()
    
    # Handle missing values (if any)
    df_clean = df_clean.dropna()
    
    return df_clean


def filter_by_block(df, block):
    """
    Filter data for a specific hostel block.
    
    Args:
        df (pandas.DataFrame): Input dataframe
        block (str): Hostel block identifier (e.g., 'A', 'B')
        
    Returns:
        pandas.DataFrame: Filtered dataframe
    """
    if df is None:
        return None
    return df[df['hostel_block'] == block].copy()


def filter_by_date_range(df, start_date=None, end_date=None):
    """
    Filter data by date range.
    
    Args:
        df (pandas.DataFrame): Input dataframe
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
        
    Returns:
        pandas.DataFrame: Filtered dataframe
    """
    if df is None:
        return None
    
    df_filtered = df.copy()
    
    if start_date:
        df_filtered = df_filtered[df_filtered['date'] >= pd.to_datetime(start_date)]
    
    if end_date:
        df_filtered = df_filtered[df_filtered['date'] <= pd.to_datetime(end_date)]
    
    return df_filtered


def add_time_features(df):
    """
    Add time-based features for better analysis.
    
    Args:
        df (pandas.DataFrame): Input dataframe with 'date' column
        
    Returns:
        pandas.DataFrame: Dataframe with additional time features
    """
    if df is None:
        return None
    
    df_enhanced = df.copy()
    
    # Extract time features
    df_enhanced['day_of_week'] = df_enhanced['date'].dt.day_name()
    df_enhanced['day_of_month'] = df_enhanced['date'].dt.day
    df_enhanced['month'] = df_enhanced['date'].dt.month
    df_enhanced['year'] = df_enhanced['date'].dt.year
    
    return df_enhanced


def normalize_consumption_column(df, consumption_col):
    """
    Normalize consumption values for better comparison.
    
    Args:
        df (pandas.DataFrame): Input dataframe
        consumption_col (str): Name of consumption column
        
    Returns:
        pandas.DataFrame: Dataframe with normalized values
    """
    if df is None or consumption_col not in df.columns:
        return None
    
    df_normalized = df.copy()
    
    # Min-max normalization
    min_val = df_normalized[consumption_col].min()
    max_val = df_normalized[consumption_col].max()
    
    if max_val - min_val > 0:
        df_normalized[f'{consumption_col}_normalized'] = (
            (df_normalized[consumption_col] - min_val) / (max_val - min_val)
        )
    
    return df_normalized
