import webbrowser
from utils import Coordinate
import gmplot
import os
import copy
import time
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class MapManager:

    def __init__(self, map_center: Coordinate, zoom=13):
        self.map_center = map_center  # center of the map
        self.zoom = zoom  # area of map to display. 13 is pretty good
        self.gmap = gmplot.GoogleMapPlotter(self.map_center.latitude, self.map_center.longitude, self.zoom)
        self.users_trips = dict()  # for each user id in the dictionary, there is a trips dictionary. # for each trip
        # id in the dictionary, there is a trip details struct

    def generateRandomColor(self):
        """
        :return: a random color string
        """
        return "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])

    def doesUserExist(self, user_id):
        """
        :param user_id: user id
        :return: true iff the user is known to the manager
        """
        return user_id in self.users_trips

    def doesTripExist(self, user_id, trip_id):
        """
        :param user_id: user id
        :param trip_id: trip id
        :return: true iff the user and the trip are known to the manager
        """
        if user_id not in self.users_trips:
            return False
        return trip_id in self.users_trips[user_id]

    def addUser(self, user_id):
        """
        adds a new user to the manager, with an empty trips dictionary
        :param user_id: user id
        :return:
        """
        if self.doesUserExist(user_id):
            print("this user is already known to the system! id: {}".format(user_id))
            return
        self.users_trips[user_id] = dict()

    def addTrip(self, user_id, trip_id, trip_details):
        """
        adds a new trip to the manager
        :param user_id: user id
        :param trip_id: trip id
        :param trip_details: trip details struct
        :return:
        """
        if not self.doesUserExist(user_id):
            print("this user is not known to the system! id: {}".format(user_id))
            return
        if self.doesTripExist(user_id, trip_id):
            print("this trip is already known to the system! user_id: {}, trip_id: {}".format(user_id, trip_id))
            return

        self.users_trips[user_id][trip_id] = trip_details

    def getTrips(self, user_id):
        """
        :param user_id: user id
        :return: trips dictionary
        """
        if not self.doesUserExist(user_id):
            print("this user is not known to the system! id: {}".format(user_id))
            return None

        return self.users_trips[user_id]

    def getTripDetails(self, user_id, trip_id):
        """
        :param user_id: user id
        :param trip_id: trip id
        :return: trip details struct
        """
        if not self.doesUserExist(user_id):
            print("this user is not known to the system! id: {}".format(user_id))
            return None
        if not self.doesTripExist(user_id, trip_id):
            print("this trip is not known to the system! user_id: {}, trip_id: {}".format(user_id, trip_id))
            return None

    def getTripCoordinates(self, user_id, trip_id):
        """
        :param user_id: user id
        :param trip_id: trip id
        :return: trip coordinate list
        """
        if not self.doesUserExist(user_id):
            print("this user is not known to the system! id: {}".format(user_id))
            return None
        if not self.doesTripExist(user_id, trip_id):
            print("this trip is not known to the system! user_id: {}, trip_id: {}".format(user_id, trip_id))
            return None

        return self.users_trips[user_id][trip_id]["coordinates_list"]

    def addCoordinateToTrip(self, user_id, trip_id, coordinate: Coordinate):
        """
        adds a new coordinate to the trip
        :param user_id: user id
        :param trip_id: trip id
        :param coordinate: new coordinate
        :return:
        """
        if not self.doesUserExist(user_id):
            print("this user is not known to the system! id: {}".format(user_id))
            return
        if not self.doesTripExist(user_id, trip_id):
            print("this trip is not known to the system! user_id: {}, trip_id: {}".format(user_id, trip_id))
            return

        self.users_trips[user_id][trip_id]["coordinates_list"].append(coordinate)

    def resetMap(self):
        """
        resets the map to be blank (removes all plots)
        :return:
        """
        self.gmap = gmplot.GoogleMapPlotter(self.map_center.latitude, self.map_center.longitude, self.zoom)

    def drawCoordinates(self, coordinates, color='cornflowerblue', edge_width=2.5):
        """
        draws the coordinates on the map
        :param coordinates: coordinates list
        :param color: color of the edges
        :param edge_width: edge width
        :return:
        """
        latitude_list = []
        longitude_list = []

        for coordinate in coordinates:
            latitude_list.append(coordinate.latitude)
            longitude_list.append(coordinate.longitude)

        self.gmap.scatter(latitude_list, longitude_list, '# FF0000', size=40, marker=False)

        self.gmap.plot(latitude_list, longitude_list, color, edge_width=edge_width)

    def drawTrip(self, user_id, trip_id, color='cornflowerblue', edge_width=2.5):
        """
        draws a user's trip
        :param user_id: user id
        :param trip_id: trip id
        :param color: color of the edges
        :param edge_width: edge width
        :return:
        """
        if not self.doesUserExist(user_id):
            print("this user is not known to the system! id: {}".format(user_id))
            return
        if not self.doesTripExist(user_id, trip_id):
            print("this trip is not known to the system! user_id: {}, trip_id: {}".format(user_id, trip_id))
            return

        self.drawCoordinates(self.getTripCoordinates(user_id, trip_id), color, edge_width)

    def drawUserTrips(self, user_id, color='cornflowerblue', edge_width=2.5):
        """
        draws all trips of user with the same color
        :param user_id:
        :param color:
        :param edge_width:
        :return:
        """
        if not self.doesUserExist(user_id):
            print("this user is not known to the system! id: {}".format(user_id))
            return
        for trip_id in self.getTrips(user_id):
            self.drawTrip(user_id, trip_id, color, edge_width)

    def drawAllTrips(self):
        """
        draws every trip of every user. trips that belong to the same user have the same random color. also plots an
        legend for the colors
        :return:
        """
        handles = []
        for user_id in self.users_trips:
            color = self.generateRandomColor()
            handles.append(mpatches.Patch(color=color, label=user_id))
            self.drawUserTrips(user_id, color)

        plt.figure()
        plt.legend(handles=handles)
        plt.show()

    def printMap(self):
        """
        prints the map
        :return:
        """
        tmp_gmap = copy.deepcopy(self.gmap)
        self.gmap.draw("map.html")
        webbrowser.open('file://' + os.path.realpath("map.html"))
        self.gmap = tmp_gmap


# coordinate = Coordinate(30.3164945, 78.03219179)
# manager = MapManager(coordinate)
#
#
# c1=Coordinate(30.3358376, 77.8701919)
# c2=Coordinate(30.307977, 78.048457)
# c3=Coordinate(30.3216419, 78.0413095)
#
#
# manager.addUser("sagi")
#
# manager.addTrip("sagi", "trip1", {"coordinates_list" : []})
#
# manager.addCoordinateToTrip("sagi", "trip1", c1)
# manager.addCoordinateToTrip("sagi", "trip1", c2)
# manager.addCoordinateToTrip("sagi", "trip1", c3)
#
#
#
# c1=Coordinate(30.3458376, 77.8801919)
# c2=Coordinate(30.347977, 78.068457)
# c3=Coordinate(30.3416419, 78.0513095)
#
#
# manager.addUser("tomer")
#
# manager.addTrip("tomer", "trip1", {"coordinates_list" : []})
#
# manager.addCoordinateToTrip("tomer", "trip1", c1)
# manager.addCoordinateToTrip("tomer", "trip1", c2)
# manager.addCoordinateToTrip("tomer", "trip1", c3)
#
#
# manager.resetMap()
# manager.drawAllTrips()
#
# manager.printMap()
