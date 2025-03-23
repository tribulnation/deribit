# deribit/http/market_data/get_tradingview_chart_data.py

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

class GetTradingViewChartData:
  client: Client

  async def get_tradingview_chart_data(self, instrument_name: str, start_timestamp: int, end_timestamp: int, resolution: str) -> TradingViewChart:
    r = await self.client.get('public/get_tradingview_chart_data', params={
      'instrument_name': instrument_name,
      'start_timestamp': start_timestamp,
      'end_timestamp': end_timestamp,
      'resolution': resolution,
    })
    return TradingViewChart.model_validate(r.result)
