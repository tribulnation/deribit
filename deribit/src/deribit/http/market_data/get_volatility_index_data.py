# deribit/http/market_data/get_volatility_index_data.py

from typing_extensions import Literal
from pydantic import BaseModel
from deribit.http.client import Client

class VolatilityCandle(BaseModel):
  timestamp: int
  open: float
  high: float
  low: float
  close: float

class VolatilityResult(BaseModel):
  continuation: int | None = None
  data: list[VolatilityCandle]

Resolution = Literal[
  '1',
  '60',
  '3600',
  '43200',
  '1D',
]

class GetVolatilityIndexData:
  client: Client

  async def get_volatility_index_data(self, currency: str, start_timestamp: int, end_timestamp: int, resolution: Resolution) -> VolatilityResult:
    r = await self.client.get('public/get_volatility_index_data', params={
      'currency': currency,
      'start_timestamp': start_timestamp,
      'end_timestamp': end_timestamp,
      'resolution': resolution,
    })
    raw_data = r.result
    candles = [VolatilityCandle(timestamp=c[0], open=c[1], high=c[2], low=c[3], close=c[4]) for c in raw_data['data']]
    return VolatilityResult(continuation=raw_data.get('continuation'), data=candles)
