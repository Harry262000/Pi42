import streamlit as st
import os


class Roadmap:
    def __init__(self, items=None):
        """
        Initialize the Roadmap class with a list of items.

        Args:
        - items (list of tuples): A list of tuples containing the title and description of each roadmap item.
        """
        if items is None:
            # Default roadmap items
            items = [
                ("🔍 Data Retrieval API", "Fetch historical cryptocurrency data from reliable sources using APIs."),
                ("🧹 Data Preprocessing", "Clean, normalize, and prepare the raw data for analysis and modeling."),
                ("📊 Exploratory Data Analysis (EDA)", "Visualize and analyze data patterns, correlations, and trends."),
                ("📈 Technical Indicators",
                 "Calculate and incorporate relevant technical indicators for enhanced prediction."),
                ("🤖 Predictive Modeling",
                 "Develop and train machine learning models to forecast cryptocurrency prices."),
                ("🏆 Model Evaluation",
                 "Assess model performance using various metrics and cross-validation techniques."),
                ("🔄 Backtesting Strategy",
                 "Validate the model's effectiveness using historical data and simulated trading."),
                ("📚 Summary and Insights", "Compile findings, interpret results, and provide actionable insights.")
            ]
        self.items = items
        self.styles = """
        <style>
        .roadmap-item {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .roadmap-item h3 {
            color: #0e1117;
            font-size: 15px;
            margin-bottom: 10px;
        }
        .roadmap-item p {
            color: #262730;
            font-size: 12px;
        }
        </style>
        """

    def display_roadmap(self):
        """Display the roadmap items in the Streamlit app."""
        st.markdown(self.styles, unsafe_allow_html=True)  # Include styles in the app
        for title, description in self.items:
            st.markdown(f"<div class='roadmap-item'><h3>{title}</h3><p>{description}</p></div>", unsafe_allow_html=True)


class ProjectDescription:
    @staticmethod
    def get_description():
        """Returns a description of the cryptocurrency project."""
        return """
        In this project, I integrated the Pi42 API to fetch cryptocurrency market data and utilized WebSocket connections for real-time data streaming.

        1. **API Documentation Exploration**: I started by thoroughly reviewing the **Pi42 API documentation** to understand the available endpoints, request parameters, and response structures. This guided me in effectively constructing requests for historical market data.

        2. **Fetching Historical Data**: To gather historical price data for the cryptocurrency trading pair (e.g., BTC/INR), I implemented the `get_kline_data` function. This function allows me to specify various intervals (like 5 minutes, 15 minutes, 1 hour, etc.) and retrieve up to 10,000 data points since a defined starting timestamp. The data is fetched using a POST request to the `/v1/market/klines` endpoint, which returns candlestick data (also known as Kline data) essential for technical analysis.

        3. **WebSocket for Real-Time Data**: To complement the historical data, I established a connection to the Pi42 WebSocket API using the `connect_websocket` function. This function utilizes the `WebSocketApp` to listen for real-time market updates, enabling me to react to price changes instantaneously.

        4. **Data Storage**: The retrieved data is stored in CSV format using the `save_to_csv` function, ensuring easy access and further analysis.

        This dual approach of leveraging API for historical data and WebSocket for real-time updates allows for a comprehensive analysis of cryptocurrency market trends.
        """


class APIHandler:
    @staticmethod
    def display_api_code(file_path):
        """
        Display the content of a Python file with syntax highlighting in Streamlit.

        Args:
        - file_path (str): Path to the Python file that contains the API code.
        """
        st.write("You can view the complete API code in the following file:")

        # Create a button to trigger the file display
        if st.button('View API Code'):
            # Check if the file exists
            if os.path.exists(file_path):
                try:
                    # Open the Python script file
                    with open(file_path, 'r') as file:
                        code_content = file.read()
                    # Display the code with syntax highlighting
                    st.code(code_content, language='python')
                except Exception as e:
                    st.error(f"Error reading the file: {e}")
            else:
                st.error(f"Error: The file '{file_path}' does not exist.")
