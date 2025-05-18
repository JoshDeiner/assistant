from app.schemas.schema import calc_tool
from app.schemas.schema import code_write_tool
from app.schemas.shell_schema import command_exec_tool
from app.schemas.crypto_currencies_schema import crypto_price_tool_schema
from app.schemas.crypto_currencies_schema import download_btc_data_tool
from app.schemas.yfinance_schema import stock_data_tool_schema


tools = [
    calc_tool,
    code_write_tool,
    crypto_price_tool_schema,
    command_exec_tool,
    download_btc_data_tool,
    stock_data_tool_schema
]