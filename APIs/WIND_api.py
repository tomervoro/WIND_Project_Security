import json
from typing import List, Dict

import requests
from Scripts.utils import *

userAuthTomer = ""
userAuthSagi = "clientId=3abd7241-cc27-4c03-85dc-5e7a32c04351;userId=2015f39e-63d4-42d5-b896-3cd95d3f0696;ft=1823d32bfc0a6d6e17f94e75eaf5e3ec"
userAuthToUse = userAuthSagi
#gen_url = 'http://api-prod.windride.io/'
gen_url = 'http://api-prod.ibyke.io/'
#gen_url = 'https://pd-prod.zbike.io/'


def get_boards_of_coordinate(coordinate: Coordinates, city_boards: Dict[Coordinates, List[str]] = None) -> List[str]:
    """
    get a list of all boards in specific coordinate
    :param coordinate: coordinate to check (of type Coordinates)
    :return: a list of all boards in the given coordinate
    """
    url = "http://api-prod.windride.io/v2/boards?latitude={}&longitude={}".format(coordinate.latitude, coordinate.longitude)
    payload = {}
    headers = {'Authentication': userAuthToUse, 'X-Additional-View': 'user;', 'X-App-Version': '4.15.0.1651'}
    response = requests.request("GET", url, headers=headers, data=payload)
    if check_status(response):
        data = json.loads(response.text.encode('utf8'))
        boards_list = [board.get('boardNo') for board in data.get('items',[]) if board.get('boardNo')]
        """
        ret_dict = dict()
        for board in data['items']:
            ret_dict[board['boardNo']] = (board['latitude'], board['longitude'],)
        """
        if city_boards:
            city_boards[coordinate] = boards_list
        return boards_list
    return []


def get_board_rideId(boardNo: str) -> str:
    """
    return a board's ride ID or None if board isn't taken
    :param boardNo: Board number such as: S0028357
    :return: rideID if the board is taken else- None
    """
    url = "http://api-prod.windride.io/v2/boards/{}".format(boardNo)
    payload = {}
    headers = {'Authentication': userAuthToUse, 'X-App-Version': '4.15.0.1651'}
    response = requests.request("GET", url, headers=headers, data=payload)
    if check_status(response):
        data = json.loads(response.text.encode('utf8'))
        return data.get('board', dict()).get('currentRideId')
    return ''


def get_ride_details(rideId: str) -> OrderDetails:
    """
    get ride details
    :param rideId: rideId to check
    :return: userId for current ride and (lat, long) of bike
    """
    url = "https://api-prod.ibyke.io/v2/boardRides/{}/waypoints".format(rideId)
    payload = {}
    headers = {'Authentication': userAuthToUse}
    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text.encode('utf8'))
    userId = data['ride']['userId']
    lat = data['board']['latitude']
    long = data['board']['longitude']
    status = data['ride']['status']
    return OrderDetails(userId=userId, coordinates=Coordinates(latitude=lat, longitude=long), order_status=status)



"""
def get_user_invitation():
    url = "https://api-prod.ibyke.io/v2/user/invitation"
    payload = "{x0a  \"code\": \"J3WKDK3\"x0a}"
    headers = {
        'Authentication': 'clientId=3abd7241-cc27-4c03-85dc-5e7a32c04351;userId=2015f39e-63d4-42d5-b896-3cd95d3f0696;ft=97889d84f5f9e8e3a71fc66cfbddcae6',
        'X-Additional-View': '',
        'X-Req-Id': 'aa9e7d65-eb0e-4bd7-942d-6bbc9a7c977b',
        'X-App-Version': '4.15.0.1651',
        'X-Country': 'US',
        'X-Lang': 'en',
        'X-Package-Name': 'com.zen.zbike',
        'X-Adv-Id': '96486936-7c6a-4e9e-842e-543306c1b397',
        'X-Platform': 'android_21',
        #'X-Timestamp': '1586515363605',
        'X-MNC': '3',
        'X-MCC': '425',
        'X-MNCMCC': '3_425',
        'X-Lat': '32.4807105',
        'X-Long': '34.9838396',
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': '23',
        'Host': 'api-prod.ibyke.io',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.8.1',
    }

    return requests.request("POST", url, headers=headers, data=payload)
"""