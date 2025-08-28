# Getting Started

Let's start exploring the Deribit SDK. We don't need API keys for market data:

## Market Data

```python
from deribit import MarketData

async with MarketData() as client:
  book = await client.get_order_book('BTC_USDT', limit=5)
  print(book)
```

```python
{
  'bids': [
    BookEntry(price='117658.65', qty='3.27462000'),
    BookEntry(price='117658.64', qty='0.18392561'),
    # ...
  ],
 'asks': [
    BookEntry(price='117658.66', qty='6.52537624'),
    BookEntry(price='117658.68', qty='0.18654832'),
    # ...
  ],
  # ...
}
```

## Real-time Feed

We can also subscribe to real-time data:

```python
from deribit import PublicSubscriptions

async with PublicSubscriptions() as client:
  resp, stream = await client.depth('BTC_USDT')
  async for book in stream:
    print(book)
```

```python
# keeps printing book updates
```

## Next Steps

- [API Keys Setup](/api-keys) - Set up your Deribit API credentials for trading.
- [Simple DCA Bot](/simple-dca-bot) - Start trading in Deribit with a simple DCA bot.