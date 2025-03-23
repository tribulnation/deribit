import pytest
from deribit.http.client import Client
from deribit.http.market_data import MarketData

client = MarketData(Client.testnet())


@pytest.mark.asyncio
async def test_get_book_summary_by_currency():
  await client.get_book_summary_by_currency("BTC")


@pytest.mark.asyncio
async def test_get_book_summary_by_instrument():
  await client.get_book_summary_by_instrument("BTC-PERPETUAL")


@pytest.mark.asyncio
async def test_get_contract_size():
  await client.get_contract_size("BTC-PERPETUAL")


@pytest.mark.asyncio
async def test_get_currencies():
  await client.get_currencies()


@pytest.mark.asyncio
async def test_get_delivery_prices():
  await client.get_delivery_prices("btc_usd")


@pytest.mark.asyncio
async def test_get_expirations():
  await client.get_expirations("grouped", "any")


@pytest.mark.asyncio
async def test_get_funding_chart_data():
  await client.get_funding_chart_data("BTC-PERPETUAL", "8h")


@pytest.mark.asyncio
async def test_get_funding_rate_history():
  await client.get_funding_rate_history("BTC-PERPETUAL", 1710000000000, 1710100000000)


@pytest.mark.asyncio
async def test_get_funding_rate_value():
  await client.get_funding_rate_value("BTC-PERPETUAL", 1710000000000, 1710100000000)


@pytest.mark.asyncio
async def test_get_historical_volatility():
  await client.get_historical_volatility("BTC")


@pytest.mark.asyncio
async def test_get_index():
  await client.get_index("BTC")


@pytest.mark.asyncio
async def test_get_index_price():
  await client.get_index_price("btc_usd")


@pytest.mark.asyncio
async def test_get_index_price_names():
  await client.get_index_price_names()


@pytest.mark.asyncio
async def test_get_instrument():
  await client.get_instrument("BTC-PERPETUAL")


@pytest.mark.asyncio
async def test_get_instruments():
  await client.get_instruments("BTC", kind="future")


@pytest.mark.asyncio
async def test_get_last_settlements_by_currency():
  await client.get_last_settlements_by_currency("BTC")


@pytest.mark.asyncio
async def test_get_last_settlements_by_instrument():
  await client.get_last_settlements_by_instrument("BTC-PERPETUAL")


@pytest.mark.asyncio
async def test_get_last_trades_by_currency():
  await client.get_last_trades_by_currency("BTC")


@pytest.mark.asyncio
async def test_get_last_trades_by_currency_and_time():
  await client.get_last_trades_by_currency_and_time("BTC", 1710000000000, 1710100000000)


@pytest.mark.asyncio
async def test_get_last_trades_by_instrument():
  await client.get_last_trades_by_instrument("BTC-PERPETUAL")


@pytest.mark.asyncio
async def test_get_last_trades_by_instrument_and_time():
  await client.get_last_trades_by_instrument_and_time("BTC-PERPETUAL", 1710000000000, 1710100000000)


@pytest.mark.asyncio
async def test_get_mark_price_history():
  await client.get_mark_price_history("BTC-PERPETUAL", 1710000000000, 1710100000000)


@pytest.mark.asyncio
async def test_get_order_book():
  await client.get_order_book("BTC-PERPETUAL")


@pytest.mark.asyncio
async def test_get_order_book_by_instrument_id():
  # Use a valid instrument_id. 100 is invalid.
  # This test is skipped unless a valid ID is provided.
  pytest.skip("Instrument ID '100' is invalid on testnet")


@pytest.mark.asyncio
async def test_get_rfqs():
  await client.get_rfqs("BTC")


@pytest.mark.asyncio
async def test_get_supported_index_names():
  await client.get_supported_index_names()


@pytest.mark.asyncio
async def test_get_trade_volumes():
  await client.get_trade_volumes()


@pytest.mark.asyncio
async def test_get_tradingview_chart_data():
  await client.get_tradingview_chart_data("BTC-PERPETUAL", 1710000000000, 1710100000000, "1")


@pytest.mark.asyncio
async def test_get_volatility_index_data():
  await client.get_volatility_index_data("BTC", 1710000000000, 1710100000000, "60")


@pytest.mark.asyncio
async def test_ticker():
  await client.ticker("BTC-PERPETUAL")
