import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("Agg")  # Use a non-interactive backend
import matplotlib.pyplot as plt
import httpx
import chardet
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Constants
API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
AIPROXY_TOKEN = os.getenv('AIPROXY_TOKEN')

def create_output_directory(file_name):
    """Create output directory for dataset if it doesn't exist."""
    dir_name = os.path.splitext(file_name)[0]
    os.makedirs(dir_name, exist_ok=True)
    return dir_name

def load_data(file_path):
    """Load CSV data with encoding detection."""
    try:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']
        return pd.read_csv(file_path, encoding=encoding)
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

def analyze_data(df):
    """Perform basic data analysis."""
    try:
        numeric_df = df.select_dtypes(include=['number'])
        analysis = {
            'summary': df.describe(include='all').to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'correlation': numeric_df.corr().to_dict() if not numeric_df.empty else {}
        }
        return analysis
    except Exception as e:
        print(f"Error in data analysis: {e}")
        raise

def visualize_data(df, output_dir):
    """Generate and save visualizations."""
    try:
        sns.set(style="whitegrid")
        plt.style.use('default')
        numeric_columns = df.select_dtypes(include=['number']).columns
        viz_paths = []

        # Distribution plots
        for column in numeric_columns[:3]:  # Limit to first 3 numeric columns
            plt.figure(figsize=(10, 6))
            sns.histplot(df[column].dropna(), kde=True)
            plt.title(f'Distribution of {column}')
            file_path = os.path.join(output_dir, f'distribution_{column}.png')
            plt.savefig(file_path, dpi=300, bbox_inches='tight')
            plt.close()
            viz_paths.append(file_path)

        # Correlation heatmap
        if len(numeric_columns) > 1:
            plt.figure(figsize=(12, 8))
            sns.heatmap(df[numeric_columns].corr(), annot=True, cmap='coolwarm', center=0)
            plt.title('Correlation Heatmap')
            file_path = os.path.join(output_dir, 'correlation_heatmap.png')
            plt.savefig(file_path, dpi=300, bbox_inches='tight')
            plt.close()
            viz_paths.append(file_path)

        return viz_paths
    except Exception as e:
        print(f"Error in visualization: {e}")
        raise

def generate_narrative(analysis, visualizations, dataset_name):
    """Generate narrative using LLM with correct API format."""
    headers = {
        'Authorization': f'Bearer {AIPROXY_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    # Update API URL to the working endpoint
    api_url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    
    # Prepare a simplified analysis summary
    summary = {
        'dataset_name': dataset_name,
        'total_rows': len(analysis['summary'].get('count', {})),
        'numeric_columns': list(analysis['correlation'].keys()),
        'missing_values_summary': {k: v for k, v in analysis['missing_values'].items() if v > 0},
        'visualizations': [os.path.basename(viz) for viz in visualizations]
    }
    
    prompt = f"""Create a detailed markdown analysis report for a dataset with the following information:

Dataset Name: {dataset_name}
Summary Statistics: {json.dumps(summary, indent=2)}

The following visualizations have been generated:
{chr(10).join(['- ' + os.path.basename(viz) for viz in visualizations])}

Please write a comprehensive markdown report that includes:
1. A clear introduction explaining the dataset
2. Analysis of key patterns and trends
3. Description of visualizations (use format: ![Description](./image_name.png))
4. Key findings and recommendations

Focus on making the insights actionable and meaningful. Make sure to reference all visualizations appropriately."""

    try:
        # Use the correct payload format that worked in our test
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert data analyst creating insightful, engaging reports with a focus on actionable insights and clear narrative flow."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        }

        print("Sending request to LLM API...")
        
        response = httpx.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=30.0
        )
        
        print(f"API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            
            # Fix image paths in the content
            for viz in visualizations:
                viz_name = os.path.basename(viz)
                content = content.replace(viz_name, f"./{viz_name}")
            
            return content
        else:
            print(f"API Error: {response.text}")
            raise Exception(f"API returned status code {response.status_code}")
            
    except Exception as e:
        print(f"Error in narrative generation: {e}")
        
        # Return fallback narrative
        return f"""# Data Analysis Report for {dataset_name}

## Dataset Overview
This analysis examines the dataset from {dataset_name}, which contains {summary['total_rows']} records.

## Visualizations and Analysis

### Distribution Analysis
We've analyzed the distribution of key numerical variables in the dataset. Below are the distribution plots:

{"".join([f'''
### Distribution of {os.path.basename(viz).replace('distribution_', '').replace('.png', '')}
![Distribution Analysis](./{os.path.basename(viz)})
''' for viz in visualizations if 'distribution' in viz])}

### Correlation Analysis
The correlation heatmap below shows the relationships between numerical variables:

![Correlation Heatmap](./correlation_heatmap.png)

## Key Findings
1. The dataset contains {len(summary['numeric_columns'])} numerical variables for analysis
2. {f"Missing values were found in: {', '.join(summary['missing_values_summary'].keys())}" if summary['missing_values_summary'] else "No missing values were detected in the dataset"}

## Recommendations
1. Further investigate any unusual patterns in the distributions shown above
2. Consider the correlations between variables for deeper analysis
3. {f"Address missing values in {len(summary['missing_values_summary'])} columns before detailed statistical analysis" if summary['missing_values_summary'] else "Proceed with detailed statistical analysis as data completeness is good"}

*Note: This is an automated analysis report. For more detailed insights, please examine the visualizations above carefully.*"""

def process_file(file_path):
    """Process a single CSV file."""
    try:
        # Create output directory
        output_dir = create_output_directory(os.path.basename(file_path))
        print(f"Created output directory: {output_dir}")
        
        # Load and analyze data
        print("Loading data...")
        df = load_data(file_path)
        print("Analyzing data...")
        analysis = analyze_data(df)
        
        # Generate visualizations
        print("Generating visualizations...")
        visualizations = visualize_data(df, output_dir)
        
        # Generate narrative
        print("Generating narrative...")
        narrative = generate_narrative(
            analysis, 
            visualizations, 
            os.path.basename(file_path)
        )
        
        # Save narrative
        readme_path = os.path.join(output_dir, 'README.md')
        print(f"Saving narrative to {readme_path}")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(narrative)
            
        print(f"Successfully processed {file_path}")
        return True
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

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