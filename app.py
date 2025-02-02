import streamlit as st
from src.data_loader import DataLoader
from src.data_processor import DataProcessor
from src.visualizer import Visualizer
from src.ai_analyzer import AIAnalyzer
from src.utils import display_error, log_execution_time

# Set page configuration
st.set_page_config(
    page_title="Data Analysis App",
    layout="centered",
)

# Sidebar information
st.sidebar.title("About This App")
st.sidebar.write("""
    Welcome to the Data Analysis App! This tool helps you analyze your data efficiently.
    
    ## What You Can Do
    - Upload CSV files for analysis
    - Get detailed statistical summaries
    - View interactive visualizations
    - Discover AI-powered insights
    
    ## How It Works
    1. Upload your CSV file
    2. Browse through automated analysis
    3. Explore visualizations
    4. Generate AI insights
    
    ## Features
    - Basic statistics
    - Missing value detection
    - Outlier analysis
    - Correlation analysis
    - Distribution plots
    - Custom visualizations
""")

# Main content
st.title("Data Analysis App")
st.write("""
    **Welcome to the Data Analysis App!**
    This app helps you analyze and visualize your data with ease.
""")

# File upload section between lines
st.markdown("---")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

@log_execution_time
def main():
    """Main function to run the Streamlit app."""
    if uploaded_file:
        try:
            # Load data
            with st.spinner("Loading data..."):
                df = DataLoader.load_csv(uploaded_file)
            if df is None:
                display_error("Failed to load the file. Please check the file format.")
                return

            # Display raw data
            st.subheader("Raw Data")
            st.write(df)

            # Data processing
            st.subheader("Data Analysis")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Basic Statistics**")
                stats = DataProcessor.get_basic_statistics(df)
                st.write(stats)

                st.markdown("**Missing Values**")
                missing_values = DataProcessor.detect_missing_values(df)
                st.write(missing_values)

            with col2:
                st.markdown("**Outliers**")
                outliers = DataProcessor.detect_outliers(df)
                st.write(outliers)

                st.markdown("**Categorical Analysis**")
                categorical_analysis = DataProcessor.analyze_categorical_data(df)
                st.write(categorical_analysis)

            # Visualizations
            st.subheader("Visualizations")
            numeric_columns = df.select_dtypes(include=["number"]).columns
            if len(numeric_columns) > 0:
                selected_column = st.selectbox("Select a column for distribution plot", numeric_columns)
                Visualizer.plot_distribution(df, selected_column)
                Visualizer.plot_correlation_heatmap(df)
                Visualizer.plot_boxplot(df, selected_column)
                Visualizer.plot_missing_values(df)
            else:
                st.warning("No numeric columns found for visualization.")

            # AI Analysis
            st.subheader("AI Insights")
            if st.button("Generate Insights"):
                with st.spinner("Generating insights..."):
                    data_summary = {
                        "numerical": stats,
                        "missing_values": missing_values,
                        "outliers": outliers,
                        "categorical": categorical_analysis,
                    }
                    insights = AIAnalyzer.generate_insights(data_summary)
                if insights:
                    st.markdown("**Generated Insights**")
                    st.write(insights)
                else:
                    display_error("Failed to generate insights. Please check your API token or try again later.")

        except Exception as e:
            display_error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.write("""
    **Data Analysis App**
    Made with ❤️ by Your Name
    [GitHub](https://github.com/your-username) | [LinkedIn](https://linkedin.com/in/your-profile)
""")

if __name__ == "__main__":
    main()