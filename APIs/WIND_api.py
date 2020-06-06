import json
from typing import List, Dict
import requests
from Scripts.utils import Coordinate, check_status, OrderDetails, userAuthToUse, _logger


#gen_url = 'http://api-prod.windride.io/'
gen_url = 'http://api-prod.ibyke.io/'
#gen_url = 'https://pd-prod.zbike.io/'


def get_boards_of_coordinate(coordinate: Coordinate, city_boards: Dict[Coordinate, List[str]] = None) -> List[str]:
    """
    get a list of all boards in specific coordinate
    :param coordinate: coordinate to check (of type Coordinate)
    :return: a list of all boards in the given coordinate
    """
    try:
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
            if city_boards is not None:
                city_boards[coordinate] = boards_list
            return boards_list
        return []
    except Exception as e:
        _logger.error("get_boards_of_coordinate Failed for coordinate: {}".format(coordinate))
        _logger.error("error type: {}, error: {}".format(type(e), e))


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
    return OrderDetails(userId=userId, order_id=rideId, coordinates=Coordinate(latitude=lat, longitude=long), order_status=status)


