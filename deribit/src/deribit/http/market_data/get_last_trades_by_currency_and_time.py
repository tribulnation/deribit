# deribit/http/market_data/get_last_trades_by_currency_and_time.py

from deribit.http.client import Client
from .get_last_trades_by_currency import Result

class GetLastTradesByCurrencyAndTime:
  client: Client

  async def get_last_trades_by_currency_and_time(self, currency: str, start_timestamp: int, end_timestamp: int, **params):
    r = await self.client.get('public/get_last_trades_by_currency_and_time', params={
      'currency': currency,
      'start_timestamp': start_timestamp,
      'end_timestamp': end_timestamp,
      **params
    })
    return Result.model_validate(r.result)
