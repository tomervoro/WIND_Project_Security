import webbrowser
from utils import Coordinate, TripDetails
import gmplot
import os
import copy
import time
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json


class MapManager:

    def __init__(self, map_center=None, zoom=13):
        if map_center is None:
            map_center = [32.072593, 34.776562]
        self.api_key='AIzaSyAUrUNe8n80OAW5Nabxu2Aly_GQeYLFw0k'
        self.map_center = map_center  # center of the map
        self.zoom = zoom  # area of map to display. 13 is pretty good
        self.gmap = gmplot.GoogleMapPlotter(self.map_center[0], self.map_center[1], self.zoom, apikey=self.api_key)
        self.users_trips = dict()  # for each user id in the dictionary, there is a trips dictionary. # for each trip
        # id in the dictionary, there is a trip details struct
        self.users_colors = dict()  # for each user id in the dictionary, there is a matching color

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

    def addUser(self, user_id, color='default'):
        """
        adds a new user to the manager, with an empty trips dictionary
        :param color: color
        :param user_id: user id
        :return:
        """
        if self.doesUserExist(user_id):
            print("this user is already known to the system! id: {}".format(user_id))
            return
        if color == 'default':
            color = self.generateRandomColor()
        self.users_trips[user_id] = dict()
        self.users_colors[user_id] = color

    def addTrip(self, user_id, trip_id, coordinates_list=None):
        """
        adds a new trip to the manager
        :param coordinates_list: coordinates list
        :param user_id: user id
        :param trip_id: trip id
        :return:
        """
        if coordinates_list is None:
            coordinates_list = []
        if not self.doesUserExist(user_id):
            print("this user is not known to the system! id: {}".format(user_id))
            return
        if self.doesTripExist(user_id, trip_id):
            print("this trip is already known to the system! user_id: {}, trip_id: {}".format(user_id, trip_id))
            return

        self.users_trips[user_id][trip_id] = [float(coordinate) for coordinate in coordinates_list]

    def getTrips(self, user_id):
        """
        :param user_id: user id
        :return: trips dictionary
        """
        if not self.doesUserExist(user_id):
            print("this user is not known to the system! id: {}".format(user_id))
            return None

        return self.users_trips[user_id]

    # def getTripDetails(self, user_id, trip_id):
    #     """
    #     :param user_id: user id
    #     :param trip_id: trip id
    #     :return: trip details struct
    #     """
    #     if not self.doesUserExist(user_id):
    #         print("this user is not known to the system! id: {}".format(user_id))
    #         return None
    #     if not self.doesTripExist(user_id, trip_id):
    #         print("this trip is not known to the system! user_id: {}, trip_id: {}".format(user_id, trip_id))
    #         return None

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

        return self.users_trips[user_id][trip_id]

    def addCoordinateToTrip(self, user_id, trip_id, coordinate: Coordinate):
        """
        adds a new coordinate to the trip
        :param user_id: user id
        :param trip_id: trip id
        :param coordinate: new coordinate
        :return:
        """
        if not self.doesUserExist(user_id):
            self.addUser(user_id)
        if not self.doesTripExist(user_id, trip_id):
            self.addTrip(user_id, trip_id, [])
        coordinates_list = self.getTripCoordinates(user_id, trip_id)
        if len(coordinates_list) > 0:
            if coordinates_list[-1] == [coordinate.latitude, coordinate.longitude]:
                return
        self.users_trips[user_id][trip_id].append([float(coordinate.latitude), float(coordinate.longitude)])

    def resetMap(self):
        """
        resets the map to be blank (removes all plots)
        :return:
        """
        self.gmap = gmplot.GoogleMapPlotter(self.map_center[0], self.map_center[1], self.zoom, apikey=self.api_key)

    def drawCoordinates(self, coordinates, color='default', edge_width=3, map=None, user_id='unknown', trip_id='unknown'):
        """
        draws the coordinates on the map
        :param map:
        :param coordinates: coordinates list
        :param color: color of the edges
        :param edge_width: edge width
        :return:
        """
        if len(coordinates) == 0:
            return
        latitude_list = []
        longitude_list = []

        for coordinate in coordinates:
            latitude_list.append(coordinate[0])
            longitude_list.append(coordinate[1])

        if color == 'default':
            color = self.generateRandomColor()
        if map is None:
            map = self.gmap

        details = "User ID: {}, Trip ID: {}".format(user_id, trip_id)
        map.marker(latitude_list[0], longitude_list[0], '#FFFFFF', title=details)
        map.scatter(latitude_list, longitude_list, color, size=15, marker=False)
        map.plot(latitude_list, longitude_list, color, edge_width=edge_width)

    def drawTrip(self, user_id, trip_id, color='default', edge_width=3, map=None):
        """
        draws a user's trip
        :param map:
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

        if color == 'default':
            color = self.users_colors[user_id]

        return self.drawCoordinates(self.getTripCoordinates(user_id, trip_id), color, edge_width, map, user_id=user_id, trip_id=trip_id)

    def drawUserTrips(self, user_id, color='default', edge_width=3, map=None):
        """
        draws all trips of user with the same color
        :param map:
        :param user_id:
        :param color:
        :param edge_width:
        :return:
        """
        if not self.doesUserExist(user_id):
            print("this user is not known to the system! id: {}".format(user_id))
            return
        for trip_id in self.getTrips(user_id):
            self.drawTrip(user_id, trip_id, color, edge_width, map)

    def drawAllTrips(self, map=None):
        """
        draws every trip of every user. trips that belong to the same user have the same random color. also plots an
        legend for the colors
        :return:
        """
        for user_id in self.users_trips:
            color = self.users_colors[user_id]
            self.drawUserTrips(user_id, color, map=map)

    def printMap(self, map=None):
        """
        prints the map
        :return:
        """

        self.printLegend()
        if map is None:
            map = self.gmap
        tmp_gmap = copy.deepcopy(map)
        tmp_gmap.draw("map.html")
        webbrowser.open('file://' + os.path.realpath("map.html"))

    def printLegend(self):
        handles = []
        for user_id in self.users_trips:
            color = self.users_colors[user_id]
            handles.append(mpatches.Patch(color=color, label=user_id))

        plt.figure()
        plt.legend(handles=handles)
        plt.savefig('users_legend.png')
        plt.show()

    def generateMap(self):
        return gmplot.GoogleMapPlotter(self.map_center[0], self.map_center[1], self.zoom, apikey=self.api_key)

    def saveToJson(self):
        print("saving to json")
        with open('users_trips.json', 'w') as fp:
            json.dump(self.users_trips, fp)
        with open('users_colors.json', 'w') as fp:
            json.dump(self.users_colors, fp)

    def loadFromJson(self):
        print("loading from json")
        with open('users_trips.json', 'r') as fp:
            self.users_trips = json.load(fp)
        with open('users_colors.json', 'r') as fp:
            self.users_colors = json.load(fp)

# coordinate = [32.072593, 34.776562]
# manager = MapManager(coordinate)
# mymap = manager.generateMap()
#
# c1=[32.082593, 34.778562]
# c2=[32.081593, 34.696562]
# c3=[32.087593, 34.706562]
#
#
# manager.addUser("sagi")
#
# manager.addTrip("sagi", "trip1")
#
# manager.addCoordinateToTrip("sagi", "trip1", c1)
# manager.addCoordinateToTrip("sagi", "trip1", c2)
# manager.addCoordinateToTrip("sagi", "trip1", c3)
#
# manager.saveToJson()
#
# manager.loadFromJson()
#
# c1=[32.182593, 34.878562]
# c2=[32.181593, 34.796562]
# c3=[32.187593, 34.806562]
#
# manager.addUser("tomer")
#
# manager.addTrip("tomer", "trip1", [])
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

