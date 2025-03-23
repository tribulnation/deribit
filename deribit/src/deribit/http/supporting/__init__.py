from dataclasses import dataclass
from deribit.http.client import Client
from .get_time import GetTime
from .status import Status
from .test import Test

@dataclass
class Supporting(GetTime, Status, Test):
  client: Client