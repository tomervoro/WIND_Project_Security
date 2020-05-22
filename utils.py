import json
import threading
import time
import http.client
import collections
from enum import Enum
PRINT_FLAG = True

userAuthTomer = ""
userAuthSagi = """clientId=3abd7241-cc27-4c03-85dc-5e7a32c04351;userId=2015f39e-63d4-42d5-b896-3cd95d3f0696;ft=1823d32bfc0a6d6e17f94e75eaf5e3ec"""
userAuthToUse = userAuthSagi
CITY_COORDINATES = [("32.072789677516006", "34.7866778075695"), ("32.072789677516006", "34.7886758075695")]
CONNECTIONS = dict()
conn = http.client.HTTPSConnection("api-prod.windride.io")
Coordinates = collections.namedtuple("Coordinates", ["latitude", "longitude"])
OrderDetails = collections.namedtuple("OrderDetails", ["userId", "coordinates", "order_status"])

class OrderStatus(Enum):
    DONE = 1000
    ROLLBACK = 2000
    CANCELLED = 5


def print_msg(msg):
    if PRINT_FLAG:
        print(msg)

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





"""
LIME





BEARER = 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX3Rva2VuIjoiRjI0STJHR1VUNDZYUiIsImxvZ2luX2NvdW50Ijo4fQ.N6lK0VA7XlbDLixHquJov_MIJjG-PdYALmi55Xd6R88'
import requests

url = "https://web-production.lime.bike/api/rider/v1/bikes/fetch_by_plate_number?plate_number={}"

payload = {}
headers = {
  'App-Version': '2.89.0',
  'User-Agent': 'Android Lime/2.89.0; (com.limebike; build:2.89.0; Android 21) okhttp/3.10.0',
  'X-Device-Token': '9f023478-fe0b-4a4f-a6f5-74b9891c716a',
  'X-Amplitude-Device-ID': 'f2be984b-2435-46f4-919d-5946ec11ace8R',
  'Platform': 'Android',
  'Accept-Language': 'en-US',
  'X-Session-ID': '1587639346318',
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX3Rva2VuIjoiSE1TTkFZRllCWVRJRyIsImxvZ2luX2NvdW50Ijo0fQ.THMS_H3ULvAstAP72ShryxbM4GyVHa1pJHulgGAaxUU',
  'Mobile-Registration-Id': 'f5Q0rhonmWo:APA91bH-roJDegbJDv6HUTPpZcU4tSkuYShn6sIZruTaKLY8Dh1ry8TwvXOTGMTJ2qsFIJ5UERNzzy2af5L82De_GaUHqR33UqByOWV-SYcprwbyWDJr-TmVwgSRPwhjDwuL82nJdK5u',
  'Host': 'web-production.lime.bike',
  'Connection': 'close',
  'Accept-Encoding': 'gzip, deflate',
  'Cookie': '__cfduid=d2bcd538462178572ba7c02886fdac26b1585215093; _limebike-web_session=KqBRvwVm2rD3hn%2B%2FW1VsqJPOV1Ut4VW4FdC%2FBgJ7fcffPDzDrQ2V5e0kcEe%2FkOdZxq%2FvXmmn0oOwe2kdx%2BG7%2FJ0b%2BJ3wT9Q%2FrbbAoYl8hTZmWhB8%2BD%2BSMRujMbvtXMYtdfGz5jb27U6ssWHXSS8V2YnXAk0gJH2lt2hTZ5UZPKRhUlwkHpYLZoduYI5%2B4oTIL%2B%2Be3uvBQf5s6XOfXBZezshKblnf1SXUQlvPHyPfKJFJd130BYEQQ9siERbNVPtT9IdSxeZjwE8x4oQrwy%2FieEg0iLNT5knb31L0Kp%2FcQUAPgcIlrBEXpo4s6U8WV3GMSLNeEVaAi%2B32WfRkTtLMnOPQksH%2Bfveoz89cQWP2vFc%2FNm70BDwvzJvOUv9xer7HOEboT0mn2ou47PbBxzb0Z%2F66VXJi637kL9q44T%2FWAFNStikleC2Do9PRjYY8zTs72JJZwsAeOPGjSh8X9IMDaiMf%2FBVNoAv2b7fVK%2Fc8QlrE--ZqS8unQAhr0aQlRZ--RPsXG1K8d5pu8CEI4vRjOA%3D%3D'
}
alpha = 'abcdefghijklmnopqrstuvwxyz'.upper() #[str(i) for i in range(0,10)] #
end_plate = 'UVQ' #'657' #

def send_req(plate):
    try:
        response = requests.request("GET", url.format(plate), headers=headers, data=payload)
        if response.status_code == 200:
            data = response.text.encode('utf8')
            if data != b'null':
                print("For plate: ", plate)
                print("Got response:", json.loads(response.text.encode('utf8')))
    except:
        print("1")

def find_plate():
    lst = []
    for x in alpha:
        for y in alpha:
            for z in alpha:
                plate= x+y+z+end_plate
                t = threading.Thread(target=send_req, args=(plate,))
                t.start()
                lst.append(t)
        for t in lst:
            t.join()
        lst = []
        print("X={} Y={} ".format(x,y))



"""