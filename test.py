import streamlit as st
import pandas as pd

def plot_btc_data(csv_file_path, chart_title):
    """Plots BTC data from a CSV file with a specified chart title."""
    st.write(f"# {chart_title}")

    try:
        # Load data
        df = pd.read_csv(csv_file_path)

        # Ensure 'Date' column exists and is datetime type
        if "Date" not in df.columns:
            st.error("The CSV file must contain a 'Date' column.")
            return

        df["Date"] = pd.to_datetime(df["Date"])

        # Determine which column to plot on the Y-axis (other than Date)
        y_columns = [col for col in df.columns if col != "Date"]
        if not y_columns:
            st.error("The CSV file must contain at least one column besides 'Date' for plotting.")
            return

        # Plot using the first non-Date column by default
        y_column = y_columns[0]
        st.line_chart(df.set_index("Date")[y_column])

    except FileNotFoundError:
        st.error(f"File not found: {csv_file_path}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Example usage

if __name__ == "__main__":
    plot_btc_data("/workspaces/assistant/app/dummyapp/btc_weekly_start.csv", "Bitcoin Weekly Data Mapped")
