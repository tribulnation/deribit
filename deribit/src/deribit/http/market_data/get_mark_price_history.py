# deribit/http/market_data/get_mark_price_history.py

from typing import Sequence
from pydantic import RootModel
from deribit.http.client import Client

class MarkPriceHistory(RootModel):
  root: Sequence[tuple[int, float]]

class GetMarkPriceHistory:
  client: Client

  async def get_mark_price_history(self, instrument_name: str, start_timestamp: int, end_timestamp: int):
    r = await self.client.get('public/get_mark_price_history', params={
      'instrument_name': instrument_name,
      'start_timestamp': start_timestamp,
      'end_timestamp': end_timestamp,
    })
    return MarkPriceHistory.model_validate(r.result).root
