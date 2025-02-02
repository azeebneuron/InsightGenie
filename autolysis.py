# /// script
# requires-python = ">=3.7"
# dependencies = [
#   "pandas",
#   "seaborn",
#   "matplotlib",
#   "httpx",
#   "chardet",
#   "python-dotenv",
#   "scikit-learn",
#   "scipy",
#   "numpy",
#   "networkx",
#   "streamlit",
# ]
# ///

import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import httpx
import chardet
from dotenv import load_dotenv
import json
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import networkx as nx
from scipy import stats

# Load environment variables
load_dotenv()

# Constants with enhanced configuration
API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
AIPROXY_TOKEN = os.getenv('AIPROXY_TOKEN')
VISION_SYSTEM_PROMPT = """You are an expert data visualization analyst. Analyze the provided charts 
and extract key insights that would be valuable for business decisions."""

def create_output_directory(file_name):
    """Create output directory for dataset if it doesn't exist."""
    dir_name = os.path.splitext(os.path.basename(file_name))[0]
    os.makedirs(dir_name, exist_ok=True)
    return dir_name

def detect_data_type(df):
    """Intelligently detect and categorize data types for analysis."""
    type_info = {
        'numeric': df.select_dtypes(include=['number']).columns.tolist(),
        'categorical': df.select_dtypes(include=['object', 'category']).columns.tolist(),
        'temporal': [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
    }
    return type_info

def advanced_analysis(df, data_types):
    """Perform comprehensive data analysis based on detected data types."""
    analysis = {
        'summary': df.describe(include='all').to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'outliers': {},
        'patterns': {}
    }
    
    # Outlier detection using IQR for numeric columns
    for col in data_types['numeric']:
        if df[col].notna().any():  # Only process if column has non-null values
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)][col]
            analysis['outliers'][col] = len(outliers)

    # Clustering for numeric columns (with handling for missing values)
    if len(data_types['numeric']) >= 2:
        try:
            # Select numeric columns and handle missing values
            numeric_df = df[data_types['numeric']].copy()
            
            # Fill missing values with column means
            numeric_df = numeric_df.fillna(numeric_df.mean())
            
            # Only proceed if we have valid data after cleaning
            if not numeric_df.empty and numeric_df.notna().all().all():
                scaler = StandardScaler()
                scaled_data = scaler.fit_transform(numeric_df)
                
                # Determine number of clusters (min of 3 or 1/3 of dataset size)
                n_clusters = min(3, max(2, len(df) // 3))
                
                kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                clusters = kmeans.fit_predict(scaled_data)
                
                analysis['clusters'] = {
                    'labels': clusters.tolist(),
                    'centers': kmeans.cluster_centers_.tolist(),
                    'features_used': data_types['numeric']
                }
        except Exception as e:
            print(f"Warning: Clustering analysis failed: {e}")
            analysis['clusters'] = {}

    # Pattern detection
    for col in data_types['numeric']:
        if df[col].notna().any():  # Only process if column has non-null values
            # Get non-null values and their indices
            valid_data = df[col].dropna()
            if len(valid_data) > 1:  # Need at least 2 points for trend analysis
                try:
                    trend = stats.linregress(range(len(valid_data)), valid_data)
                    analysis['patterns'][col] = {
                        'trend_slope': trend.slope,
                        'trend_pvalue': trend.pvalue
                    }
                except Exception as e:
                    print(f"Warning: Pattern analysis failed for {col}: {e}")
                    analysis['patterns'][col] = {}

    return analysis

def create_innovative_visualizations(df, data_types, output_dir):
    """Generate creative and informative visualizations with metadata."""
    viz_metadata = []
    
    # Enhanced distribution plots with statistical annotations
    for col in data_types['numeric'][:2]:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[col].dropna(), kde=True)
        mean_val = df[col].mean()
        median_val = df[col].median()
        plt.axvline(mean_val, color='r', linestyle='--', label=f'Mean: {mean_val:.2f}')
        plt.axvline(median_val, color='g', linestyle='--', label=f'Median: {median_val:.2f}')
        plt.title(f'Distribution Analysis of {col}')
        plt.legend()
        
        file_path = os.path.join(output_dir, f'enhanced_distribution_{col}.png')
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        # Store metadata about the visualization
        metadata = {
            'file_name': os.path.basename(file_path),
            'type': 'distribution',
            'variable': col,
            'statistics': {
                'mean': mean_val,
                'median': median_val,
                'std': df[col].std(),
                'skew': df[col].skew()
            }
        }
        viz_metadata.append(metadata)

    # Network visualization for correlations
    if len(data_types['numeric']) > 1:
        corr_matrix = df[data_types['numeric']].corr()
        
        # Create correlation heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Correlation Analysis')
        
        file_path = os.path.join(output_dir, 'correlation_heatmap.png')
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        # Store metadata about correlations
        metadata = {
            'file_name': os.path.basename(file_path),
            'type': 'correlation',
            'strong_correlations': [
                {
                    'variables': [col1, col2],
                    'correlation': corr_matrix.loc[col1, col2]
                }
                for col1 in corr_matrix.columns
                for col2 in corr_matrix.columns
                if col1 < col2 and abs(corr_matrix.loc[col1, col2]) > 0.5
            ]
        }
        viz_metadata.append(metadata)

    return viz_metadata


def generate_enhanced_narrative(analysis, viz_metadata, dataset_name, data_types):
    """Generate an engaging narrative using metadata from visualizations."""
    
    # Safely get row count from analysis
    # Fix the float length issue by getting the first numeric column's count
    row_count = 0
    if analysis['summary']:
        first_col = next(iter(analysis['summary']))
        if 'count' in analysis['summary'][first_col]:
            row_count = int(analysis['summary'][first_col]['count'])
    
    # Prepare a comprehensive context for the LLM
    context = {
        'dataset': {
            'name': dataset_name,
            'data_types': data_types,
            'rows': row_count
        },
        'analysis': {
            'missing_values': analysis['missing_values'],
            'outliers': analysis.get('outliers', {}),
            'patterns': analysis.get('patterns', {})
        },
        'visualizations': viz_metadata
    }

    narrative_prompt = f"""Create an engaging and insightful analysis report for the {dataset_name} dataset.

Dataset Overview:
- Name: {dataset_name}
- Total Records: {row_count}
- Data Types: {json.dumps(data_types, indent=2)}

Visualizations Created:
{json.dumps(viz_metadata, indent=2)}

Key Analysis Points:
1. Distribution Analysis:
{json.dumps([viz for viz in viz_metadata if viz['type'] == 'distribution'], indent=2)}

2. Correlation Analysis:
{json.dumps([viz for viz in viz_metadata if viz['type'] == 'correlation'], indent=2)}

3. Additional Insights:
- Outliers: {json.dumps(context['analysis']['outliers'], indent=2)}
- Patterns: {json.dumps(context['analysis']['patterns'], indent=2)}

Please create a comprehensive markdown report that includes:
1. Executive Summary
2. Detailed Analysis of Distributions and Correlations
3. Key Findings and Patterns
4. Strategic Recommendations

For each visualization, reference it using the format: ![Description](./filename.png)
Make sure to highlight significant patterns, unusual findings, and actionable insights."""

    try:
        headers = {
            'Authorization': f'Bearer {AIPROXY_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert data analyst creating engaging and insightful reports. Focus on clear explanations and actionable insights."
                },
                {
                    "role": "user",
                    "content": narrative_prompt
                }
            ],
            "temperature": 0.7
        }
        
        response = httpx.post(API_URL, headers=headers, json=payload, timeout=30.0)
        
        if response.status_code == 200:
            narrative = response.json()['choices'][0]['message']['content']
            return narrative
        else:
            print(f"API Error: {response.text}")
            return create_fallback_narrative(dataset_name, analysis, [vm['file_name'] for vm in viz_metadata])
            
    except Exception as e:
        print(f"Error in narrative generation: {e}")
        return create_fallback_narrative(dataset_name, analysis, [vm['file_name'] for vm in viz_metadata])


def call_llm(prompt, instruction, functions=None):
    """Helper function for LLM API calls with error handling."""
    headers = {
        'Authorization': f'Bearer {AIPROXY_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert data analyst creating engaging and insightful reports."
            },
            {
                "role": "user",
                "content": f"{instruction}\n\n{prompt}"
            }
        ],
        "temperature": 0.7
    }
    
    if functions:
        payload["functions"] = functions
    
    try:
        response = httpx.post(API_URL, headers=headers, json=payload, timeout=30.0)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        raise Exception(f"API returned status code {response.status_code}")
    except Exception as e:
        print(f"Error in LLM call: {e}")
        return f"Error generating {instruction.lower()}"

def create_fallback_narrative(dataset_name, analysis, visualization_files):
    """Create a basic narrative when LLM fails."""
    # Safely get row count
    row_count = 0
    if analysis['summary']:
        first_col = next(iter(analysis['summary']))
        if 'count' in analysis['summary'][first_col]:
            row_count = int(analysis['summary'][first_col]['count'])

    return f"""# Analysis Report for {dataset_name}

## Executive Summary
This report presents a comprehensive analysis of the {dataset_name} dataset, containing {row_count} records.

## Visualizations and Analysis
{chr(10).join([f'![Analysis of {viz}](./{viz})' for viz in visualization_files])}

## Key Statistical Findings
- Missing Values: {json.dumps(analysis['missing_values'], indent=2)}
- Outliers Detected: {json.dumps(analysis.get('outliers', {}), indent=2)}
- Patterns Identified: {json.dumps(analysis.get('patterns', {}), indent=2)}

## Recommendations
1. Review identified patterns for business insights
2. Investigate outliers for potential data quality issues
3. Consider deeper analysis of strongly correlated variables

*Note: This is an automated analysis report. Please review visualizations and statistics for detailed insights.*"""

def process_file(file_path):
    """Process a single CSV file with enhanced error handling and logging."""
    try:
        output_dir = create_output_directory(file_path)
        print(f"Processing {file_path} in directory: {output_dir}")
        
        df = pd.read_csv(file_path, encoding=detect_encoding(file_path))
        data_types = detect_data_type(df)
        
        analysis = advanced_analysis(df, data_types)
        visualizations = create_innovative_visualizations(df, data_types, output_dir)
        
        narrative = generate_enhanced_narrative(
            analysis, 
            visualizations,
            os.path.basename(file_path),
            data_types
        )
        
        with open(os.path.join(output_dir, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(narrative)
        
        return True
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def detect_encoding(file_path):
    """Detect file encoding using chardet."""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def main():
    if len(sys.argv) != 2:
        print("Usage: uv run autolysis.py <csv_file>")
        return
    
    csv_file = sys.argv[1]
    if not os.path.exists(csv_file):
        print(f"Error: File {csv_file} not found")
        return
    
    if process_file(csv_file):
        print("Analysis completed successfully!")
    else:
        print("Analysis failed. Please check the error messages above.")

if __name__ == "__main__":
    main()