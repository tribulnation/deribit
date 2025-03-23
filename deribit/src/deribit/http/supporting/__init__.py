# deribit/http/supporting/__init__.py

from dataclasses import dataclass, field
from deribit.http.client import Client
from .get_time import GetTime
from .status import Status
from .test import Test

@dataclass
class Supporting(GetTime, Status, Test):
  client: Client = field(default_factory=Client)

  @classmethod
  def testnet(cls):
    return cls(client=Client.testnet())