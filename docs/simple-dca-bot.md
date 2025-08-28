# Simple Trading Bot

Let's build our first simple trading bot!🚀🚀

It'll be a simple DCA bot for our bitcoin maximalists :)

## First Version

```python
import asyncio
from deribit import Deribit

async def dca_bot(
  pair: str = 'BTCUSDT',
  qty: str = '0.001',
  interval: int = 3600*24,
):
  async with Deribit.new() as client:
    while True:
      await client.buy(pair, {
        'amount': qty,
        'type': 'market',
      })
      await asyncio.sleep(interval)
```

## Second Version

> "This eats the spread and taker fees!", you'll point out.

> "Fair enough, let's make it smarter".

We'll keep track of the order book at instead place limit orders on the top bid.

```python
async def maker_dca_bot(
  pair: str = 'BTCUSDT',
  qty: str = '0.001',
  interval: int = 3600*24,
):
  async with Deribit.new() as client:
    while True:
      book = await client.get_order_book(pair, depth=1)
      price, _ = book['result']['bids'][0]
      order = await client.buy(pair, {
        'price': price,
        'amount': qty,
        'type': 'limit',
      })
      order_id = order['result']['order']['order_id']
      while True:
        status = await client.get_order_state(order_id)
        if status['result']['order_state'] == 'filled':
          break
        await asyncio.sleep(15)
    
      await asyncio.sleep(interval)
```

Much better!


## Next Steps

- [Hedging Perps](/hedging-perps) - Use real-time streams for automated hedging.