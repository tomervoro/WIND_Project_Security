from typing import Dict
from Scripts.utils import Coordinate
from Scripts.parallel_utils import open_thread, wait_threads_to_finish
from APIs.WIND_api import *
import numpy as np


class UsersTracker:
    def __init__(self):
        self.ridesIds_to_track = []

    def track_user(self, rideId):
        """
        get rideId and get the ride's details so that we'll track the user's route
        :param rideId: rideId to track
        :return: updates USERS_ROUTES TO HOLD: {userId: {rideId: [list of coordinates]}}
        """
        order_details = get_ride_details(rideId)
        while order_details.order_status == OrderStatus.RESERVE:
            time.sleep(30)
            order_details = get_ride_details(rideId)

        while order_details.order_status == OrderStatus.ON_GOING:
            if "undefined" not in order_details.coordinates:
                # TODO- Call SAGI's functions
                pass

    def track_all_users(self, new_rides: Dict[Coordinate, List[str]]) -> None:
        """
        call the tracking function for each rideId
        :param new_rides : dictionary of: {rideId: curr_bike_coordinates}
        """
        for rideId in new_rides:
            self.add_rideId_to_track(rideId)

    def add_rideId_to_track(self, rideId: str) -> None:
        """
        add a ride to track and open a thread to track the order
        :param rideId: ID of ride to track
        """
        open_thread(target=self.track_user, args=(rideId,))


class FindTargets:
    def __init__(self):
        self.users_tracker = UsersTracker()

    @staticmethod
    def get_order_ids(missing_boards: Dict[Coordinate, List[str]]) -> Dict[Coordinate, List[str]]:
        """
        find all orderIds for all recently ordered boards
        :param missing_boards: dictionary of missing_boards that were recently ordered: {boardNo: board_coordinates}
        :return: orders dictionary: {coordinate: <list of missing bikes rideIds>}
        """
        order_ids = {}
        for coordinate in missing_boards:
            for boardNo in missing_boards[coordinate]:
                rideId = get_board_rideId(boardNo)
                if rideId:
                    order_ids[coordinate] = order_ids.get(coordinate, []) + [rideId]
        return order_ids

    @staticmethod
    def get_current_city_boards() -> Dict[Coordinate, List[str]]:
        """
        iterate over the city's coordinates get the board in the city
        return: {coordinate: <list of bikes in that location>}
        """
        city_boards = dict()
        thread_num = 0
        for coordinate in CITY_COORDINATES:
            coordinate_to_check = Coordinate(latitude=coordinate[0], longitude=coordinate[1])
            open_thread(target=get_boards_of_coordinate, args=(coordinate_to_check, city_boards,), name="get_current_city_boards_"+str(thread_num),)
            thread_num += 1
        wait_threads_to_finish("get_current_city_boards", thread_num)
        return city_boards

    @staticmethod
    def get_disappeared_boards(city_boards: Dict[Coordinate, List[str]],
                               curr_boards: Dict[Coordinate, List[str]]) -> Dict[Coordinate, List[str]]:
        """
        get board_ids that existed in the last scan but disappeared from the map in the current scan (->therefore taken by a user)
        :param city_boards: dict of {Coordinate: <list of board_ids in that Coordinate>} of the last city's scan
        :param curr_boards: dict of {Coordinate: <list of board_ids in that Coordinate>} of the current city's scan
        :return: dict of {Coordinate: <list of board_ids in that Coordinate>} of the boards that went missing (->taken by a user)
        """
        disappeared_boards = dict()
        for coordinate in city_boards:
            boards = list(np.setdiff1d(city_boards[coordinate], curr_boards.get(curr_boards, [])))
            if boards:
                disappeared_boards[coordinate] = boards
        return disappeared_boards

    def collect_disappearing_boards(self):
        city_boards = dict()
        while True:
            curr_city_boards: Dict = self.get_current_city_boards()
            disappeared_boards: Dict = self.get_disappeared_boards(city_boards, curr_city_boards)
            new_orders = self.get_order_ids(disappeared_boards)
            self.users_tracker.track_all_users(new_orders)
            city_boards.update(curr_city_boards)

