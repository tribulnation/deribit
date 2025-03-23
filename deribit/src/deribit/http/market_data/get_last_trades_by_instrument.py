# deribit/http/market_data/get_last_trades_by_instrument.py

from deribit.http.client import Client
from .get_last_trades_by_currency import Result

class GetLastTradesByInstrument:
  client: Client

  async def get_last_trades_by_instrument(self, instrument_name: str, **params):
    r = await self.client.get('public/get_last_trades_by_instrument', params={'instrument_name': instrument_name, **params})
    return Result.model_validate(r.result)
