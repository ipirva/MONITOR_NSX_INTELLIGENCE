#!/usr/bin/env python3

"""
Get total number of config objects in database.
Values for each config type should be less than 10~20 times the number of object in the system.
For example, if there are 5000 VMs in the system, the number of objects should not be more than 100000.
"""

import requests
import json

druid_broker_sql_endpoint = "https://druid-broker.nsxi-platform.svc:8282/druid/v2/sql"
druid_broker_sql_endpoint_headers = { 'Content-Type' : 'application/json', 'Accept' : 'application/json' }
druid_broker_sql_endpoint_data = {"query": "select config_type ,count(*) from pace2druid_manager_realization_config group by config_type"}

pushgateway_endpoint = "http://pushgateway-service:8080/metrics/job/nsxi-platform/instance/druid-broker"
pushgateway_endpoint_headers = {'X-Requested-With': 'Python requests', 'Content-type': 'text/xml'}
pushgateway_endpoint_data = set()

# get total config_objects number
try:
    response = requests.post(druid_broker_sql_endpoint, headers=druid_broker_sql_endpoint_headers, json=druid_broker_sql_endpoint_data, verify=False, timeout=5 )
except Exception as e:
    print(f"[ERROR] While trying to get {druid_broker_sql_endpoint_data} from the endpoint {druid_broker_sql_endpoint}, the returned error was: {e}")
else:
    print(f"[SUCCESS] POST data {druid_broker_sql_endpoint_data} to the endpoint {druid_broker_sql_endpoint}")
    # expected response.content is bytes format b'[{"config_type":"MANAGER_DFW_RULE","EXPR$1":55},{"config_type":"NS_GROUP","EXPR$1":39},{"config_type":"VM","EXPR$1":666}]\n'
    if isinstance(response.content, (bytes, bytearray)):
        content = json.loads(response.content.decode('ascii'))
        config_type = set()
        for index, value in enumerate(content): config_type.add(value['config_type'])
        print(f"[INFO] We got {len(content)} object(s) type: {config_type}")
        # config_objects
        for index, value in enumerate(content): pushgateway_endpoint_data.add(f"druid_config_object_{value['config_type']} {value['EXPR$1']}\n")
finally:
    print(f"[INFO] Status Code: {response.status_code}")
    print(f"[INFO] Response content raw: {response.content}")

# send different config_objects number to pushgateway
def send_config_objects(pushgateway_endpoint_data: set) -> str:
    """
    Pushgateway will receive one pair druid_config_object_OBJECTNAME xxx per config object type
    e.g. config_object_MANAGER_DFW_RULE 55
    config_object_NS_GROUP 39
    config_object_VM 666
    """
    try:
        response = requests.post(pushgateway_endpoint, headers=pushgateway_endpoint_headers, data=pushgateway_endpoint_data, verify=False, timeout=5 )
    except Exception as e:
        print(f"[ERROR] While trying to push data {pushgateway_endpoint_data} to the endpoint {pushgateway_endpoint}, the returned error was: {e}")
    else:
        print(f"[SUCCESS] POST data {pushgateway_endpoint_data} to the endpoint {pushgateway_endpoint}")
        print(f"[INFO] Status Code: {response.status_code}")
        print(f"[INFO] Response content raw: {response.content}")

if len(pushgateway_endpoint_data) > 0:
    for item in pushgateway_endpoint_data:
        send_config_objects(item)