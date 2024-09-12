from dadata import DadataAsync
from config import dadata_secret as secret, dadata_api_key as token


async def get_valid_address_and_coords(
    address: str
) -> (str, float, float): # type: ignore
    async with DadataAsync(token=token, secret=secret) as dadata:
        raw_data = await dadata.clean(name="address", source=address)
        return (raw_data["result"], raw_data["geo_lat"], raw_data["geo_lon"])
        