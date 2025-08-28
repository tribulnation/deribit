# Hedging Perps

Let's use the real-time streams for automated hedging.

## Reacting to Trades

We'll manually place limit short orders on the `ETH_USDC` perpetual. Once one fills, we'll automatically buy the spot, same amount.

```python
async def hedge_short():
  async with Deribit.new() as client:
    _, stream = await client.subscriptions.user_trades(instrument_name='ETH_USDC-PERPETUAL')
    async for trades in stream:
      for trade in trades:
        if trade['direction'] == 'sell':
          await client.buy('ETH_USDC', {
            'amount': trade['amount'],
            'type': 'market',
          })
```

And that's the kind of thing you can only do with the API.🚀🚀
