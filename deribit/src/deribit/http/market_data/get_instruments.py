# deribit/http/market_data/get_instruments.py

from typing import Literal
from pydantic import RootModel
from deribit.http.client import Client
from .get_instrument import InstrumentInfo

Currency = Literal['BTC', 'ETH', 'USDC', 'USDT', 'EURR', 'any']
Kind = Literal['future', 'option', 'spot', 'future_combo', 'option_combo']

class InstrumentsResponse(RootModel):
  root: list[InstrumentInfo]

class GetInstruments:
  client: Client

  async def get_instruments(self, currency: Currency, kind: Kind | None = None, expired: bool = False):
    params = {'currency': currency, 'expired': expired}
    if kind is not None:
      params['kind'] = kind
    r = await self.client.get('public/get_instruments', params=params)
    return InstrumentsResponse.model_validate(r.result).root
