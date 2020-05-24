import json
import threading
import time
import http.client
import collections
from enum import Enum
import logging
PRINT_FLAG = True
CITY_COORDINATES = [("32.072789677516006", "34.7866778075695"), ("32.091219", " 34.775575"), ("32.089635", " 34.790858"), ("32.083630", " 34.773860"), ("32.081820", " 34.788971"), ("32.077886", " 34.772398"), ("32.074191", " 34.784707"), ("32.071390", " 34.771087"), ("32.069289", " 34.782164"), ("32.065087", " 34.768286"), ("32.063291", " 34.778506"), ("32.061669", " 34.766633"), ("32.057920", " 34.777858")]
CONNECTIONS = dict()
userAuthTomer = ""
userAuthSagi = "clientId=eb20aac6-fed4-4a5f-82f9-a7943c03867d;userId=2015f39e-63d4-42d5-b896-3cd95d3f0696;ft=99f8913e5136d0fda861a30608d62dc4"
userAuthToUse = userAuthSagi
conn = http.client.HTTPSConnection("api-prod.windride.io")
Coordinate = collections.namedtuple("Coordinate", ["latitude", "longitude"])
OrderDetails = collections.namedtuple("OrderDetails", ["userId", "order_id", "coordinates", "order_status"])
TripDetails = collections.namedtuple("TripDetails", ["coordinates_list"])
_logger = logging.getLogger(__name__)
logging.basicConfig(filename='logfile.log', level=logging.INFO)
fmt="%(funcName)s():%(lineno)i: %(levelname)s   %(message)s"
logging.basicConfig(format=fmt)




class OrderStatus(Enum):
    DONE = 5
    PARKING = 3
    ROLLBACK = 2000
    CANCELLED = 5
    ON_GOING = 2
    RESERVE = 0



def setUp():
    for coordinate in CITY_COORDINATES:
        payload = ''
        headers = {'Authentication': userAuthToUse}
        CONNECTIONS[coordinate] = conn.request("GET", "/v2/boards?latitude={}&longitude={}".format(coordinate[0], coordinate[1]), payload, headers)

def check_status(response):
    try:
        status = response.status_code
    except Exception as _:
        try:
            status = response.status
        except Exception as e:
            raise e

    assert status == 200, response.reason
    return True

