# 🏢 Smart Hostel Resource Usage Analyzer

## Overview

A **Data Analytics + IoT Simulation** mini-project that analyzes electricity and water consumption in hostels using **simulated smart meter data**. This project demonstrates how IoT concepts can be implemented **without physical hardware** using data analytics and machine learning.

---

## ✨ Key Features

### 📊 **Data Analytics**
- Load and preprocess CSV-based IoT smart meter data
- Calculate consumption statistics (average, max, min, total)
- Analyze trends over time
- Compare usage across different hostel blocks

### 🔍 **Anomaly Detection**
- Detect abnormal over-usage using statistical methods
- Flag high and low consumption anomalies
- Visual identification of unusual patterns

### 🤖 **Machine Learning Predictions**
- Predict next-day consumption using Linear Regression
- 7-day consumption forecasting
- Model performance metrics (R², RMSE, MAE)
- **Predictions update automatically when new data is added**

### 📱 **Interactive Dashboard**
- Real-time data visualization using Streamlit
- Multiple views: Analytics, Anomaly Detection, Predictions, Raw Data
- Interactive charts and graphs
- Filter by hostel block and resource type

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Programming Language** | Python 3.x |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib |
| **Machine Learning** | Scikit-learn |
| **Dashboard** | Streamlit |

---

## 📁 Project Structure

```
Smart_Hostel_Resource_Analyzer/
│
├── data/                           # IoT simulated data
│   ├── electricity_data.csv        # Electricity consumption records
│   └── water_data.csv              # Water consumption records
│
├── src/                            # Core modules
│   ├── data_loader.py              # Load CSV data
│   ├── data_preprocessing.py       # Clean and transform data
│   ├── analysis.py                 # Statistical analysis & anomaly detection
│   └── prediction.py               # ML prediction model
│
├── app.py                          # Streamlit dashboard
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Verify Data Files

Ensure the following CSV files exist in the `data/` folder:
- `electricity_data.csv`
- `water_data.csv`

---

## ▶️ Running the Application

### Launch the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser at: `http://localhost:8501`

---

## 📊 Data Format

### Electricity Data (`electricity_data.csv`)

| Column | Description |
|--------|-------------|
| `date` | Date in YYYY-MM-DD format |
| `hostel_block` | Hostel block identifier (A, B, etc.) |
| `units_consumed` | Electricity consumed in kWh units |

**Example:**
```csv
date,hostel_block,units_consumed
2024-01-01,A,320
2024-01-02,A,350
2024-01-03,A,410
```

### Water Data (`water_data.csv`)

| Column | Description |
|--------|-------------|
| `date` | Date in YYYY-MM-DD format |
| `hostel_block` | Hostel block identifier (A, B, etc.) |
| `liters_used` | Water consumed in liters |

**Example:**
```csv
date,hostel_block,liters_used
2024-01-01,A,2200
2024-01-02,A,2500
2024-01-03,A,3000
```

---

## 🎯 How It Works

### 1. **IoT Concept Without Hardware**

**Traditional IoT Setup:**
- Physical sensors (electricity meters, water flow sensors)
- Hardware transmits data to cloud servers
- Real-time data collection

**Our Approach:**
- CSV files **simulate** smart meter data
- Data represents what sensors would collect
- System processes data as if received from IoT devices
- **No physical hardware needed!**

### 2. **Real-Time vs. Simulated Real-Time**

| Aspect | This Project |
|--------|--------------|
| **Data Collection** | Simulated (CSV files) |
| **Processing** | Real-time when dashboard runs |
| **Updates** | Manual (add new rows to CSV) |
| **Behavior** | Simulates real-time analytics |

**How to Simulate New Data:**
1. Open `electricity_data.csv` or `water_data.csv`
2. Add new rows with future dates
3. Refresh the dashboard
4. **Predictions automatically update!**

### 3. **Machine Learning Prediction**

**Algorithm:** Linear Regression

**How It Works:**
1. Loads historical consumption data
2. Trains a model to learn patterns
3. Predicts future consumption based on trends
4. Updates automatically when new data is added

**Example:**
- If consumption is increasing daily by 10 units
- Model predicts next day will be: Last Value + 10 units
- Adapts to new patterns as data grows

---

## 📈 Dashboard Features

### Tab 1: Analytics Dashboard
- **Metrics:** Average, Max, Min, Total consumption
- **Trends:** Daily changes, percentage changes
- **Charts:** Time-series consumption visualization
- **Comparison:** Block-wise usage comparison

### Tab 2: Anomaly Detection
- **Detection:** Statistical anomaly identification
- **Visualization:** Red markers for unusual consumption
- **Summary:** Count of high/low usage alerts
- **Records:** Detailed list of anomalies

### Tab 3: ML Predictions
- **Model Metrics:** R², RMSE, MAE scores
- **Next-Day Forecast:** Predicted consumption
- **7-Day Forecast:** Weekly prediction chart
- **Trend Analysis:** Increasing/decreasing patterns

### Tab 4: Raw Data
- **Full Dataset:** View all records
- **Export:** Download as CSV

---

## 🎓 Viva Preparation - Key Points

### Q: Is this real-time or simulated?
**A:** This is **simulated real-time**. We use CSV files to represent sensor data, but the analytics and predictions run in real-time when the dashboard is active.

### Q: How does IoT work without hardware?
**A:** We simulate IoT data collection using CSV files. In a real system, sensors would generate this data. Our project focuses on the **data processing and analysis** layer of IoT.

### Q: How do predictions change with new data?
**A:** 
1. Add new rows to CSV files
2. Refresh the dashboard
3. The ML model retrains with updated data
4. New predictions reflect the latest patterns

### Q: What is anomaly detection?
**A:** We use **statistical methods** (standard deviation) to identify consumption values that are unusually high or low compared to normal patterns.

### Q: Why is this suitable for a mini project?
**A:**
- ✅ Demonstrates IoT concepts without expensive hardware
- ✅ Uses industry-standard tools (Python, ML, Streamlit)
- ✅ Real-world application (resource management)
- ✅ Complete software lifecycle (data → analysis → prediction → visualization)
- ✅ Easy to demonstrate and explain

---

## 🔧 Extending the Project

### Add More Data
```python
# Simply append new rows to CSV files
2024-01-31,A,500
2024-02-01,A,520
```

### Add More Hostel Blocks
```python
# Add rows with new block identifiers
2024-01-01,C,300
2024-01-02,C,310
```

### Improve Predictions
- Try different ML algorithms (Random Forest, LSTM)
- Add more features (day of week, holidays)
- Implement time-series forecasting

---

## 📝 Module Descriptions

### `data_loader.py`
- Loads CSV files into Pandas DataFrames
- Validates data file existence
- Provides data access functions

### `data_preprocessing.py`
- Parses dates and sorts data
- Filters by block or date range
- Adds time-based features
- Cleans and normalizes data

### `analysis.py`
- Calculates statistical metrics
- Detects anomalies using standard deviation
- Analyzes consumption trends
- Compares different hostel blocks

### `prediction.py`
- Prepares data for ML training
- Trains Linear Regression model
- Generates predictions
- Calculates model performance metrics

### `app.py`
- Creates Streamlit dashboard
- Integrates all modules
- Provides interactive visualizations
- Manages user interface

---

## 🏆 Project Highlights

✅ **No Hardware Required** - Pure software implementation  
✅ **Industry-Ready Tools** - Python, Pandas, ML, Streamlit  
✅ **Real-World Application** - Resource management in hostels  
✅ **Complete Analytics Pipeline** - Load → Process → Analyze → Predict  
✅ **Interactive Dashboard** - Professional web-based UI  
✅ **Beginner-Friendly** - Clean, modular, well-documented code  
✅ **Viva-Ready** - Clear explanations and demonstrations  

---

## 📧 Support

For questions or issues:
1. Review this README
2. Check code comments in Python files
3. Verify all dependencies are installed
4. Ensure CSV files are properly formatted

---

## 🎉 Conclusion

This project successfully demonstrates:
- **IoT concepts** without physical hardware
- **Data Analytics** techniques for resource monitoring
- **Machine Learning** for consumption prediction
- **Real-time simulation** using CSV-based data
- **Professional dashboard** for data visualization

**Perfect for:**
- College mini projects
- Data Analytics + IoT subject
- Portfolio demonstrations
- Learning Python data science

---

**Built with ❤️ for educational purposes**
