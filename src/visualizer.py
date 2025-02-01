import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List

class Visualizer:
    """Handles data visualization tasks for mixed data types."""

    @staticmethod
    def set_style():
        """Set custom styling for plots."""
        sns.set(style="whitegrid", palette="pastel")

    @staticmethod
    def plot_distribution(df: pd.DataFrame, column: str):
        """
        Plot distribution of a column (numerical or categorical).
        
        Args:
            df (pd.DataFrame): Input DataFrame.
            column (str): Column to plot.
        """
        Visualizer.set_style()
        plt.figure(figsize=(8, 6))
        
        if pd.api.types.is_numeric_dtype(df[column]):
            sns.histplot(df[column], kde=True, color="skyblue")
            plt.title(f"Distribution of {column}", fontsize=16)
            plt.xlabel(column, fontsize=14)
            plt.ylabel("Frequency", fontsize=14)
        else:
            sns.countplot(y=df[column], color="skyblue", order=df[column].value_counts().index)
            plt.title(f"Value Counts of {column}", fontsize=16)
            plt.xlabel("Count", fontsize=14)
            plt.ylabel(column, fontsize=14)
        
        st.pyplot(plt)

    @staticmethod
    def plot_correlation_heatmap(df: pd.DataFrame):
        """
        Plot a correlation heatmap for numerical columns.
        
        Args:
            df (pd.DataFrame): Input DataFrame.
        """
        numerical_cols = df.select_dtypes(include=["number"]).columns
        if len(numerical_cols) == 0:
            st.warning("No numerical columns found for correlation heatmap.")
            return
        
        Visualizer.set_style()
        plt.figure(figsize=(10, 8))
        corr = df[numerical_cols].corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
        plt.title("Correlation Heatmap", fontsize=16)
        st.pyplot(plt)

    @staticmethod
    def plot_boxplot(df: pd.DataFrame, column: str):
        """
        Plot a boxplot for a numerical column.
        
        Args:
            df (pd.DataFrame): Input DataFrame.
            column (str): Column to plot.
        """
        if not pd.api.types.is_numeric_dtype(df[column]):
            st.warning(f"Cannot plot boxplot for non-numeric column: {column}")
            return
        
        Visualizer.set_style()
        plt.figure(figsize=(8, 6))
        sns.boxplot(x=df[column], color="lightgreen")
        plt.title(f"Boxplot of {column}", fontsize=16)
        plt.xlabel(column, fontsize=14)
        st.pyplot(plt)

    @staticmethod
    def plot_temporal_data(df: pd.DataFrame, column: str):
        """
        Plot temporal data (e.g., time series).
        
        Args:
            df (pd.DataFrame): Input DataFrame.
            column (str): Temporal column to plot.
        """
        if not pd.api.types.is_datetime64_any_dtype(df[column]):
            st.warning(f"Cannot plot temporal data for non-datetime column: {column}")
            return
        
        Visualizer.set_style()
        plt.figure(figsize=(10, 6))
        df.set_index(column).plot()
        plt.title(f"Temporal Plot of {column}", fontsize=16)
        plt.xlabel(column, fontsize=14)
        plt.ylabel("Value", fontsize=14)
        st.pyplot(plt)
    
    @staticmethod
    def plot_missing_values(df: pd.DataFrame):
        """
        Visualize missing values in the dataset using a heatmap.
        
        Args:
            df (pd.DataFrame): Input DataFrame.
        """
        Visualizer.set_style()
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.isnull(), cbar=False, cmap="viridis")
        plt.title("Missing Values Heatmap", fontsize=16)
        st.pyplot(plt)

# Example usage
# if __name__ == "__main__":
#     data = {
#         "col1": [1, 2, 3, 4, 5],
#         "col2": ["A", "B", "A", "C", "B"],
#         "col3": ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"],
#     }
#     df = pd.DataFrame(data)
#     df["col3"] = pd.to_datetime(df["col3"])  # Convert to datetime

#     st.title("Data Visualizations")
#     Visualizer.plot_distribution(df, "col1")
#     Visualizer.plot_distribution(df, "col2")
#     Visualizer.plot_correlation_heatmap(df)
#     Visualizer.plot_boxplot(df, "col1")
#     Visualizer.plot_temporal_data(df, "col3")
#     Visualizer.plot_missing_values(df)