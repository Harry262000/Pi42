
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose
from plotly.subplots import make_subplots


class EDA:
    def __init__(self, data_dict, selected_interval):
        self.data_dict = data_dict
        self.selected_interval = selected_interval
        self.df = self.data_dict[self.selected_interval]

    def price_trend(self):
        st.subheader("Price Trend")
        plt.figure(figsize=(12, 6))
        plt.plot(self.df['close'], label='Close Price', color='blue')
        plt.title(f'{self.selected_interval} Close Price Trend')
        plt.xlabel('Date')
        plt.ylabel('Price (INR)')
        plt.legend()
        st.pyplot(plt)

    def correlation_heatmap(self):
        st.subheader("Correlation Heatmap")
        correlation = self.df.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation, annot=True, fmt=".2f", cmap='coolwarm')
        plt.title("Correlation Heatmap")
        st.pyplot(plt)

    def price_distribution(self):
        st.subheader("Price Distribution")
        plt.figure(figsize=(10, 6))
        sns.histplot(self.df['close'], bins=30, kde=True, color='orange')
        plt.title("Distribution of Close Prices")
        plt.xlabel("Price (INR)")
        st.pyplot(plt)

    def price_change_analysis(self):
        self.df['price_change'] = self.df['close'] - self.df['open']
        mean_change = self.df['price_change'].mean()
        std_change = self.df['price_change'].std()

        fig = px.histogram(
            self.df,
            x='price_change',
            nbins=30,
            marginal="rug",
            title=f'Distribution of Daily Price Changes ({self.selected_interval})',
            labels={'price_change': 'Price Change (Close - Open)'},
            color_discrete_sequence=['blue']
        )
        fig.add_vline(x=mean_change, line_dash="dash", line_color="red",
                      annotation_text=f"Mean: {mean_change:.2f}", annotation_position="top left")
        fig.add_vline(x=mean_change + std_change, line_dash="dash", line_color="green",
                      annotation_text=f"Std Dev: {std_change:.2f}", annotation_position="top left")
        fig.add_vline(x=mean_change - std_change, line_dash="dash", line_color="green")

        st.plotly_chart(fig)

        st.write(f"**Mean Price Change**: {mean_change:.2f}")
        st.write(f"**Standard Deviation**: {std_change:.2f}")

    def plot_open_prices(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.df.index,
            y=self.df['open'],
            mode='lines',
            name='Open Price'
        ))
        fig.update_layout(
            title=f"Open Prices Over Time - {self.selected_interval} Interval",
            xaxis_title="Time",
            yaxis_title="Price",
            showlegend=False,
            margin=dict(l=50, r=30, t=50, b=50),
            template="plotly_white",
        )
        st.plotly_chart(fig)

    def volume_over_time(self):
        data_sorted = self.df.sort_values('endTime', ascending=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data_sorted['endTime'],
            y=data_sorted['volume'],
            mode='lines',
            name='Volume',
            line=dict(color='rgba(31, 119, 180, 1.0)'),
        ))
        fig.update_layout(
            title=f"Volume Over Time - {self.selected_interval} Interval",
            xaxis_title="End Time",
            yaxis_title="Volume",
            showlegend=False,
            margin=dict(l=50, r=30, t=50, b=50),
            template="plotly_white",
        )
        st.plotly_chart(fig)

    def moving_average_analysis(self):
        self.df['SMA_7'] = self.df['close'].rolling(window=7).mean()
        self.df['SMA_30'] = self.df['close'].rolling(window=30).mean()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.df.index, y=self.df['close'], mode='lines', name='Close Price'))
        fig.add_trace(go.Scatter(x=self.df.index, y=self.df['SMA_7'], mode='lines', name='7-Day SMA',
                                 line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=self.df.index, y=self.df['SMA_30'], mode='lines', name='30-Day SMA',
                                 line=dict(color='green')))
        fig.update_layout(
            title=f"SMA Analysis - {self.selected_interval} Interval",
            xaxis_title="End Time",
            yaxis_title="Price",
            showlegend=True,
            margin=dict(l=50, r=30, t=50, b=50),
            template="plotly_white",
        )
        st.plotly_chart(fig)

    def rsi_analysis(self):
        delta = self.df['close'].diff(1)
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        self.df['RSI'] = 100 - (100 / (1 + rs))

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.df.index, y=self.df['RSI'], mode='lines', name='RSI'))
        fig.update_layout(title='Relative Strength Index (RSI)', xaxis_title='Date', yaxis_title='RSI')
        st.plotly_chart(fig)

    def seasonal_decomposition(self):
        result = seasonal_decompose(self.df['close'], model='additive', period=30)
        fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.02)
        fig.add_trace(go.Scatter(x=self.df.index, y=result.observed, name='Observed'), row=1, col=1)
        fig.add_trace(go.Scatter(x=self.df.index, y=result.trend, name='Trend'), row=2, col=1)
        fig.add_trace(go.Scatter(x=self.df.index, y=result.seasonal, name='Seasonal'), row=3, col=1)
        fig.add_trace(go.Scatter(x=self.df.index, y=result.resid, name='Residual'), row=4, col=1)
        fig.update_layout(height=800, title='Seasonal Decomposition of Close Price')
        st.plotly_chart(fig)

    def run(self):
        self.price_trend()
        self.correlation_heatmap()
        self.price_distribution()
        self.price_change_analysis()
        self.plot_open_prices()
        self.volume_over_time()
        self.moving_average_analysis()
        self.rsi_analysis()
        self.seasonal_decomposition()
