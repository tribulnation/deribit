import pytest
from . import Supporting

client = Supporting()


@pytest.mark.asyncio
async def test_get_time():
    time = await client.get_time()
    assert isinstance(time, int)
    assert time > 0


@pytest.mark.asyncio
async def test_status():
    status = await client.status()
    assert status.locked in ('true', 'false', 'partial')
    assert isinstance(status.locked_indices, list)


@pytest.mark.asyncio
async def test_test():
    result = await client.test()
    assert isinstance(result.version, str)
