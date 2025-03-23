# deribit/http/market_data/get_currencies.py

from pydantic import BaseModel, RootModel
from deribit.http.client import Client

class WithdrawalPriority(BaseModel):
  name: str
  value: float

class Currency(BaseModel):
  coin_type: str
  currency: str
  currency_long: str
  fee_precision: int
  in_cross_collateral_pool: bool
  min_confirmations: int
  min_withdrawal_fee: float
  withdrawal_fee: float
  withdrawal_priorities: list[WithdrawalPriority]

class Currencies(RootModel):
  root: list[Currency]

class GetCurrencies:
  client: Client

  async def get_currencies(self):
    r = await self.client.get('public/get_currencies')
    return Currencies.model_validate(r.result).root