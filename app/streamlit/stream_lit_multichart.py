import streamlit as st
import pandas as pd
import altair as alt

@st.cache_data
def load_and_compute_pct(
    csv_data,
    date_col: str | None = None,
    value_col: str | None = None
) -> pd.DataFrame:
    """
    Load CSV data, auto-detect (or use provided) date & value columns,
    compute week-over-week percent change, and return a DataFrame indexed by date.
    """
    df = pd.read_csv(csv_data)
    cols = list(df.columns)

    # Detect date column if not provided
    if date_col is None:
        if 'Date' in cols:
            date_col = 'Date'
        else:
            date_candidates = [c for c in cols if 'date' in c.lower()]
            date_col = date_candidates[0] if date_candidates else cols[0]

    # Detect value column if not provided
    if value_col is None:
        if 'Close' in cols:
            value_col = 'Close'
        else:
            value_candidates = [c for c in cols if c.lower() in ('close','price','value','adj close')]
            value_col = value_candidates[0] if value_candidates else (cols[1] if len(cols)>1 else cols[0])

    # Keep only the two columns and drop missing values
    df = df[[date_col, value_col]].dropna()

    # Parse dates with UTC to handle timezones, then sort
    df[date_col] = pd.to_datetime(df[date_col], utc=True)
    df = df.set_index(date_col).sort_index()

    # Resample to weekly frequency and take last observation
    weekly = df.resample('W').last()

    # Compute week-over-week percent change
    pct = weekly[value_col].pct_change() * 100
    pct = pct.rename(f"{value_col}_pct_change")

    return pct.to_frame()


def main():
    st.title("Compare Weekly % Change of Two Series")
    st.markdown("""
    Upload two CSV files (each with at least a date column and a numeric value column).
    The app will compute the week-over-week percent change for each and display them together.
    """)
    
    # Sidebar for uploads
    st.sidebar.header("Upload CSVs")
    file1 = st.sidebar.file_uploader("First CSV", type="csv", key="csv1")
    file2 = st.sidebar.file_uploader("Second CSV", type="csv", key="csv2")

    if file1 and file2:
        # Compute percent-change series
        pct1 = load_and_compute_pct(file1)
        pct2 = load_and_compute_pct(file2)
        
        # Merge on date index
        merged = pd.concat([pct1, pct2], axis=1)
        merged.columns = ["Series 1 % change", "Series 2 % change"]
        merged = merged.dropna(how="any")

        st.subheader("Weekly Percent Change Comparison")

        # Prepare for Altair chart
        chart_data = merged.reset_index()
        chart_data.columns = ['date', 'Series 1 % change', 'Series 2 % change']

        # Build Altair chart with custom colors
        chart = alt.Chart(chart_data).transform_fold(
            ['Series 1 % change', 'Series 2 % change'],
            as_=['Series', 'Percent Change']
        ).mark_line(point=True).encode(
            x=alt.X('date:T', title='Date'),
            y=alt.Y('Percent Change:Q', title='Week-over-Week % Change'),
            color=alt.Color('Series:N', scale=alt.Scale(range=['#1f77b4', '#ff7f0e']))
        ).properties(
            width='container',
            height=400
        )

        st.altair_chart(chart, use_container_width=True)

        # Optional: show data table
        st.dataframe(merged)
    else:
        st.info("Please upload both CSV files in the sidebar to generate the chart.")


if __name__ == "__main__":
    main()

