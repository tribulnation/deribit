# deribit/http/market_data/get_funding_rate_value.py

from decimal import Decimal
from pydantic import RootModel
from deribit.http.client import Client

class Result(RootModel):
  root: Decimal

class GetFundingRateValue:
  client: Client

  async def get_funding_rate_value(self, instrument_name: str, start_timestamp: int, end_timestamp: int) -> Decimal:
    params = {
      'instrument_name': instrument_name,
      'start_timestamp': start_timestamp,
      'end_timestamp': end_timestamp,
    }
    r = await self.client.get('public/get_funding_rate_value', params=params)
    return Result.model_validate(r.result).root


