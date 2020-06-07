from time import sleep
from typing import Dict, List
from parallel_utils import open_thread, wait_threads_to_finish
from APIs.WIND_api import get_ride_details, get_board_rideId, get_boards_of_coordinate
from utils import CITY_COORDINATES, OrderStatus, Coordinate
from map_manager import MapManager
import numpy as np


class UsersTracker:
    def __init__(self):
        self.ridesIds_to_track = []
        self.map_manager = MapManager()
        self.map_manager.loadFromJson()

    def track_ride(self, rideId):
        """
        get rideId and get the ride's details so that we'll track the user's route
        :param rideId: rideId to track
        :return: updates USERS_ROUTES TO HOLD: {userId: {rideId: [list of coordinates]}}
        """
        print(rideId)
        order_details = get_ride_details(rideId)
        #user_map = self.map_manager.generateMap()
        while order_details.order_status == OrderStatus.RESERVE.value:
            sleep(30)
            order_details = get_ride_details(rideId)

        cnt = 1
        while order_details.order_status == OrderStatus.ON_GOING.value:
            if "undefined" not in order_details.coordinates:
                self.map_manager.addCoordinateToTrip(user_id=order_details.userId, trip_id=order_details.order_id, coordinate=order_details.coordinates)
                sleep(5)
                cnt += 1

            order_details = get_ride_details(rideId)
            if cnt % 20 == 0:
                self.map_manager.drawAllTrips() # drawTrip(user_id=order_details.userId, trip_id=order_details.order_id)
                self.map_manager.printMap()
                self.map_manager.saveToJson()

        self.map_manager.drawAllTrips()  # drawTrip(user_id=order_details.userId, trip_id=order_details.order_id)
        self.map_manager.printMap()
        self.map_manager.saveToJson()

    def add_rideId_to_track(self, rideId: str) -> None:
        """
        add a ride to track and open a thread to track the order
        :param rideId: ID of ride to track
        """
        #### TODO- add this instead:
        open_thread(target=self.track_ride, args=(rideId,))
        #self.track_ride(rideId)

    def track_users(self, rides_ids: List[str]) -> None:
        """
        Main entry point for this class: call the tracking function for each rideId in a separate thread
        :param new_rides : list of rideIds
        """
        for rideId in set(rides_ids):
            self.add_rideId_to_track(rideId)

   

class FindTargets:
    def __init__(self):
        self.users_tracker = UsersTracker()
        self.first_run_flag = True

    @staticmethod
    def get_rides_ids(missing_boards: Dict[Coordinate, List[str]]) -> List[str]:
        """
        find all orderIds for all recently ordered boards
        :param missing_boards: dictionary of missing_boards that were recently ordered: {boardNo: board_coordinates}
        :return: list of rideIds
        """
        rides_ids = []
        for coordinate in missing_boards:
            for boardNo in missing_boards[coordinate]:
                rideId = get_board_rideId(boardNo)
                if rideId:
                    rides_ids.append(rideId)
        return rides_ids

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



            #TODO- add instead:
            #open_thread(target=get_boards_of_coordinate, args=(coordinate_to_check, city_boards,), name="get_current_city_boards_"+str(thread_num),)
            get_boards_of_coordinate(coordinate_to_check, city_boards)



            thread_num += 1
        ### TODO- add this: wait_threads_to_finish("get_current_city_boards")
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
            boards = list(np.setdiff1d(city_boards[coordinate], curr_boards.get(coordinate, [])))
            if boards:
                disappeared_boards[coordinate] = boards
        return disappeared_boards

    def collect_disappearing_boards(self):
        """
        main entry point that does the following:
        1. collect all the boards in the city by scanning each coordinate's radius
        2. check which boards went missing in the current scan
        3. get the order IDs of the recently taken boards
        4. call users_tracker to track the new orders
        5. update the city_boards for the next scan
        """
        city_boards = dict()
        while True:
            try:
                curr_city_boards: Dict = self.get_current_city_boards()
                if self.first_run_flag:
                    city_boards.update(curr_city_boards)
                    self.first_run_flag = False
                    continue
                disappeared_boards: Dict = self.get_disappeared_boards(city_boards, curr_city_boards)
                if not disappeared_boards:
                    continue
                new_rides_ids = self.get_rides_ids(disappeared_boards)
                if not new_rides_ids:
                    continue
                self.users_tracker.track_users(new_rides_ids)
                city_boards.update(curr_city_boards)
            except:
                continue
            #sleep(10)


def main():
    hacker = FindTargets()
    hacker.collect_disappearing_boards()

if __name__ == "__main__":
    main()