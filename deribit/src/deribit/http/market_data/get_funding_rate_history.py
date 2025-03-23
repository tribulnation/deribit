# deribit/http/market_data/get_funding_rate_history.py

from decimal import Decimal
from pydantic import BaseModel, RootModel
from deribit.http.client import Client

class FundingRateEntry(BaseModel):
  index_price: Decimal
  interest_1h: Decimal
  interest_8h: Decimal
  prev_index_price: Decimal
  timestamp: int

class FundingRateHistory(RootModel):
  root: list[FundingRateEntry]

class GetFundingRateHistory:
  client: Client

  async def get_funding_rate_history(self, instrument_name: str, start_timestamp: int, end_timestamp: int):
    params = {
      'instrument_name': instrument_name,
      'start_timestamp': start_timestamp,
      'end_timestamp': end_timestamp
    }
    r = await self.client.get('public/get_funding_rate_history', params=params)
    return FundingRateHistory.model_validate(r.result).root