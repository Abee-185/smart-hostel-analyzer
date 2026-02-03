"""
Smart Hostel Resource Usage Analyzer
Streamlit Dashboard Application

This dashboard displays:
- Resource consumption analytics
- Anomaly detection results
- ML-based predictions for future consumption
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import load_electricity_data, load_water_data
from data_preprocessing import preprocess_data, filter_by_block
from analysis import (
    calculate_statistics, detect_anomalies, 
    get_anomalies_summary, analyze_trends, compare_blocks
)
from prediction import get_prediction_summary


# Page configuration
st.set_page_config(
    page_title="Smart Hostel Resource Analyzer",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern app-like design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background with gradient */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Content area */
    .block-container {
        padding: 2rem 3rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        margin: 2rem auto;
        backdrop-filter: blur(10px);
    }
    
    /* Header styling */
    h1 {
        color: #1a1a2e;
        font-weight: 700;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        color: #2d3748;
        font-weight: 600;
        font-size: 1.8rem !important;
        margin-top: 1.5rem !important;
    }
    
    h3 {
        color: #4a5568;
        font-weight: 600;
        font-size: 1.4rem !important;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #667eea !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: #4a5568 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.9rem !important;
    }
    
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea15 0%, #764ba220 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #667eea30;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: none;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #e2e8f0;
    }
    
    [data-testid="stSidebar"] h1 {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    
    /* Sidebar widgets */
    [data-testid="stSidebar"] .stSelectbox label {
        color: #e2e8f0 !important;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #667eea15 0%, #764ba220 100%);
        border-radius: 10px 10px 0 0;
        padding: 1rem 2rem;
        font-weight: 600;
        color: #4a5568;
        border: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-color: #667eea;
    }
    
    /* Info/Warning/Success boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* DataFrames */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(72, 187, 120, 0.4);
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }
    
    /* Chart containers */
    .stPlotlyChart {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Header with custom styling
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0 2rem 0;'>
            <h1 style='margin-bottom: 0.5rem;'>🏢 Smart Hostel Resource Analyzer</h1>
            <p style='font-size: 1.2rem; color: #718096; font-weight: 500;'>
                Data Analytics + IoT Simulation Platform
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with modern design
    st.sidebar.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='color: white; font-size: 1.8rem; margin-bottom: 0.5rem;'>⚙️ Controls</h1>
            <p style='color: #cbd5e0; font-size: 0.9rem;'>Configure your analysis</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Resource type selection
    st.sidebar.markdown("### 📊 Resource Type")
    resource_type = st.sidebar.selectbox(
        "Select Resource Type",
        ["Electricity", "Water"]
    )
    
    # Load data
    if resource_type == "Electricity":
        df = load_electricity_data()
        consumption_col = 'units_consumed'
        unit = 'kWh Units'
    else:
        df = load_water_data()
        consumption_col = 'liters_used'
        unit = 'Liters'
    
    if df is None:
        st.error("❌ Failed to load data. Please check if data files exist.")
        return
    
    # Preprocess data
    df = preprocess_data(df)
    
    # Hostel block selection
    st.sidebar.markdown("### 🏢 Hostel Block")
    blocks = df['hostel_block'].unique()
    selected_block = st.sidebar.selectbox("Select Block", ["All"] + list(blocks), label_visibility="collapsed")
    
    # Filter data by block if selected
    if selected_block != "All":
        df_filtered = filter_by_block(df, selected_block)
    else:
        df_filtered = df
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 About")
    st.sidebar.markdown("""
        <div style='background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px; color: #e2e8f0; font-size: 0.85rem;'>
            <p style='margin: 0;'>🔬 <strong>IoT Simulation</strong><br>
            Analyzes smart meter data without physical hardware</p>
            <p style='margin: 0.8rem 0 0 0;'>🤖 <strong>ML Powered</strong><br>
            Predicts future consumption using AI</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Analytics Dashboard", 
        "🔍 Anomaly Detection", 
        "🤖 ML Predictions",
        "📊 Raw Data"
    ])
    
    # Tab 1: Analytics Dashboard
    with tab1:
        st.header(f"📈 {resource_type} Consumption Analytics")
        
        # Statistics
        stats = calculate_statistics(df_filtered, consumption_col)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Average Consumption", f"{stats['average']:.2f} {unit}")
        with col2:
            st.metric("Maximum Consumption", f"{stats['maximum']:.2f} {unit}")
        with col3:
            st.metric("Minimum Consumption", f"{stats['minimum']:.2f} {unit}")
        with col4:
            st.metric("Total Consumption", f"{stats['total']:.2f} {unit}")
        
        st.markdown("---")
        
        # Trends
        trends = analyze_trends(df_filtered, consumption_col)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Consumption Trends")
            trend_direction = "📈 Increasing" if trends['is_increasing'] else "📉 Decreasing"
            st.write(f"**Overall Trend:** {trend_direction}")
            st.write(f"**Avg Daily Change:** {trends['average_daily_change']:.2f} {unit}")
            st.write(f"**Max Increase:** {trends['max_increase']:.2f} {unit}")
            st.write(f"**Max Decrease:** {trends['max_decrease']:.2f} {unit}")
        
        with col2:
            st.subheader("📉 Consumption Chart")
            fig, ax = plt.subplots(figsize=(10, 5))
            
            if selected_block == "All":
                for block in blocks:
                    block_data = filter_by_block(df, block)
                    ax.plot(block_data['date'], block_data[consumption_col], 
                           marker='o', label=f'Block {block}')
            else:
                ax.plot(df_filtered['date'], df_filtered[consumption_col], 
                       marker='o', color='blue', linewidth=2)
            
            ax.set_xlabel('Date')
            ax.set_ylabel(f'Consumption ({unit})')
            ax.set_title(f'{resource_type} Consumption Over Time')
            ax.grid(True, alpha=0.3)
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        # Block comparison
        if selected_block == "All":
            st.markdown("---")
            st.subheader("🏢 Hostel Block Comparison")
            comparison = compare_blocks(df, consumption_col)
            st.dataframe(comparison, width="stretch")
    
    # Tab 2: Anomaly Detection
    with tab2:
        st.header("🔍 Anomaly Detection Results")
        
        st.info(
            "🔎 Anomalies are detected using statistical analysis. "
            "Values beyond 2 standard deviations from the mean are flagged."
        )
        
        # Detect anomalies
        df_anomaly = detect_anomalies(df_filtered, consumption_col, threshold=2.0)
        anomaly_summary = get_anomalies_summary(df_anomaly, consumption_col)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Records", anomaly_summary['total_records'])
        with col2:
            st.metric("Anomalies Detected", anomaly_summary['anomaly_count'])
        with col3:
            st.metric("Anomaly Rate", f"{anomaly_summary['anomaly_percentage']:.1f}%")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Anomaly Breakdown")
            st.write(f"**High Usage Alerts:** {anomaly_summary['high_usage_count']}")
            st.write(f"**Low Usage Alerts:** {anomaly_summary['low_usage_count']}")
            
            if anomaly_summary['anomaly_count'] > 0:
                st.warning(
                    f"⚠️ {anomaly_summary['anomaly_count']} anomalies detected! "
                    "Review the chart for unusual consumption patterns."
                )
            else:
                st.success("✅ No anomalies detected. Consumption is within normal range.")
        
        with col2:
            st.subheader("📈 Anomaly Visualization")
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Plot normal data
            normal_data = df_anomaly[df_anomaly['is_anomaly'] == False]
            ax.plot(normal_data['date'], normal_data[consumption_col], 
                   marker='o', color='green', label='Normal', linewidth=2)
            
            # Plot anomalies
            anomalies = df_anomaly[df_anomaly['is_anomaly'] == True]
            if len(anomalies) > 0:
                ax.scatter(anomalies['date'], anomalies[consumption_col], 
                          color='red', s=100, label='Anomaly', zorder=5)
            
            # Add mean line
            mean_val = df_anomaly[consumption_col].mean()
            ax.axhline(y=mean_val, color='blue', linestyle='--', 
                      label=f'Mean ({mean_val:.2f})')
            
            ax.set_xlabel('Date')
            ax.set_ylabel(f'Consumption ({unit})')
            ax.set_title('Anomaly Detection Results')
            ax.legend()
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        # Show anomaly records
        if anomaly_summary['anomaly_count'] > 0:
            st.markdown("---")
            st.subheader("🔴 Detected Anomaly Records")
            anomaly_records = df_anomaly[df_anomaly['is_anomaly'] == True][
                ['date', 'hostel_block', consumption_col, 'anomaly_type']
            ]
            st.dataframe(anomaly_records, width="stretch")
    
    # Tab 3: ML Predictions
    with tab3:
        st.header("🤖 Machine Learning Predictions")
        
        st.info(
            "🧠 Using Linear Regression to predict future consumption. "
            "The model learns from historical patterns and forecasts next-day usage."
        )
        
        # Generate predictions for each block
        if selected_block == "All":
            for block in blocks:
                st.subheader(f"🏢 Block {block} Predictions")
                show_predictions(df, block, consumption_col, unit)
                st.markdown("---")
        else:
            show_predictions(df, selected_block, consumption_col, unit)
    
    # Tab 4: Raw Data
    with tab4:
        st.header("📊 Raw Data View")
        
        st.info(f"Showing {len(df_filtered)} records")
        
        # Display data
        st.dataframe(df_filtered, width="stretch")
        
        # Download button
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"{resource_type.lower()}_data.csv",
            mime="text/csv"
        )


def show_predictions(df, block, consumption_col, unit):
    """Helper function to display predictions for a specific block"""
    
    prediction = get_prediction_summary(df, consumption_col, block)
    
    if prediction is None:
        st.error("❌ Unable to generate predictions")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Model Performance")
        metrics = prediction['model_metrics']
        st.write(f"**R² Score:** {metrics['r2_score']:.4f}")
        st.write(f"**RMSE:** {metrics['rmse']:.2f}")
        st.write(f"**MAE:** {metrics['mae']:.2f}")
        
        if metrics['r2_score'] > 0.8:
            st.success("✅ High prediction accuracy!")
        elif metrics['r2_score'] > 0.6:
            st.warning("⚠️ Moderate prediction accuracy")
        else:
            st.error("❌ Low prediction accuracy - more data needed")
    
    with col2:
        st.subheader("🔮 Next Day Prediction")
        st.metric(
            "Last Actual Value",
            f"{prediction['last_actual_value']:.2f} {unit}"
        )
        st.metric(
            "Predicted Next Day",
            f"{prediction['next_day_prediction']:.2f} {unit}",
            delta=f"{prediction['predicted_change']:.2f} {unit}"
        )
        st.write(f"**Trend:** {prediction['trend_direction']}")
    
    # 7-day forecast
    st.subheader("📅 7-Day Forecast")
    
    forecast_df = pd.DataFrame({
        'Day': [f'Day +{i+1}' for i in range(7)],
        'Predicted Consumption': [f"{val:.2f}" for val in prediction['next_week_predictions']]
    })
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.dataframe(forecast_df, width="stretch")
    
    with col2:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(range(1, 8), prediction['next_week_predictions'], 
               marker='o', color='purple', linewidth=2)
        ax.set_xlabel('Days Ahead')
        ax.set_ylabel(f'Predicted Consumption ({unit})')
        ax.set_title('7-Day Consumption Forecast')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)


if __name__ == "__main__":
    main()
