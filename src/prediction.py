"""
Prediction Module
This module uses machine learning to predict future consumption.
Uses Linear Regression for next-day prediction.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


def prepare_data_for_prediction(df, consumption_col):
    """
    Prepare data for machine learning prediction.
    Creates features based on date index.
    
    Args:
        df (pandas.DataFrame): Input dataframe with date column
        consumption_col (str): Name of consumption column to predict
        
    Returns:
        tuple: (X, y) features and target
    """
    if df is None or len(df) == 0:
        return None, None
    
    df_sorted = df.sort_values('date').copy()
    
    # Create sequential index as feature (day number)
    df_sorted['day_index'] = range(1, len(df_sorted) + 1)
    
    X = df_sorted[['day_index']].values
    y = df_sorted[consumption_col].values
    
    return X, y


def train_prediction_model(X, y):
    """
    Train a Linear Regression model for consumption prediction.
    
    Args:
        X (numpy.array): Feature matrix
        y (numpy.array): Target values
        
    Returns:
        tuple: (model, metrics) trained model and performance metrics
    """
    if X is None or y is None or len(X) == 0:
        return None, None
    
    # Split data into training and testing sets (80-20 split)
    if len(X) > 5:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
    else:
        # If too few samples, use all for training
        X_train, X_test, y_train, y_test = X, X, y, y
    
    # Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predictions on test set
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    metrics = {
        'r2_score': r2_score(y_test, y_pred),
        'mse': mean_squared_error(y_test, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
        'mae': mean_absolute_error(y_test, y_pred)
    }
    
    return model, metrics


def predict_next_day(model, last_day_index):
    """
    Predict consumption for the next day.
    
    Args:
        model: Trained Linear Regression model
        last_day_index (int): Index of the last day in the dataset
        
    Returns:
        float: Predicted consumption value
    """
    if model is None:
        return None
    
    next_day_index = last_day_index + 1
    prediction = model.predict([[next_day_index]])
    
    return prediction[0]


def predict_multiple_days(model, last_day_index, num_days=7):
    """
    Predict consumption for multiple future days.
    
    Args:
        model: Trained Linear Regression model
        last_day_index (int): Index of the last day in the dataset
        num_days (int): Number of days to predict
        
    Returns:
        list: List of predicted values
    """
    if model is None:
        return None
    
    predictions = []
    for i in range(1, num_days + 1):
        future_day_index = last_day_index + i
        pred = model.predict([[future_day_index]])
        predictions.append(pred[0])
    
    return predictions


def get_prediction_summary(df, consumption_col, hostel_block=None):
    """
    Complete prediction pipeline: prepare data, train model, and predict.
    
    Args:
        df (pandas.DataFrame): Input dataframe
        consumption_col (str): Name of consumption column
        hostel_block (str): Optional filter for specific hostel block
        
    Returns:
        dict: Prediction results and model metrics
    """
    if df is None or len(df) == 0:
        return None
    
    # Filter by block if specified
    if hostel_block:
        df = df[df['hostel_block'] == hostel_block].copy()
    
    # Prepare data
    X, y = prepare_data_for_prediction(df, consumption_col)
    
    if X is None or len(X) == 0:
        return None
    
    # Train model
    model, metrics = train_prediction_model(X, y)
    
    if model is None:
        return None
    
    # Predict next day
    last_day_index = len(X)
    next_day_pred = predict_next_day(model, last_day_index)
    
    # Predict next 7 days
    week_predictions = predict_multiple_days(model, last_day_index, 7)
    
    summary = {
        'model_metrics': metrics,
        'last_actual_value': y[-1],
        'next_day_prediction': next_day_pred,
        'next_week_predictions': week_predictions,
        'trend_direction': 'Increasing' if next_day_pred > y[-1] else 'Decreasing',
        'predicted_change': next_day_pred - y[-1]
    }
    
    return summary
