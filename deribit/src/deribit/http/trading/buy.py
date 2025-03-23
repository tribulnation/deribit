from __future__ import annotations

from typing import Literal, TypedDict, NotRequired
from pydantic import BaseModel, Field
from deribit.http.client import AuthedClient

# === PARAM TYPES ===

OrderType = Literal[
  'limit', 'stop_limit', 'take_limit', 'market', 'stop_market', 'take_market', 'market_limit', 'trailing_stop'
]
TimeInForce = Literal[
  'good_til_cancelled', 'good_til_day', 'fill_or_kill', 'immediate_or_cancel'
]
Trigger = Literal['index_price', 'mark_price', 'last_price']
LinkedOrderType = Literal[
  'one_triggers_other', 'one_cancels_other', 'one_triggers_one_cancels_other'
]
TriggerFillCondition = Literal['first_hit', 'complete_fill', 'incremental']
Advanced = Literal['usd', 'implv']
Direction = Literal['buy', 'sell']

class BaseOrderParams(TypedDict, total=False):
  instrument_name: str
  """Instrument name"""
  amount: NotRequired[float]
  """Requested order size (USD for perps/futures, base currency for options)"""
  contracts: NotRequired[float]
  """Order size in contracts (used instead of amount)"""
  type: NotRequired[OrderType]
  """The order type. Default is 'limit'."""
  label: NotRequired[str]
  """User-defined order label (max 64 chars)"""
  time_in_force: NotRequired[TimeInForce]
  """How long the order stays active. Default: 'good_til_cancelled'."""
  max_show: NotRequired[float]
  """Maximum visible amount to other users. 0 = invisible."""
  post_only: NotRequired[bool]
  """Whether the order should avoid taking liquidity."""
  reject_post_only: NotRequired[bool]
  """Reject the order if it would take liquidity. Only valid with post_only=True."""
  reduce_only: NotRequired[bool]
  """Whether the order should only reduce the current position."""
  trigger_offset: NotRequired[float]
  """Max deviation from price peak for triggering (trailing stop)"""
  mmp: NotRequired[bool]
  """Order MMP flag (only for limit)"""
  valid_until: NotRequired[int]
  """If provided, the server processes the request only before this timestamp."""
  linked_order_type: NotRequired[LinkedOrderType]
  """Linked order strategy (e.g. OCO, OTO)"""
  trigger_fill_condition: NotRequired[TriggerFillCondition]
  """Condition under which secondary orders are placed for linked strategies"""
  advanced: NotRequired[Advanced]
  """Advanced pricing (only for options): 'usd' or 'implv'"""

class LimitOrderParams(BaseOrderParams):
  price: float
  """Order price in base currency"""

class TriggerOrderParams(BaseOrderParams):
  trigger_price: float
  """Trigger price required for stop/take orders"""
  trigger: Trigger
  """Trigger condition: index, mark or last price"""

class TriggerLimitOrderParams(TriggerOrderParams):
  price: float
  """Limit price (stop_limit/take_limit only)"""

BuyParams = LimitOrderParams | TriggerLimitOrderParams | TriggerOrderParams | BaseOrderParams

# === RESPONSE TYPES ===

class Order(BaseModel):
  instrument_name: str
  """Unique instrument identifier"""
  order_id: str
  """Unique order ID"""
  order_state: str
  """State: 'open', 'filled', 'rejected', 'cancelled', etc."""
  order_type: str
  """Order type: 'limit', 'market', etc."""
  direction: str
  """Direction: 'buy' or 'sell'"""
  amount: float
  """Requested order size"""
  price: float | str
  """Order price or 'market_price'"""
  average_price: float | None = None
  """Average fill price of the order"""
  filled_amount: float | None = None
  """Amount that has been filled so far"""
  time_in_force: str
  """Time in force policy"""
  post_only: bool
  """Whether the order is post-only"""
  reduce_only: bool | None = None
  """Whether the order is reduce-only"""
  label: str | None = None
  """User-defined order label"""
  trigger: str | None = None
  """Trigger type (for stop/take orders)"""
  trigger_price: float | None = None
  """Price at which the trigger activates the order"""
  trigger_offset: float | None = None
  """Max deviation from peak for triggering (trailing stop)"""
  trigger_fill_condition: str | None = None
  """Trigger condition behavior: first_hit, complete_fill, etc."""
  triggered: bool | None = None
  """Whether the trigger has fired (for triggered orders)"""
  creation_timestamp: int
  """When the order was created (ms since epoch)"""
  last_update_timestamp: int
  """Last update time (ms since epoch)"""

class Trade(BaseModel):
  trade_id: str
  """Unique ID of the trade"""
  timestamp: int
  """Time of trade (ms since epoch)"""
  price: float
  """Trade price"""
  amount: float
  """Amount traded"""
  fee: float
  """Fee paid by user"""
  fee_currency: str
  """Currency in which fee is charged"""
  direction: Direction
  """Direction of trade: 'buy' or 'sell'"""
  liquidity: Literal['M', 'T']
  """Whether order was maker ('M') or taker ('T')"""

class BuyResult(BaseModel):
  order: Order
  """Order details"""
  trades: list[Trade]
  """List of individual trades for this order"""

# === METHOD ===

class Buy:
  client: AuthedClient
  async def buy(self, data: BuyParams) -> BuyResult:
    r = await self.client.authed_post('private/buy', json=data)
    return BuyResult.model_validate(r.result)
