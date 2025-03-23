from typing import NamedTuple, Sequence, Literal
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, RootModel, TypeAdapter
from deribit.util import timestamp
from deribit.client import SocketClient, DERIBIT_MAINNET, DERIBIT_TESTNET

@dataclass
class MarketData:
  client: SocketClient = field(default_factory=SocketClient)

  @classmethod
  def new(cls, testnet: bool = False, timeout_secs: int | None = None, debug: bool = False):
    return cls(SocketClient(url=DERIBIT_TESTNET if testnet else DERIBIT_MAINNET, timeout_secs=timeout_secs, debug=debug))

  async def __aenter__(self):
    await self.client.__aenter__()
    return self

  async def __aexit__(self, *args):
    print('Exiting')
    await self.client.__aexit__(*args)

  class ContractSize(BaseModel):
    contract_size: Decimal

  async def get_contract_size(self, instrument: str):
    r = await self.client.request({
      'method': 'public/get_contract_size',
      'params': {'instrument_name': instrument}
    })
    return MarketData.ContractSize.model_validate(r).contract_size


  @dataclass
  class VolatilityEntry:
    time: datetime
    volatility: float

  class HistoricalVolatility(RootModel):
    root: Sequence[tuple[int, float]]

  async def get_historical_volatility(self, currency: str):
    r = await self.client.request({
      'method': 'public/get_historical_volatility',
      'params': {'currency': currency}
    })
    entries = MarketData.HistoricalVolatility.model_validate(r).root
    return [MarketData.VolatilityEntry(timestamp.parse(t), vol) for t, vol in entries]


  class IndexPrice(BaseModel):
    index_price: Decimal
    estimated_delivery_price: Decimal

  async def get_index_price(self, index_name: str):
    r = await self.client.request({
      'method': 'public/get_index_price',
      'params': {'index_name': index_name}
    })
    return MarketData.IndexPrice.model_validate(r)
  
  
  InstrumentKind = Literal['future', 'option', 'spot', 'future_combo', 'option_combo']
  class Instrument(BaseModel):
    model_config = ConfigDict(extra='allow')
    base_currency: str
    contract_size: Decimal
    counter_currency: str
    creation_timestamp: int
    expiration_timestamp: int
    is_active: bool
    kind: 'MarketData.InstrumentKind'
    maker_commission: Decimal
    min_trade_amount: Decimal
    quote_currency: str
    taker_commission: Decimal
    tick_size: Decimal
    instrument_name: str
    settlement_currency: str | None = None # anything but spot
    settlement_period: str | None = None # anything but spot
    @property
    def expiry(self):
      return timestamp.parse(self.expiration_timestamp)

  async def get_instrument(self, instrument: str):
    r = await self.client.request({
      'method': 'public/get_instrument',
      'params': {'instrument_name': instrument}
    })
    return MarketData.Instrument.model_validate(r)
  
  async def get_instruments(self, currency: str, *, kind: InstrumentKind | None = None, expired: bool = False):
    params: dict = {'currency': currency}
    if kind is not None:
      params['kind'] = kind
    if expired:
      params['expired'] = True
    r = await self.client.request({
      'method': 'public/get_instruments',
      'params': params
    })
    Instruments = TypeAdapter(list[MarketData.Instrument])
    return Instruments.validate_python(r)
  

  class Option(Instrument):
    option_type: Literal['call', 'put']
    strike: Decimal
  
  async def get_options(self, currency: str, *, expired: bool = False):
    params: dict = {'currency': currency, 'kind': 'option'}
    if expired:
      params['expired'] = True
    r = await self.client.request({
      'method': 'public/get_instruments',
      'params': params
    })
    Instruments = TypeAdapter(list[MarketData.Option])
    return Instruments.validate_python(r)
  

  class Order(NamedTuple):
    price: Decimal
    amount: Decimal

  class OrderBook(BaseModel):
    model_config = ConfigDict(extra='allow')
    asks: list['MarketData.Order']
    bids: list['MarketData.Order']
    best_ask_amount: Decimal
    best_ask_price: Decimal
    best_bid_amount: Decimal
    best_bid_price: Decimal
    index_price: Decimal
    last_price: Decimal | None
    mark_iv: Decimal
    mark_price: Decimal
  
  async def get_order_book(self, instrument: str, *, depth: int | None = None):
    params: dict = {'instrument_name': instrument}
    if depth is not None:
      params['depth'] = depth
    r = await self.client.request({
      'method': 'public/get_order_book',
      'params': params
    })
    return MarketData.OrderBook.model_validate(r)
  

  class OptionOrderBook(OrderBook):
    ask_iv: Decimal
    bid_iv: Decimal
    interest_rate: Decimal
  
  async def get_option_order_book(self, instrument: str, *, depth: int | None = None):
    params: dict = {'instrument_name': instrument}
    if depth is not None:
      params['depth'] = depth
    r = await self.client.request({
      'method': 'public/get_order_book',
      'params': params
    })
    return MarketData.OptionOrderBook.model_validate(r)