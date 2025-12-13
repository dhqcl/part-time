import requests
import json
import urllib3

# Disable SSL warnings for cleaner output if verify=False is used
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://mina-cmapi.cp-properties.cn:1443"

def _get_headers(token, building_id=1):
    # Standard headers. requests will add Content-Length, Host, Connection, etc.
    # We supply the critical custom ones.
    return {
        'Authorization': f'Bearer {token}',
        'buildingid': str(building_id),
        # 'content-type': 'application/json', # Let requests set this to avoid conflicts
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.61(0x18003d39) NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx3f27877140587959/89/page-frame.html'
    }

def query_park_fee(token, plate_number):
    """
    Query parking fee for a specific license plate.
    """
    url = f"{BASE_URL}/api/Park/QueryParkFee_zxtf"
    params = {
        'carno': plate_number
    }
    headers = _get_headers(token, building_id=1)
    
    response = requests.get(url, headers=headers, params=params, verify=False)
    response.raise_for_status()
    return response.json()

def exchange_office_coupon(token, gift_card_id="KQ0000001618", gift_batch_id="GM0000000775"):
    """
    Exchange an office coupon (2 hours).
    """
    url = f"{BASE_URL}/api/UserGiftCert/CertIssue"
    headers = _get_headers(token, building_id=1)
    data = {
        "Giftcartid": gift_card_id,
        "Giftbatchid": gift_batch_id,
        "Bonus": 100,
        "Num": 1
    }
    
    # requests.post(json=data) automatically calls json.dumps and sets Content-Type: application/json
    response = requests.post(url, headers=headers, json=data, verify=False)
    response.raise_for_status()
    return response.json()

def get_cert_bonus(token, gift_card_id="KQ0000001618", gift_batch_id="GM0000000775"):
    """
    Get certificate bonus info.
    """
    url = f"{BASE_URL}/api/GiftCardCert/GetCertBonusAsync"
    headers = _get_headers(token, building_id=1)
    params = {
        "GiftCertId": gift_card_id,
        "GiftBatchId": gift_batch_id
    }
    
    response = requests.get(url, headers=headers, params=params, verify=False)
    response.raise_for_status()
    return response.json()

def query_vip_info_office(token):
    """
    Query VIP info for office.
    """
    url = f"{BASE_URL}/api/VipInfo/QueryVipInfoAsync_office"
    headers = _get_headers(token, building_id=1)
    
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()




def get_park_records(token, page_index=1, page_size=20):
    """
    Get parking payment records.
    """
    url = f"{BASE_URL}/api/Park/ParkRecord_zxtf"
    headers = _get_headers(token, building_id=1)
    params = {
        "pageindex": page_index,
        "pagesize": page_size
    }
    
    response = requests.get(url, headers=headers, params=params, verify=False)
    response.raise_for_status()
    return response.json()

def get_coupon_list(token, page_index=1, page_size=9):
    """
    Get coupon list.
    """
    url = f"{BASE_URL}/api/UserGiftCert/GetCertVipListAsync"
    headers = _get_headers(token, building_id=1)
    data = {
        "ettype": 0,
        "pageindex": page_index,
        "pagesize": page_size,
        "cardtype": "*"
    }
    
    response = requests.post(url, headers=headers, json=data, verify=False)
    response.raise_for_status()
    return response.json()

def sign_shangyuewan(token):
    """
    Sign in to Shang Yue Wan.
    """
    url = f"{BASE_URL}/api/VipInfo/Sign"
    headers = _get_headers(token, building_id=2)
    
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()

def query_vip_info(token):
    """
    Query VIP info (Async version).
    Maps to query_vip_info.txt
    """
    url = f"{BASE_URL}/api/VipInfo/QueryVipInfoAsync"
    headers = _get_headers(token, building_id=1)
    
    # Body is literal 'null', so we send None as json which requests handles as null
    response = requests.post(url, headers=headers, json=None, verify=False)
    response.raise_for_status()
    return response.json()
