from dadata import DadataAsync
from config import dadata_secret as secret, dadata_token as token


async def get_valid_address_and_coords(
    address: str
) -> (str, float, float): # type: ignore
    async with DadataAsync(token) as dadata:
        raw_data = (await dadata.suggest("address", address))[0]
        return (raw_data["value"], raw_data["data"]["geo_lat"], raw_data["data"]["geo_lon"])
    