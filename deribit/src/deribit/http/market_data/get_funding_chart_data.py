# deribit/http/market_data/get_funding_chart_data.py

from typing import Literal
from decimal import Decimal
from pydantic import BaseModel, RootModel
from deribit.http.client import Client

class FundingChartPoint(BaseModel):
  index_price: Decimal
  interest_8h: Decimal
  timestamp: int

class FundingChartData(BaseModel):
  current_interest: Decimal
  interest_8h: Decimal
  data: list[FundingChartPoint]

class FundingChartResponse(RootModel):
  root: FundingChartData

Length = Literal['8h', '24h', '1m']

class GetFundingChartData:
  client: Client

  async def get_funding_chart_data(self, instrument_name: str, length: Length):
    params = {'instrument_name': instrument_name, 'length': length}
    r = await self.client.get('public/get_funding_chart_data', params=params)
    return FundingChartResponse.model_validate(r.result).root

