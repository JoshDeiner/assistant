import subprocess
import yfinance as yf
import pandas as pd

def main():
    csv_file_path = "app/dummyapp/btc_weekly_start.csv"
    subprocess.run(
        ["rm",  csv_file_path],       # command and arguments as a list
        capture_output=True,              # capture stdout and stderr
        text=True,                        # decode bytes → str
        check=False                       # don’t raise on non-zero exit by default
    )
    # 1. Download daily BTC-USD data
    btc = yf.download(
        "BTC-USD",
        start="2013-01-01",
        end=pd.Timestamp.today().strftime("%Y-%m-%d"),
        interval="1d",
        progress=False
    )

    # 2. Ensure the index is datetime
    btc.index = pd.to_datetime(btc.index)

    # 3. Resample to weekly starts (weeks anchored on Monday) and take the first Close price
    weekly_start = btc["Close"].resample("W-MON").first()

    # 4b. (Optional) Also write to CSV
    weekly_start.to_csv(
        csv_file_path,
        header=["Close"]
    )

    print("Wrote weekly-start BTC prices to btc_weekly_start.json and btc_weekly_start.csv")

    # writing it into llm memory
    # os.system("cat btc_weekly_start.csv")

if __name__ == "__main__":
    main()
