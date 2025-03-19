from typing import Literal
from datetime import datetime, timedelta, date
from decimal import Decimal
import asyncio
from deribit import MarketData

def days(td: timedelta):
  return td.total_seconds() / (3600*24)

async def premium_vs_expiry(
  client: MarketData, *, strike: Decimal | float, currency: str,
  type: Literal['call', 'put'], now: datetime | None = None
):
  """Returns `([expiry_1, ..., expiry_n], [premium_1, ..., premium_n])`"""
  options = await client.get_options(currency)
  options = [opt for opt in options if opt.strike == Decimal(strike) and opt.option_type == type]
  options.sort(key=lambda x: x.expiration_timestamp)
  books = await asyncio.gather(*[client.get_option_order_book(opt.instrument_name) for opt in options])
  prices = [book.mark_price for book in books]
  now = now or datetime.now()
  expiry_days = [days(opt.expiry-now) for opt in options]
  return expiry_days, prices

async def premium_vs_strike(
  client: MarketData, *, expiry: date | datetime, currency: str,
  type: Literal['call', 'put']
):
  """Returns `([strike_1, ..., strike_n], [premium_1, ..., premium_n])`"""
  def eq_expiry(opt: MarketData.Option):
    return opt.expiry.date() == expiry if isinstance(expiry, date) else opt.expiry == expiry

  options = await client.get_options(currency)
  options = [opt for opt in options if eq_expiry(opt) and opt.option_type == type]
  options.sort(key=lambda x: x.strike)
  books = await asyncio.gather(*[client.get_option_order_book(opt.instrument_name) for opt in options])
  prices = [book.mark_price for book in books]
  strikes = [opt.strike for opt in options]
  return strikes, prices