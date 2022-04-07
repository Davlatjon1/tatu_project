from geopy import GoogleV3
from data import config
from geopy.adapters import AioHTTPAdapter
from fake_useragent import UserAgent


async def get_address(latitude: str, longitude: str):
    key = config.MAP_TOKEN
    try:
        async with GoogleV3(api_key=key,
                            timeout=10,
                            adapter_factory=AioHTTPAdapter,
                            user_agent=UserAgent().chrome) as geolocation:
            location = await geolocation.reverse(f"{latitude}, {longitude}")
            result = location.address
    except Exception as err:
        result = ''

    return result
