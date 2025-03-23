# deribit/http/market_data/get_last_settlements_by_instrument.py

from deribit.http.market_data.get_last_settlements_by_currency import Settlement, Result
from deribit.http.client import Client

class GetLastSettlementsByInstrument:
  client: Client

  async def get_last_settlements_by_instrument(self, instrument_name: str, **params):
    r = await self.client.get('public/get_last_settlements_by_instrument', params={'instrument_name': instrument_name, **params})
    return Result.model_validate(r.result)
