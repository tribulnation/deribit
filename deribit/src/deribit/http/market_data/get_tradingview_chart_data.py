# deribit/http/market_data/get_tradingview_chart_data.py

from typing_extensions import Literal
from pydantic import BaseModel
from deribit.http.client import Client

class TradingViewChart(BaseModel):
  close: list[float]
  cost: list[float]
  high: list[float]
  low: list[float]
  open: list[float]
  status: str
  ticks: list[int]
  volume: list[float]

Resolution = Literal[
  '1',
  '3',
  '5',
  '10',
  '15',
  '30',
  '60',
  '120',
  '180',
  '360',
  '720',
  '1D',
]

class GetTradingViewChartData:
  client: Client

  async def get_tradingview_chart_data(self, instrument_name: str, start_timestamp: int, end_timestamp: int, resolution: Resolution) -> TradingViewChart:
    r = await self.client.get('public/get_tradingview_chart_data', params={
      'instrument_name': instrument_name,
      'start_timestamp': start_timestamp,
      'end_timestamp': end_timestamp,
      'resolution': resolution,
    })
    return TradingViewChart.model_validate(r.result)
