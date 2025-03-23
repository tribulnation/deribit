from typing import Annotated
from datetime import datetime, date
from pydantic import BeforeValidator
from decimal import Decimal, ROUND_HALF_DOWN

def round2tick(x: Decimal, tick_size: Decimal) -> Decimal:
  r = (x / tick_size).quantize(Decimal('1.'), rounding=ROUND_HALF_DOWN) * tick_size
  return r.normalize()

def path_join(base: str, *parts: str):
  return '/'.join([base.rstrip('/')] + [part.lstrip('/') for part in parts])

class timestamp:
  @staticmethod
  def parse(timestamp: int):
    return datetime.fromtimestamp(timestamp/1e3)
  @staticmethod
  def dump(dt: datetime):
    return int(dt.timestamp()*1e3)
  @staticmethod
  def now():
    return round(datetime.now().timestamp()*1e3)
  
def getenv(var: str):
  def getter():
    import os
    return os.environ[var]
  return getter


def parse_date(value):
  """Parse date in `DDMMMYY` (e.g `25JUN24`) format."""
  if isinstance(value, str):
    value = datetime.strptime(value, '%d%b%y').date()
  return value

Date = Annotated[date, BeforeValidator(parse_date)]