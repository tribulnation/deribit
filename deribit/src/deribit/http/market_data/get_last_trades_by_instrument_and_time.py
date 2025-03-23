# deribit/http/market_data/get_last_trades_by_instrument_and_time.py

from deribit.http.client import Client
from .get_last_trades_by_currency import Result

class GetLastTradesByInstrumentAndTime:
  client: Client

  async def get_last_trades_by_instrument_and_time(self, instrument_name: str, start_timestamp: int, end_timestamp: int, **params):
    r = await self.client.get('public/get_last_trades_by_instrument_and_time', params={
      'instrument_name': instrument_name,
      'start_timestamp': start_timestamp,
      'end_timestamp': end_timestamp,
      **params
    })
    return Result.model_validate(r.result)
