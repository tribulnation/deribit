# deribit/http/market_data/get_historical_volatility.py

from pydantic import RootModel
from deribit.http.client import Client

class HistoricalVolatility(RootModel):
  root: list[tuple[int, float]]

class GetHistoricalVolatility:
  client: Client

  async def get_historical_volatility(self, currency: str):
    r = await self.client.get('public/get_historical_volatility', params={'currency': currency})
    return HistoricalVolatility.model_validate(r.result).root


