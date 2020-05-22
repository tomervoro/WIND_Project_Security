import json

import requests
import threading
import time
import APIs.WIND as wind


def check_status(r):
    if (r.status_code // 100 == 2):
        json_formatted_str = json.dumps(r.json(), indent=2)
        print ("Success! returned: \n{}".format(json_formatted_str))
        with open("results.json", "w") as f:
            f.write(json_formatted_str)
        return True

    if (r.status_code // 100 == 4):
        print ("Error {}! Returned {}".format(r.status_code, r.reason))

    if (r.status_code // 100 == 5):
        print ("Server Error {}! Returned {} ".format(r.status_code, r.reason))

    return False



flag = False
def thread_func(order_id, tid):
    try:
        r = wind.get_order_details(order_id=order_id)
        if r.json().get('result', -1) == 0:
            global flag
            flag = True
            check_status(r)
            print ("Chosen ID: {}".format(order_id))
    except:
        print ("Error for thread {}".format(tid))
        exit()



r = wind.get_order_details(order_id='97e8fb046fb4')
#r = wind.get_user_invitation()
check_status(r)






