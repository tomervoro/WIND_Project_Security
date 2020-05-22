from Scripts.utils import *
from APIs.WIND import *
CITY_BOARDS = {}
USERS_ROUTES = {}


def check_ride_status(status):
    if status == OrderStatus.CANCELLED:
        return OrderStatus.ROLLBACK
    # TODO- add statuses!


def track_user(rideId):
    """
    get rideId and get the ride's details so that we'll track the user's route
    :param rideId: rideId to track
    :return: updates USERS_ROUTES TO HOLD: {userId: {rideId: [list of coordinates]}}
    """
    order_details = get_ride_details(rideId)
    if "undefined" not in order_details.coordinates:
        last_coord = USERS_ROUTES[order_details.userId][rideId][-1]
        if order_details.coordinates != last_coord:
            USERS_ROUTES[order_details.userId][rideId].append(order_details.coordinates)
    if check_ride_status == OrderStatus.ROLLBACK:
        USERS_ROUTES[order_details.userId].pop(rideId)
        return False

def connect_user_to_bike(recent_rides: dict):
    """
    :param recent_rides: dictionary of: {rideId: curr_bike_coordinates}
    :return: list of rideIds to track
    """
    ridesIds = []
    for rideId in recent_rides.keys():
        order_details = get_ride_details(rideId)
        ridesIds.append(rideId)
        USERS_ROUTES[order_details.userId][rideId] = [recent_rides[rideId]]
    return ridesIds


def get_order_ids(missing_boards: dict):
    """
    find all orderIds for all recently ordered boards
    :param missing_boards: dictionary of missing_boards that were recently ordered: {boardNo: board_coordinates}
    :return: orders dictionary: {rideId: curr_bike_coordinates}
    """
    USERS_ROUTES = {}
    for boardNo in missing_boards.keys():
        rideId = get_board_rideId(boardNo)
        if rideId:
            USERS_ROUTES[rideId] = missing_boards[boardNo]
    return USERS_ROUTES

def get_missing_boards(curr_boards: dict, coordinates: tuple):
    """
    find the missing boards that were recently ordered by a user
    :param curr_boards: dictionary that holds {boardNo: coordinates} of all boards at the current time
    :param coordinates: a tuple of (lat, long) to check
    :return: dictionary of missing_boards: {boardNo: board_coordinates}
    """
    missing_boards = dict()
    for boards_id in CITY_BOARDS[coordinates].keys():
        if not curr_boards.get(boards_id):
            missing_boards[boards_id] = CITY_BOARDS[coordinates][boards_id]
            CITY_BOARDS.pop(boards_id)
    return missing_boards


def get_city_boards():
    """
    iterate over the city's coordinates and check if boards gone missing.
    return: a list dictionary of missing_boards:
        {boards_id: (<last lat>, <last long>)}
    """
    missing_boards = dict()
    for coordinate in CITY_COORDINATES:
        res = get_boards(coordinate[0], coordinate[1])
        missing_boards.update(get_missing_boards(res, coordinate))
    return missing_boards


def collect_city_boards():
    """
    collect all the boards in the city into one dictionary: CITY_COORDINATES (check utils.py)
    """
    for coordinate in CITY_COORDINATES:
        res = get_boards(coordinate[0], coordinate[1])
        if res:
            CITY_BOARDS.update(res)
    print_msg("Built all CITY_BOARDS: {}".format(CITY_BOARDS))


#collect_city_boards()