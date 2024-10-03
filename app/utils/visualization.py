# visualization.py
import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots


class DataVisualizer:
    def __init__(self, data_dict):
        self.data_dict = data_dict

    def display_selected_data(self):
        intervals = list(self.data_dict.keys())
        selected_interval = st.selectbox("Select Interval", intervals)
        data = self.data_dict[selected_interval]

        st.subheader(f"{selected_interval} Interval Data")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Sample of Analyzed Data (Head):")
            st.dataframe(data.head())
        with col2:
            st.write("Sample of Analyzed Data (Tail):")
            st.dataframe(data.tail())

        self.plot_closing_prices(data, selected_interval)
        self.display_basic_statistics(data)

    def plot_closing_prices(self, data, selected_interval):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['close'], mode='lines', name='Closing Price'))
        fig.update_layout(
            title=f"{selected_interval} Interval Closing Prices",
            xaxis_title="Time",
            yaxis_title="Price (INR)",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

    def display_basic_statistics(self, data):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Basic Statistics")
            st.write(data.describe())
        with col2:
            st.subheader("Dataset Information")
            st.write(f"Total number of records: {len(data)}")
            st.write(f"Date range: from {data.index.min()} to {data.index.max()}")
            st.write(f"Columns in the dataset: {', '.join(data.columns)}")

    def create_multi_timeframe_chart(self):
        st.subheader("Multi-Timeframe Comparison")
        fig = make_subplots(rows=3, cols=2, subplot_titles=list(self.data_dict.keys()), shared_xaxes=True, vertical_spacing=0.1)

        # Add traces for each timeframe
        for i, (interval, data) in enumerate(self.data_dict.items()):
            row = i // 2 + 1
            col = i % 2 + 1
            daily_data = data['close'].resample('D').last()
            fig.add_trace(go.Scatter(x=daily_data.index, y=daily_data, mode='lines', name=interval), row=row, col=col)
            fig.update_xaxes(title_text="Date", row=row, col=col)
            fig.update_yaxes(title_text="Price (INR)", row=row, col=col)
        fig.update_layout(height=900, width=1000, title_text="BTCINR Closing Prices Across Different Timeframes")
        st.plotly_chart(fig, use_container_width=True)
        self.display_trend_analysis()

    def display_trend_analysis(self):
        st.write("### Trend Analysis")
        col1, col2, col3 = st.columns(3)
        with col1:    
            st.write("#### Short-term (5m, 15m):")
            st.write("""
            - Highly volatile with rapid price fluctuations
            - Potential for scalping strategies
            - Requires real-time analysis and quick decision making
            """)
        with col2:   
            st.write("#### Medium-term (30m, 1h):")
            st.write("""
            - Shows an overall upward trend with significant oscillations
            - Suitable for intraday trading strategies
            - Allows for more considered entry and exit points
            """)
        with col3:
            st.write("#### Long-term (6h, 12h):")
            st.write("""
            - Reveals broader cyclical patterns
            - Ideal for swing trading strategies
            - Helps in identifying major support and resistance levels
            """)


