#!/usr/bin/env python3

""" 
Get correlated_flow_viz number of segments from Druid
This number should be less than 80 million * number of worker nodes. 
If already breaching, or approaching the threshold, it's recommended to scale out analytics.
"""

import requests
import json

druid_broker_sql_endpoint = "https://druid-broker.nsxi-platform.svc:8282/druid/v2/sql"
druid_broker_sql_endpoint_headers = { 'Content-Type' : 'application/json', 'Accept' : 'application/json' }
druid_broker_sql_endpoint_data = {"query": "select count(*) from correlated_flow_viz"}

pushgateway_endpoint = "http://pushgateway-service:8080/metrics/job/nsxi-platform/instance/druid-broker"
pushgateway_endpoint_headers = {'X-Requested-With': 'Python requests', 'Content-type': 'text/xml'}
pushgateway_endpoint_data = "correlated_flow_viz 0\n"

# get correlated_flow_viz number of segments from Druid
try:
    response = requests.post(druid_broker_sql_endpoint, headers=druid_broker_sql_endpoint_headers, json=druid_broker_sql_endpoint_data, verify=False, timeout=5 )
except Exception as e:
    print(f"[ERROR] While trying to get {druid_broker_sql_endpoint_data} from the endpoint {druid_broker_sql_endpoint}, the returned error was: {e}")
else:
    print(f"[SUCCESS] POST data {druid_broker_sql_endpoint_data} to the endpoint {druid_broker_sql_endpoint}")
    # expected response.content is bytes format b'[{"EXPR$0":12317}]\n'
    if isinstance(response.content, (bytes, bytearray)):
        content = json.loads(response.content.decode('ascii'))
        # correlated_flow_viz segments
        correlated_flow_viz = content[0]['EXPR$0']
        pushgateway_endpoint_data = f"correlated_flow_viz {correlated_flow_viz}\n"
finally:
    print(pushgateway_endpoint_data)

    print(f"[INFO] Status Code: {response.status_code}")
    print(f"[INFO] Response content raw: {response.content}")

# send correlated_flow_viz number of segments to pushgateway
try:
    response = requests.post(pushgateway_endpoint, headers=pushgateway_endpoint_headers, data=pushgateway_endpoint_data, verify=False, timeout=5 )
except Exception as e:
    print(f"[ERROR] While trying to push data {pushgateway_endpoint_data} to the endpoint {pushgateway_endpoint}, the returned error was: {e}")
else:
    print(f"[SUCCESS] POST data {pushgateway_endpoint_data} to the endpoint {pushgateway_endpoint}")
    print(f"[INFO] Status Code: {response.status_code}")
    print(f"[INFO] Response content raw: {response.content}")