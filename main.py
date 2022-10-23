"""
from tradingview_ta import TA_Handler, Interval, Exchange

handler = TA_Handler(
    symbol="ETHBUSD",
    exchange="binance",
    screener="crypto",
    interval="1h",
    timeout=None
)

analysis=handler.get_analysis().indicators


print(analysis)
"""


import requests
import json

url="https://cryptopanic.com/api/v1/posts/?auth_token=17d093c57021d47dad85e52ec1ac028d5a980727&public=true"
x=requests.get(url)
t=x.json()

