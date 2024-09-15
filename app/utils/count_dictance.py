import math

async def count_distance(
    point_a: tuple,
    point_b: tuple
) -> int:
    R = 6371.0
    
    lat1_rad = math.radians(point_a[0])
    lon1_rad = math.radians(point_a[1])
    lat2_rad = math.radians(point_b[0])
    lon2_rad = math.radians(point_b[1])
    
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad
    
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return int(distance)
