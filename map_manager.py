import webbrowser

from utils import Coordinate
import gmplot
import os
import copy
import time


class map_manager():

    def __init__(self, map_center: Coordinate, zoom=13):
        self.map_center = map_center
        self.zoom = zoom
        self.gmap = gmplot.GoogleMapPlotter(self.map_center.latitude, self.map_center.longitude, self.zoom)
        self.users_trips = dict()

    def doesUserExist(self, user_id):
        return user_id in self.users_trips

    def doesTripExist(self, user_id, trip_id):
        if user_id not in self.users_trips:
            return False
        return trip_id in self.users_trips[user_id]

    def addUser(self, user_id):
        if self.doesUserExist(user_id):
            print("this user is already known to the system! id: {}".format(user_id))
            return
        self.users_trips[user_id] = [dict()]

    def addNewTrip(self, user_id, trip_id, trip_details):
        if not self.doesUserExist(user_id):
            print("this user is not known to the system! id: {}".format(user_id))
            return
        if self.doesTripExist(user_id, trip_id):
            print("this trip is already known to the system! user_id: {}, trip_id: {}".format(user_id, trip_id))
            return

        self.users_trips[user_id][trip_id] = trip_details

    def getTripDetails(self, user_id, trip_id):
        if not self.doesUserExist(user_id):
            print("this user is not known to the system! id: {}".format(user_id))
            return None
        if not self.doesTripExist(user_id, trip_id):
            print("this trip is not known to the system! user_id: {}, trip_id: {}".format(user_id, trip_id))
            return None


    def getTripCoordinates(self, user_id, trip_id):
        if not self.doesUserExist(user_id):
            print("this user is not known to the system! id: {}".format(user_id))
            return None
        if not self.doesTripExist(user_id, trip_id):
            print("this trip is not known to the system! user_id: {}, trip_id: {}".format(user_id, trip_id))
            return None

        return self.users_trips[user_id][trip_id].coordinates_list

    def addCoordinateToTrip(self, user_id, trip_id, coordinate: Coordinate):
        if not self.doesUserExist(user_id):
            print("this user is not known to the system! id: {}".format(user_id))
            return
        if not self.doesTripExist(user_id, trip_id):
            print("this trip is not known to the system! user_id: {}, trip_id: {}".format(user_id, trip_id))
            return
        self.users_trips[user_id][trip_id].coordinates.append(coordinate)

    def reset_map(self):
        self.gmap = gmplot.GoogleMapPlotter(self.map_center.latitude, self.map_center.longitude, self.zoom)

    def draw_coordinates(self, coordinates, color='cornflowerblue', edge_width=2.5):
        latitude_list = []
        longitude_list = []

        for coordinate in coordinates:
            latitude_list.append(coordinate.latitude)
            longitude_list.append(coordinate.longitude)

        self.gmap.scatter(latitude_list, longitude_list, '# FF0000', size=40, marker=False)

        self.gmap.plot(latitude_list, longitude_list, color, edge_width=edge_width)

    def draw_trip(self, user_id, trip_id, color='cornflowerblue', edge_width=2.5):
        if not self.doesUserExist(user_id):
            print("this user is not known to the system! id: {}".format(user_id))
            return
        if not self.doesTripExist(user_id, trip_id):
            print("this trip is not known to the system! user_id: {}, trip_id: {}".format(user_id, trip_id))
            return

        self.draw_coordinates(self.users_trips[user_id][trip_id].coordinates_list, color, edge_width)

    def print_map(self):
        tmp_gmap = copy.deepcopy(self.gmap)
        self.gmap.draw("map.html")
        webbrowser.open('file://' + os.path.realpath("map.html"))
        self.gmap = tmp_gmap


# coordinate = Coordinate(30.3164945, 78.03219179)
# manager = map_manager(coordinate)
#
#
# c1=Coordinate(30.3358376, 77.8701919)
# c2=Coordinate(30.307977, 78.048457)
# c3=Coordinate(30.3216419, 78.0413095)
#
# coordinates = [c1, c2, c3]
#
# manager.draw_coordinates(coordinates)
# manager.print_map()
#
# c1=Coordinate(30.3458376, 77.8801919)
# c2=Coordinate(30.347977, 78.068457)
# c3=Coordinate(30.3416419, 78.0513095)
#
# coordinates = [c1, c2, c3]
# manager.reset_map()
# manager.draw_coordinates(coordinates)
# time.sleep(3)
# manager.print_map()
