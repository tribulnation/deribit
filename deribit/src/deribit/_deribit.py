from dataclasses import dataclass

from . import MarketData, Trading, Account

@dataclass(frozen=True)
class Deribit(
  MarketData,
  Trading,
  Account,
):
  ...