from dataclasses import dataclass
import pytest
import pytest_asyncio
from . import MarketData

BTC_PRICE = 85000

@dataclass
class Instruments:
  future: list[str]
  option: list[str]
  spot: list[str]

  @property
  def all(self):
    return self.future + self.option + self.spot
  
  @property
  def non_spot(self):
    return self.future + self.option

@pytest.fixture(scope='module')
def client():
  return MarketData()

@pytest_asyncio.fixture(scope='module')
async def btc_instruments(client: MarketData):
  # Get all BTC instruments
  futures = await client.get_instruments('BTC', kind='future')
  options = await client.get_instruments('BTC', kind='option')
  spots = await client.get_instruments('BTC', kind='spot')
  
  return Instruments(
    future=[futures[0].instrument_name],
    option=[options[0].instrument_name],
    spot=[spots[0].instrument_name]
  )

@pytest.fixture
def timestamps():
  from datetime import datetime, timedelta
  from deribit.util import timestamp
  t1 = datetime.now()
  t0 = t1 - timedelta(days=1)
  return timestamp.dump(t0), timestamp.dump(t1)

@pytest.mark.asyncio
async def test_get_book_summary_by_currency(client: MarketData):
  result = await client.get_book_summary_by_currency('BTC')
  assert result is not None

@pytest.mark.asyncio
async def test_get_book_summary_by_instrument(client: MarketData, btc_instruments: Instruments):
  for instrument in btc_instruments.all:
    result = await client.get_book_summary_by_instrument(instrument)
    assert result is not None

@pytest.mark.asyncio
async def test_get_contract_size(client: MarketData, btc_instruments: Instruments):
  for instrument in btc_instruments.all:
    result = await client.get_contract_size(instrument)
    assert result is not None

@pytest.mark.asyncio
async def test_get_currencies(client: MarketData):
  result = await client.get_currencies()
  assert result is not None
  assert len(result) > 0

@pytest.mark.asyncio
async def test_get_delivery_prices(client: MarketData):
  result = await client.get_delivery_prices('btc_usd')
  assert result is not None

@pytest.mark.asyncio
async def test_get_expirations(client: MarketData):
  result = await client.get_expirations('BTC', 'any')
  assert result is not None

@pytest.mark.asyncio
async def test_get_funding_chart_data(client: MarketData):
  for interval in ('1m', '8h', '24h'):
    await client.get_funding_chart_data('BTC-PERPETUAL', interval)

@pytest.mark.asyncio
async def test_get_funding_rate_history(client: MarketData, timestamps):
  await client.get_funding_rate_history('BTC-PERPETUAL', timestamps[0], timestamps[1])

@pytest.mark.asyncio
async def test_get_funding_rate_value(client: MarketData, timestamps):
  await client.get_funding_rate_value('BTC-PERPETUAL', timestamps[0], timestamps[1])

@pytest.mark.asyncio
async def test_get_historical_volatility(client: MarketData):
  result = await client.get_historical_volatility('BTC')
  assert result is not None

@pytest.mark.asyncio
async def test_get_index(client: MarketData):
  result = await client.get_index('BTC')
  assert result is not None

@pytest.mark.asyncio
async def test_get_index_price(client: MarketData):
  result = await client.get_index_price('btc_usd')
  assert result is not None

@pytest.mark.asyncio
async def test_get_index_price_names(client: MarketData):
  result = await client.get_index_price_names()
  assert result is not None
  assert len(result) > 0

@pytest.mark.asyncio
async def test_get_instrument(client: MarketData, btc_instruments: Instruments):
  for instrument in btc_instruments.all:
    result = await client.get_instrument(instrument)
    assert result is not None

@pytest.mark.asyncio
async def test_get_instruments(client: MarketData):
  kinds = ('future', 'option', 'spot')
  for kind in kinds:
    result = await client.get_instruments('BTC', kind=kind)
    assert result is not None
    assert len(result) > 0

@pytest.mark.asyncio
async def test_get_last_settlements_by_currency(client: MarketData):
  result = await client.get_last_settlements_by_currency('BTC')
  assert result is not None

@pytest.mark.asyncio
async def test_get_last_settlements_by_instrument(client: MarketData, btc_instruments: Instruments):
  for instrument in btc_instruments.non_spot:
    result = await client.get_last_settlements_by_instrument(instrument)
    assert result is not None

@pytest.mark.asyncio
async def test_get_last_trades_by_currency(client: MarketData):
  result = await client.get_last_trades_by_currency('BTC')
  assert result is not None

@pytest.mark.asyncio
async def test_get_last_trades_by_currency_and_time(client: MarketData, timestamps):
  result = await client.get_last_trades_by_currency_and_time('BTC', timestamps[0], timestamps[1])
  assert result is not None

@pytest.mark.asyncio
async def test_get_last_trades_by_instrument(client: MarketData, btc_instruments: Instruments):
  for instrument in btc_instruments.all:
    result = await client.get_last_trades_by_instrument(instrument)
    assert result is not None

@pytest.mark.asyncio
async def test_get_last_trades_by_instrument_and_time(client: MarketData, btc_instruments, timestamps):
  for instrument in btc_instruments.all:
    result = await client.get_last_trades_by_instrument_and_time(instrument, timestamps[0], timestamps[1])
    assert result is not None

@pytest.mark.asyncio
async def test_get_mark_price_history(client: MarketData, btc_instruments, timestamps):
  for instrument in btc_instruments.all:
    result = await client.get_mark_price_history(instrument, timestamps[0], timestamps[1])
    assert result is not None

@pytest.mark.asyncio
async def test_get_order_book(client: MarketData, btc_instruments: Instruments):
  for instrument in btc_instruments.all:
    result = await client.get_order_book(instrument)
    assert result is not None

@pytest.mark.asyncio
async def test_get_order_book_by_instrument_id():
  # This test is skipped as it requires valid instrument IDs
  pytest.skip('Requires valid instrument IDs')

@pytest.mark.asyncio
async def test_get_rfqs(client: MarketData):
  result = await client.get_rfqs('BTC')
  assert result is not None

@pytest.mark.asyncio
async def test_get_supported_index_names(client: MarketData):
  result = await client.get_supported_index_names()
  assert result is not None
  assert len(result) > 0

@pytest.mark.asyncio
async def test_get_trade_volumes(client: MarketData):
  result = await client.get_trade_volumes()
  assert result is not None

@pytest.mark.asyncio
async def test_get_tradingview_chart_data(client: MarketData, btc_instruments, timestamps):
  for instrument in btc_instruments.all:
    for interval in ('1', '3', '5', '1D'):
      result = await client.get_tradingview_chart_data(instrument, timestamps[0], timestamps[1], interval)
      assert result is not None

@pytest.mark.asyncio
async def test_get_volatility_index_data(client: MarketData, timestamps):
  for interval in ('1', '60', '3600', '1D'):
    result = await client.get_volatility_index_data('BTC', timestamps[0], timestamps[1], interval)
    assert result is not None

@pytest.mark.asyncio
async def test_ticker(client: MarketData, btc_instruments: Instruments):
  for instrument in btc_instruments.all:
    result = await client.ticker(instrument)
    assert result is not None
