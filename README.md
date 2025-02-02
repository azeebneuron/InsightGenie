
# **InsightGenie**

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-3776AB?style=for-the-badge&logo=python&logoColor=white)

A modular Streamlit application for data analysis, visualization, and AI-powered insights. This app supports CSV file uploads, handles mixed data types (numerical, categorical, and temporal), and provides robust data analysis and visualization features.

---

## **Features**

- **Data Loading**:
  - Upload CSV files.
  - Automatic encoding detection using `chardet`.
  - Comprehensive file validation and error handling.

- **Data Analysis**:
  - Basic statistics (mean, median, std dev, min, max).
  - Missing value analysis.
  - Outlier detection.
  - Categorical data analysis (value counts, unique values).

- **Visualizations**:
  - Distribution plots (histograms, KDE).
  - Correlation heatmaps.
  - Box plots for outlier visualization.
  - Missing value heatmaps.
  - Temporal data plots (time series).

- **AI-Powered Insights**:
  - Integration with OpenAI API for generating textual insights.
  - Narrative generation about data patterns.
  - Key findings and recommendations.

- **User Interface**:
  - Clean, modern interface using Streamlit.
  - Sidebar for file upload and settings.
  - Tabs for different analysis sections.
  - Progress indicators and loading states.
  - Download options for reports and visualizations.

---

## **Installation**

### **Prerequisites**
- Python 3.8 or higher.
- Required libraries (install via `requirements.txt`).

### **Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/azeebneuron/InsightGenie.git
   cd streamlit-data-analysis-app
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your `AIPROXY_TOKEN`:
   ```env
   AIPROXY_TOKEN=your_api_token_here
   ```

5. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

---

## **Usage**

1. **Upload a CSV File**:
   - Use the sidebar to upload a CSV file.
   - The app will automatically detect the file encoding and load the data.

2. **Explore Data Analysis**:
   - View basic statistics, missing values, and outliers.
   - Analyze categorical data (value counts, unique values).

3. **Visualize Data**:
   - Explore distribution plots, correlation heatmaps, and box plots.
   - Visualize missing values and temporal data.

4. **Generate AI Insights**:
   - Click the "Generate Insights" button to get AI-powered insights about your data.

5. **Download Results**:
   - Download visualizations and reports for further analysis.

---

## **Project Structure**

```
project/
│
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration and environment variables
│   ├── data_loader.py     # File handling and data loading
│   ├── data_processor.py  # Data analysis and processing
│   ├── visualizer.py      # Visualization functions
│   ├── ai_analyzer.py     # AI-powered analysis
│   └── utils.py           # Utility functions
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # List of dependencies
└── .env                   # Environment variables
```

---

## **Dependencies**

- **Core Libraries**:
  - `streamlit`
  - `pandas`
  - `numpy`
  - `seaborn`
  - `matplotlib`
  - `scikit-learn`
  - `chardet`
  - `httpx`
  - `python-dotenv`

- **AI Integration**:
  - OpenAI API (via `AIPROXY_TOKEN`).

---

## **Contributing**

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---