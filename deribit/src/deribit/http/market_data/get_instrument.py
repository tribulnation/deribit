# deribit/http/market_data/get_instrument.py

from pydantic import BaseModel, RootModel
from decimal import Decimal
from deribit.http.client import Client

class TickSizeStep(BaseModel):
  above_price: Decimal
  tick_size: Decimal

class InstrumentInfo(BaseModel):
  base_currency: str
  block_trade_commission: Decimal
  block_trade_min_trade_amount: Decimal
  block_trade_tick_size: Decimal
  contract_size: int
  counter_currency: str
  creation_timestamp: int
  expiration_timestamp: int | None = None
  future_type: str | None = None
  instrument_id: int
  instrument_name: str
  instrument_type: str
  is_active: bool
  kind: str
  maker_commission: Decimal
  max_leverage: int | None = None
  max_liquidation_commission: Decimal | None = None
  min_trade_amount: Decimal
  option_type: str | None = None
  price_index: str
  quote_currency: str
  rfq: bool
  settlement_currency: str | None = None
  settlement_period: str | None = None
  strike: Decimal | None = None
  taker_commission: Decimal
  tick_size: Decimal
  tick_size_steps: list[TickSizeStep] | None = None

class InstrumentResponse(RootModel):
  root: InstrumentInfo

class GetInstrument:
  client: Client

  async def get_instrument(self, instrument_name: str):
    r = await self.client.get('public/get_instrument', params={'instrument_name': instrument_name})
    return InstrumentResponse.model_validate(r.result).root


