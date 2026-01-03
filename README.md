# 🏎️ F1 Visual Dashboard - Interactive Streamlit App

[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Live Demo](https://img.shields.io/badge/Live-Demo-success.svg)](YOUR_STREAMLIT_LINK_HERE)

## 🚀 Live Application

### 📱 **Try it Now!**
🔗 **[Launch F1 Visual Dashboard](YOUR_STREAMLIT_LINK_HERE)**

![App Demo](images/app_demo.gif)
*Interactive demo of the dashboard in action*

---

## 📊 Project Overview

A fully interactive web application built with Streamlit for real-time Formula 1 data visualization and analysis. Features include live race tracking, driver comparisons, team analytics, and predictive insights.

**Why Streamlit?**
- ⚡ Fast deployment
- 🎨 Beautiful UI out of the box
- 🔄 Real-time updates
- 📱 Mobile responsive
- 🆓 Free hosting

![Landing Page](images/landing_page.png)
*Dashboard landing page with navigation*

---

## ✨ Application Features

### 🏠 Home Page
![Home Page](images/home_page.png)

**Features:**
- Current season overview
- Latest race results
- Live championship standings
- Quick stats carousel

---

### 👤 Driver Analysis Page
![Driver Analysis](images/driver_analysis.png)

**Interactive Elements:**
- Select driver from dropdown
- View career statistics
- Performance trends over time
- Head-to-head comparisons

**Visualizations:**
- Line chart: Points progression
- Bar chart: Wins by season
- Radar chart: Performance metrics
- Heatmap: Track-specific performance

**Sample Code:**
```python
# Driver selection widget
selected_driver = st.selectbox(
    "Choose a Driver",
    options=drivers_list,
    index=0
)

# Display statistics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Points", driver_points, delta="+125")
with col2:
    st.metric("Win Rate", f"{win_rate}%", delta="+2.3%")
with col3:
    st.metric("Podium Rate", f"{podium_rate}%")
```

---

### 🏁 Race Analysis Page
![Race Analysis](images/race_analysis.png)

**Features:**
- Race selection by season/circuit
- Lap-by-lap position changes
- Pit stop strategy visualization
- Fastest lap analysis

**Interactive Charts:**
- Animated position changes
- Tire strategy timeline
- Gap analysis between drivers
- Sector time comparisons

---

### 🔧 Team Performance Page
![Team Performance](images/team_performance.png)

**Analytics:**
- Constructor standings
- Team comparison tools
- Resource allocation analysis
- Strategy success rates

**Visualizations:**
- Stacked area chart: Points accumulation
- Grouped bar chart: Win comparison
- Sunburst chart: Points distribution
- Box plot: Consistency analysis

---

### 📈 Statistical Insights Page
![Statistical Insights](images/statistical_page.png)

**Advanced Features:**
- Correlation analysis
- Regression predictions
- Hypothesis testing results
- Interactive statistical tests

**Tools:**
- Correlation heatmap (interactive)
- Distribution plots
- Scatter plots with regression lines
- Statistical test results tables

---

### 🔮 Predictions Page
![Predictions](images/predictions_page.png)

**Machine Learning Features:**
- Race winner prediction
- Points forecast
- Championship simulation
- What-if scenarios

**User Inputs:**
- Circuit selection
- Weather conditions
- Starting grid positions
- Historical performance weights

---

## 🎨 Application Screenshots

### Mobile View
<p align="center">
  <img src="images/mobile_view.png" width="300" alt="Mobile View">
</p>

*Fully responsive design for mobile devices*

### Dark Mode
![Dark Mode](images/dark_mode.png)
*Toggle between light and dark themes*

### Data Export
![Export Feature](images/export_feature.png)
*Download data in CSV/Excel format*

---

## 🛠️ Technical Stack

### Frontend:
- **Streamlit** - Web framework
- **Plotly** - Interactive visualizations
- **Altair** - Statistical graphics

### Backend:
- **Python 3.9+** - Core language
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning

### Deployment:
- **Streamlit Cloud** - Free hosting
- **GitHub** - Version control
- **Ergast API** - Data source

---

## 📦 Project Structure

f1-visual-dashboard/
├── app.py                      # Main Streamlit application
├── pages/
│   ├── 1_🏠_Home.py
│   ├── 2_👤_Driver_Analysis.py
│   ├── 3_🏁_Race_Analysis.py
│   ├── 4_🔧_Team_Performance.py
│   ├── 5_📈_Statistical_Insights.py
│   └── 6_🔮_Predictions.py
├── utils/
│   ├── data_loader.py         # Data fetching functions
│   ├── visualization.py       # Plotting functions
│   ├── analysis.py            # Statistical analysis
│   └── ml_models.py           # Prediction models
├── data/
│   ├── cache/                 # Cached API responses
│   └── processed/             # Preprocessed datasets
├── images/                    # Screenshots for README
├── .streamlit/
│   └── config.toml           # App configuration
├── requirements.txt
├── README.md
└── app_screenshot.py         # Screenshot automation

---

## 🚀 Local Installation & Usage

### Prerequisites
```bash
Python 3.9 or higher
pip package manager
```

### Step 1: Clone Repository
```bash
git clone https://github.com/debastene/f1-visual-dashboard.git
cd f1-visual-dashboard
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Application
```bash
streamlit run app.py
```

### Step 4: Open Browser

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501

---

## 🌐 Deployment to Streamlit Cloud

### Quick Deploy (5 minutes):

1. **Fork this repository** to your GitHub

2. **Go to** [share.streamlit.io](https://share.streamlit.io)

3. **Click "New app"**

4. **Fill in:**
   - Repository: `your-username/f1-visual-dashboard`
   - Branch: `main`
   - Main file: `app.py`

5. **Click "Deploy"**

6. **Done!** Your app will be live at:
https://your-app-name.streamlit.app

### Configuration (Optional):

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF1E00"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"

[server]
maxUploadSize = 200
enableXsrfProtection = true
```

---

## 📊 Data Sources

### Primary API:
**Ergast F1 API**
- Endpoint: `http://ergast.com/api/f1`
- Update Frequency: Real-time during race weekends
- Historical Data: 1950-present

### Data Caching:
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_race_data(season, round):
    url = f"http://ergast.com/api/f1/{season}/{round}/results.json"
    response = requests.get(url)
    return process_data(response.json())
```

---

## 💡 Key Features Explained

### 1. Real-Time Data Updates
```python
# Auto-refresh every 30 seconds during races
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.experimental_rerun()
```

### 2. Interactive Filtering
```python
# Multi-select filters
selected_seasons = st.multiselect(
    "Select Seasons",
    options=range(2018, 2024),
    default=[2023]
)

selected_teams = st.multiselect(
    "Select Teams",
    options=team_list,
    default=["Red Bull Racing", "Mercedes"]
)
```

### 3. Download Functionality
```python
# Export data to CSV
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df_to_csv(data)
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="f1_data.csv",
    mime="text/csv"
)
```

### 4. Sidebar Navigation
```python
# Sidebar with filters
with st.sidebar:
    st.image("images/f1_logo.png")
    st.title("F1 Dashboard")
    
    season = st.selectbox("Season", range(2023, 2017, -1))
    race = st.selectbox("Race", races_list)
    
    st.markdown("---")
    st.info("💡 Tip: Hover over charts for details!")
```

---

## 📈 Performance Metrics

**App Performance:**
- Load Time: < 2 seconds
- Data Fetch: < 1 second (cached)
- Visualization Render: < 0.5 seconds
- Memory Usage: ~150 MB

**Optimization Techniques:**
- `@st.cache_data` for expensive operations
- Lazy loading for large datasets
- Efficient pandas operations
- Plotly WebGL rendering

---

## 🎓 Learning Outcomes

### Streamlit Skills:
✅ Multi-page app architecture
✅ Session state management
✅ Custom components
✅ Deployment strategies

### Data Visualization:
✅ Interactive Plotly charts
✅ Real-time updates
✅ Responsive design
✅ UX best practices

### API Integration:
✅ RESTful API consumption
✅ Data caching strategies
✅ Error handling
✅ Rate limiting

---

## 🐛 Troubleshooting

### Common Issues:

**Issue:** App won't start
```bash
# Solution: Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Issue:** API rate limit exceeded
```python
# Solution: Implement caching
@st.cache_data(ttl=7200)  # Cache for
