import streamlit as st
import pandas as pd
from .base_service import BaseService


class BitcoinChartService(BaseService):
    def __init__(self, file_path="bitcoin_data.csv", chart_title="Bitcoin Weekly Data"):
        self.default_file_path = file_path
        self.default_chart_title = chart_title

    def execute(self, file_path=None, chart_title=None):
        """Generate and display a Bitcoin chart based on CSV data."""
        file_path = file_path or self.default_file_path
        chart_title = chart_title or self.default_chart_title

        st.sidebar.title(chart_title)
        st.write(f"# {chart_title}")

        # Control panel
        file_path = st.sidebar.text_input("CSV File Path", file_path)
        chart_title = st.sidebar.text_input("Chart Title", chart_title)

        try:
            df = pd.read_csv(file_path)
            if "Date" not in df.columns:
                st.error("The CSV file must contain a 'Date' column.")
                return

            df["Date"] = pd.to_datetime(df["Date"])
            df = df.set_index("Date")

            y_columns = [col for col in df.columns if col != "Date"]
            if not y_columns:
                st.error("The CSV must have at least one non-'Date' column.")
                return

            selected_columns = st.multiselect("Select Columns to Plot", y_columns, default=y_columns[:1])
            chart_type = st.selectbox("Chart Type", ["Line", "Area", "Bar"])

            if selected_columns:
                if chart_type == "Line":
                    st.line_chart(df[selected_columns])
                elif chart_type == "Area":
                    st.area_chart(df[selected_columns])
                elif chart_type == "Bar":
                    st.bar_chart(df[selected_columns])

        except FileNotFoundError:
            st.error(f"File not found: {file_path}")
        except Exception as e:
            st.error(f"An error occurred: {e}")