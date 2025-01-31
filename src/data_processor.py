import pandas as pd
from typing import Dict, Any, List

class DataProcessor:
    """Handles data analysis and processing tasks for mixed data types."""

    @staticmethod
    def get_column_types(df: pd.DataFrame) -> Dict[str, List[str]]:
        """
        Identify numerical, categorical, and temporal columns in the DataFrame.
        
        Args:
            df (pd.DataFrame): Input DataFrame.
        
        Returns:
            Dict[str, List[str]]: Dictionary with keys 'numerical', 'categorical', and 'temporal'.
        """
        numerical_cols = df.select_dtypes(include=["number"]).columns.tolist()
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        temporal_cols = df.select_dtypes(include=["datetime"]).columns.tolist()
        
        return {
            "numerical": numerical_cols,
            "categorical": categorical_cols,
            "temporal": temporal_cols,
        }

    @staticmethod
    def get_basic_statistics(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate basic statistics for numerical columns.
        
        Args:
            df (pd.DataFrame): Input DataFrame.
        
        Returns:
            Dict[str, Any]: Dictionary containing mean, median, std dev, min, and max.
        """
        numerical_cols = df.select_dtypes(include=["number"]).columns
        if len(numerical_cols) == 0:
            return {}
        return {
            "mean": df[numerical_cols].mean().to_dict(),  # Convert Series to dict
            "median": df[numerical_cols].median().to_dict(),  # Convert Series to dict
            "std_dev": df[numerical_cols].std().to_dict(),  # Convert Series to dict
            "min": df[numerical_cols].min().to_dict(),  # Convert Series to dict
            "max": df[numerical_cols].max().to_dict(),  # Convert Series to dict
        }

    @staticmethod
    def detect_missing_values(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Detect missing values in the DataFrame.
        
        Args:
            df (pd.DataFrame): Input DataFrame.
        
        Returns:
            Dict[str, Any]: Dictionary containing missing counts and percentages.
        """
        missing_count = df.isnull().sum().to_dict()  # Convert Series to dict
        missing_percentage = (df.isnull().mean() * 100).round(2).to_dict()  # Convert Series to dict
        return {
            "missing_count": missing_count,
            "missing_percentage": missing_percentage,
        }

    @staticmethod
    def detect_outliers(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Detect outliers in numerical columns using the IQR method.
        
        Args:
            df (pd.DataFrame): Input DataFrame.
        
        Returns:
            Dict[str, Any]: Dictionary containing outlier counts for each numerical column.
        """
        numerical_cols = df.select_dtypes(include=["number"]).columns
        if len(numerical_cols) == 0:
            return {}
        
        outliers = {}
        for col in numerical_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outlier_mask = (df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))
            outliers[col] = int(outlier_mask.sum())  # Convert to int
        return {"outliers": outliers}

    @staticmethod
    def analyze_categorical_data(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze categorical columns by calculating value counts and unique values.
        
        Args:
            df (pd.DataFrame): Input DataFrame.
        
        Returns:
            Dict[str, Any]: Dictionary containing value counts and unique values for each categorical column.
        """
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns
        if len(categorical_cols) == 0:
            return {}
        
        analysis = {}
        for col in categorical_cols:
            analysis[col] = {
                "value_counts": df[col].value_counts().to_dict(),  # Convert Series to dict
                "unique_values": int(df[col].nunique()),  # Convert to int
            }
        return analysis