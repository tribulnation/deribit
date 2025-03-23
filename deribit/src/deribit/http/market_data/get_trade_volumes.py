# deribit/http/market_data/get_trade_volumes.py

from pydantic import BaseModel
from deribit.http.client import Client

class TradeVolume(BaseModel):
  currency: str
  calls_volume: float
  calls_volume_7d: float | None = None
  calls_volume_30d: float | None = None
  puts_volume: float
  puts_volume_7d: float | None = None
  puts_volume_30d: float | None = None
  futures_volume: float
  futures_volume_7d: float | None = None
  futures_volume_30d: float | None = None
  spot_volume: float
  spot_volume_7d: float | None = None
  spot_volume_30d: float | None = None

class GetTradeVolumes:
  client: Client

  async def get_trade_volumes(self, extended: bool = False) -> list[TradeVolume]:
    r = await self.client.get('public/get_trade_volumes', params={'extended': extended})
    return [TradeVolume.model_validate(x) for x in r.result]
