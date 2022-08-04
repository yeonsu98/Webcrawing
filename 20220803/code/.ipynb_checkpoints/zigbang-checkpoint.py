import requests
import pandas as pd
import geohash2

def oneroom(addr):
    """ This function is crawling information of oneroom from zigbang
    
    Params
    ------
    addr : str : address
    
    Return
    ------
    type : DataFrame : display item_id, sales_type, deposit, rent, size_m2, address1, manage_cost columns
    
    """
    
    # 1. 동이름 > 위도, 경도
    url = f"https://apis.zigbang.com/v2/search?leaseYn=N&q={addr}&serviceType=원룸"
    response = requests.get(url)
    
    data = response.json()['items'][0]
    lat, lng = data['lat'], data['lng']
    
    # 2. 위도, 경도 > geohash(영역) 변환
    geohash = geohash2.encode(lat, lng, precision=5)
    
    # 3. geohash > 매물 아이디
    url = f"https://apis.zigbang.com/v2/items?deposit_gteq=0&domain=zigbang\
&geohash={geohash}&needHasNoFiltered=true&rent_gteq=0&sales_type_in=전세|월세&service_type_eq=원룸"

    response = requests.get(url)
    
    items = response.json()['items']
    ids = [item['item_id'] for item in items]
    
    # 4. 매물 아이디 > 매물 정보
    url = "https://apis.zigbang.com/v2/items/list"
    params = {
        "domain" : "zigbang",
        "withCoalition": "true",
        "item_ids" : ids[:900]
    }
    response = requests.post(url, params)
    
    items = response.json()["items"]
    columns = ["item_id", "sales_type", "deposit", "rent", "size_m2", "address1", "manage_cost"]
    
    return pd.DataFrame(items)[columns]
    
