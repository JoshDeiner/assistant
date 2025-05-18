import os
from dotenv import load_dotenv
from app.clients.factory_clients import ApiClientFactory

# Load environment variables
load_dotenv()

def main():
    # Create a YFinance client for VOO
    voo_client = ApiClientFactory.get_client(
        "yfinance",
        ticker="VOO",
        period=os.getenv("PERIOD", "10y"),
        interval=os.getenv("INTERVAL_GRAPH", "1d"),
        csv_file_path="voo_data.csv"
    )
    
    # Get VOO data
    voo_status, voo_result = voo_client.fetch()
    if voo_status == 0:
        print(f"VOO data saved to: {voo_result['data']}")
    else:
        print(f"Error fetching VOO data: {voo_result['error']}")
    
    # Create a YFinance client for VTI
    vti_client = ApiClientFactory.get_client(
        "yfinance",
        ticker="VTI",
        period=os.getenv("PERIOD", "10y"),
        interval=os.getenv("INTERVAL_GRAPH", "1d"),
        csv_file_path="vti_data.csv"
    )
    
    # Get VTI data
    vti_status, vti_result = vti_client.fetch()
    if vti_status == 0:
        print(f"VTI data saved to: {vti_result['data']}")
    else:
        print(f"Error fetching VTI data: {vti_result['error']}")

if __name__ == "__main__":
    main()