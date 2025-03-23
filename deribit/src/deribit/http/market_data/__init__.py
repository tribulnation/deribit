# deribit/http/market_data/__init__.py

from dataclasses import dataclass, field
from deribit.http.client import Client

from .get_book_summary_by_currency import GetBookSummaryByCurrency
from .get_book_summary_by_instrument import GetBookSummaryByInstrument
from .get_contract_size import GetContractSize
from .get_currencies import GetCurrencies
from .get_delivery_prices import GetDeliveryPrices
from .get_expirations import GetExpirations
from .get_funding_chart_data import GetFundingChartData
from .get_funding_rate_history import GetFundingRateHistory
from .get_funding_rate_value import GetFundingRateValue
from .get_historical_volatility import GetHistoricalVolatility
from .get_index import GetIndex
from .get_index_price import GetIndexPrice
from .get_index_price_names import GetIndexPriceNames
from .get_instrument import GetInstrument
from .get_instruments import GetInstruments
from .get_last_settlements_by_currency import GetLastSettlementsByCurrency
from .get_last_settlements_by_instrument import GetLastSettlementsByInstrument
from .get_last_trades_by_currency import GetLastTradesByCurrency
from .get_last_trades_by_currency_and_time import GetLastTradesByCurrencyAndTime
from .get_last_trades_by_instrument import GetLastTradesByInstrument
from .get_last_trades_by_instrument_and_time import GetLastTradesByInstrumentAndTime
from .get_mark_price_history import GetMarkPriceHistory
from .get_order_book import GetOrderBook
from .get_order_book_by_instrument_id import GetOrderBookByInstrumentId
from .get_rfqs import GetRFQs
from .get_supported_index_names import GetSupportedIndexNames
from .get_trade_volumes import GetTradeVolumes
from .get_tradingview_chart_data import GetTradingViewChartData
from .get_volatility_index_data import GetVolatilityIndexData
from .ticker import GetTicker

@dataclass
class MarketData(
  GetBookSummaryByCurrency,
  GetBookSummaryByInstrument,
  GetContractSize,
  GetCurrencies,
  GetDeliveryPrices,
  GetExpirations,
  GetFundingChartData,
  GetFundingRateHistory,
  GetFundingRateValue,
  GetHistoricalVolatility,
  GetIndex,
  GetIndexPrice,
  GetIndexPriceNames,
  GetInstrument,
  GetInstruments,
  GetLastSettlementsByCurrency,
  GetLastSettlementsByInstrument,
  GetLastTradesByCurrency,
  GetLastTradesByCurrencyAndTime,
  GetLastTradesByInstrument,
  GetLastTradesByInstrumentAndTime,
  GetMarkPriceHistory,
  GetOrderBook,
  GetOrderBookByInstrumentId,
  GetRFQs,
  GetSupportedIndexNames,
  GetTradeVolumes,
  GetTradingViewChartData,
  GetVolatilityIndexData,
  GetTicker,
):
  client: Client = field(default_factory=Client)

  @classmethod
  def testnet(cls):
    return cls(client=Client.testnet())
