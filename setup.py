import os
from setuptools import setup, find_packages

# Function to create the folder structure
def create_project_structure():
    
    # Defining the folder structure for the Streamlit project
    structure = {
        'data': {
            'raw/': '',
            'processed/': '',
            'historical/': '',
        },
        'streamlit_app': {
            'app.py': '# Main Streamlit app entry point',
            'pages': {
                'exploration.py': '# Data exploration and visualization',
                'indicators.py': '# Technical indicators and feature engineering',
                'forecasting_models.py': '# Model training and prediction',
                'backtesting.py': '# Backtesting and validation',
                'insights.py': '# Final insights and conclusions',
            },
            'utils': {
                'data_retrieval.py': '# Fetch data from Pi42 API/WebSocket',
                'EDA.py': '# Calculate technical indicators like MA, RSI',
                'forecasting_models.py': '# Model training and prediction functions',
                'backtesting.py': '# Backtesting strategy implementation',
                'visualization.py': '# Helper functions for charts using Matplotlib',
                'config.py': '# Configuration file for API keys and env variables',
            },
        },
        'reports': {
            'figures/': '# Storing charts for Streamlit display',
        },
        'tests': {
            'test_data_retrieval.py': '# Unit tests for data retrieval functionality',
            'test_feature_engineering.py': '# Unit tests for feature calculation',
        },
        'requirements.txt': '# Python dependencies',
        'README.md': '# Project overview and instructions',
        'config.py': '# Configuration for environment settings',
    }
    
    # Create the directories and files
    def create_structure(base_path, structure):
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):  # Directory
                os.makedirs(path, exist_ok=True)
                create_structure(path, content)
            else:  # File
                with open(path, 'w') as f:
                    f.write(content)
    
    create_structure(os.getcwd(), structure)

# Call the function to create the structure when the project is set up
create_project_structure()

# Setup for the project
setup(
    name='pi42_crypto_analysis',
    version='0.1.0',
    description='Cryptocurrency analysis using Streamlit and Pi42 API',
    author='Harshal Honde',
    author_email='Harshalhonde50@gmail.com',
    url='https://github.com/Harry262000/pi42_crypto_analysis',  # Update with your repository URL
    packages=find_packages(where='streamlit_app'),  # Find packages in the 'streamlit_app' folder
    package_dir={'': 'streamlit_app'},  # Tells setuptools to look for packages in 'streamlit_app'
    install_requires=[
        'streamlit',
        'pandas',
        'numpy',
        'scikit-learn',
        'matplotlib',
        'requests',
        'ta-lib',  # If using technical analysis indicators
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
