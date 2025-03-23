import pytest
import pytest_asyncio
from dataclasses import dataclass
from typing import List, TypedDict, Literal
from dotenv import load_dotenv
from deribit.http.client import AuthedClient
from ..market_data import MarketData
from . import Trading
from .buy import LimitOrderParams, TriggerOrderParams, TriggerLimitOrderParams

load_dotenv()

# Price constant for testing
BTC_PRICE = 85000

@dataclass
class Instruments:
  future: list[str]
  option: list[str]

  @property
  def all(self):
    return self.future + self.option + self.spot

@pytest.fixture(scope='module')
def clients() -> List[Trading]:
  return [
    Trading(AuthedClient.oauth2(testnet=True)),
    Trading(AuthedClient.hmac(testnet=True))
  ]


@pytest_asyncio.fixture(scope='module')
async def btc_instruments():
  # Get all BTC instruments
  client = MarketData()
  futures = await client.get_instruments('BTC', kind='future')
  options = await client.get_instruments('BTC', kind='option')
  
  mid = lambda xs: xs[len(xs) // 2]
  return Instruments(
    future=[mid(futures).instrument_name],
    option=[mid(options).instrument_name],
  )

# === Limit Order Tests ===

@pytest.mark.asyncio
async def test_buy_limit_spot(clients: List[Trading], btc_instruments: Instruments):
  for client in clients:
    params: LimitOrderParams = {
      "instrument_name": 'BTC_USDC',
      "type": "limit",
      "price": BTC_PRICE,
      "amount": 0.01,
    }
    result = await client.buy(params)
    assert result.order is not None

@pytest.mark.asyncio
async def test_buy_limit_future(clients: List[Trading], btc_instruments: Instruments):
  for client in clients:
    params: LimitOrderParams = {
      "instrument_name": btc_instruments.future[0],
      "type": "limit",
      "price": BTC_PRICE,
      "amount": 10,
    }
    result = await client.buy(params)
    assert result.order is not None

@pytest.mark.asyncio
async def test_buy_limit_option(clients: List[Trading], btc_instruments: Instruments):
  for client in clients:
    params: LimitOrderParams = {
      "instrument_name": btc_instruments.option[0],
      "type": "limit",
      "price": 0.1,
      "amount": 0.1,
    }
    result = await client.buy(params)
    assert result.order is not None

# === Market Order Tests ===

@pytest.mark.asyncio
async def test_buy_market_spot(clients: List[Trading], btc_instruments: Instruments):
  for client in clients:
    params: LimitOrderParams = {
      "instrument_name": 'BTC_USDC',
      "type": "market",
      "price": BTC_PRICE,
      "amount": 0.1,
    }
    result = await client.buy(params)
    assert result.order is not None

@pytest.mark.asyncio
async def test_buy_market_future(clients: List[Trading], btc_instruments: Instruments):
  for client in clients:
    params: LimitOrderParams = {
      "instrument_name": btc_instruments.future[0],
      "type": "market",
      "price": BTC_PRICE,
      "amount": 10,
    }
    result = await client.buy(params)
    assert result.order is not None

@pytest.mark.asyncio
async def test_buy_market_option(clients: List[Trading], btc_instruments: Instruments):
  for client in clients:
    params: LimitOrderParams = {
      "instrument_name": btc_instruments.option[0],
      "type": "market",
      "price": 0.1,
      "amount": 1,
    }
    result = await client.buy(params)
    assert result.order is not None

# === Stop Order Tests ===

@pytest.mark.asyncio
async def test_buy_stop_market(clients: List[Trading], btc_instruments: Instruments):
  for client in clients:
    params: TriggerOrderParams = {
      "instrument_name": btc_instruments.future[0],
      "type": "stop_market",
      "amount": 10,
      "trigger_price": BTC_PRICE * 1.1,
      "trigger": "last_price",
    }
    result = await client.buy(params)
    assert result.order is not None

@pytest.mark.asyncio
async def test_buy_stop_limit(clients: List[Trading], btc_instruments: Instruments):
  for client in clients:
    params: TriggerLimitOrderParams = {
      "instrument_name": btc_instruments.future[0],
      "type": "stop_limit",
      "price": BTC_PRICE * 1.1,
      "amount": 10,
      "trigger_price": BTC_PRICE * 1.05,
      "trigger": "last_price",
    }
    result = await client.buy(params)
    assert result.order is not None

# === Take Order Tests ===

@pytest.mark.asyncio
async def test_buy_take_market(clients: List[Trading], btc_instruments: Instruments):
  for client in clients:
    params: TriggerOrderParams = {
      "instrument_name": btc_instruments.future[0],
      "type": "take_market",
      "amount": 10,
      "trigger_price": BTC_PRICE * 0.9,
      "trigger": "last_price",
    }
    result = await client.buy(params)
    assert result.order is not None

@pytest.mark.asyncio
async def test_buy_take_limit(clients: List[Trading], btc_instruments: Instruments):
  for client in clients:
    params: TriggerLimitOrderParams = {
      "instrument_name": btc_instruments.future[0],
      "type": "take_limit",
      "price": BTC_PRICE * 0.9,
      "amount": 10,
      "trigger_price": BTC_PRICE * 0.95,
      "trigger": "last_price",
    }
    result = await client.buy(params)
    assert result.order is not None

# === Trailing Stop Tests ===

@pytest.mark.asyncio
async def test_buy_trailing_stop(clients: List[Trading], btc_instruments: Instruments):
  for client in clients:
    params: TriggerOrderParams = {
      "instrument_name": btc_instruments.future[0],
      "type": "trailing_stop",
      "amount": 10,
      "trigger_offset": 50,
      "trigger": "index_price",
      "trigger_price": BTC_PRICE,
    }
    result = await client.buy(params)
    assert result.order is not None

# === Additional Parameter Tests ===

@pytest.mark.asyncio
async def test_buy_with_time_in_force(clients: List[Trading], btc_instruments: Instruments):
  for client in clients:
    params: LimitOrderParams = {
      "instrument_name": btc_instruments.future[0],
      "type": "limit",
      "price": BTC_PRICE,
      "amount": 10,
      "time_in_force": "good_til_day",
    }
    result = await client.buy(params)
    assert result.order is not None

@pytest.mark.asyncio
async def test_buy_with_post_only(clients: List[Trading], btc_instruments: Instruments):
  for client in clients:
    params: LimitOrderParams = {
      "instrument_name": btc_instruments.future[0],
      "type": "limit",
      "price": BTC_PRICE,
      "amount": 10,
      "post_only": True,
    }
    result = await client.buy(params)
    assert result.order is not None

