from dataclasses import dataclass

from . import MarketData, Trading, Account, Wallet

@dataclass(frozen=True)
class Deribit(
  MarketData,
  Trading,
  Account,
  Wallet,
):
  ...