#!/usr/bin/env python3

""" 
Get correlated_flow_viz number of segments from Druid
This number should be less than 80 million * number of worker nodes. 
If already breaching, or approaching the threshold, it's recommended to scale out analytics.
"""

import requests
import json
from time import time
from datetime import datetime

def get_time(format: str = "timestamp") -> str:
    # return time
    # (default) format = timestamp -> it returns integer timestamp (seconds)
    # format = utc -> it returns UTC time as 2023-11-17 16:56:43
    if format == "timestamp":
        return int(time())
    if format ==  "utc":
        return f"{datetime.utcfromtimestamp(int(time()))} UTC"
    return ""

def send_stdout(message: str = "N/A", type: str = "INFO") -> str:
    # sends message to the std output
    # types INFO, ERROR, SUCCESS
    return f"[{type.upper()}] [{get_time(format = 'utc')}] {message}"

job_start = get_time(); send_stdout(message=f"The job started at: {get_time(format = 'utc')}", type="INFO")

druid_broker_sql_endpoint = "https://druid-broker.nsxi-platform.svc:8282/druid/v2/sql"
druid_broker_sql_endpoint_headers = { 'Content-Type' : 'application/json', 'Accept' : 'application/json' }
druid_broker_sql_endpoint_data = {"query": "select count(*) from correlated_flow_viz"}

pushgateway_endpoint = "http://pushgateway-service:8080/metrics/job/nsxi-platform/instance/druid-broker"
pushgateway_endpoint_headers = {'X-Requested-With': 'Python requests', 'Content-type': 'text/xml'}
pushgateway_endpoint_data = "druid_correlated_flow_viz 0\n"

# get correlated_flow_viz number of segments from Druid
try:
    response = requests.post(druid_broker_sql_endpoint, headers=druid_broker_sql_endpoint_headers, json=druid_broker_sql_endpoint_data, verify=False, timeout=5 )
except Exception as e:
    send_stdout(message=f"While trying to get {druid_broker_sql_endpoint_data} from the endpoint {druid_broker_sql_endpoint}, the returned error was: {e}", type="ERROR")
else:
    send_stdout(message=f"POST data {druid_broker_sql_endpoint_data} to the endpoint {druid_broker_sql_endpoint}", type="SUCCESS")
    # expected response.content is bytes format b'[{"EXPR$0":12317}]\n'
    if isinstance(response.content, (bytes, bytearray)):
        content = json.loads(response.content.decode('ascii'))
        # correlated_flow_viz segments
        correlated_flow_viz = content[0]['EXPR$0']
        pushgateway_endpoint_data = f"# TYPE druid_correlated_flow_viz gauge\ndruid_correlated_flow_viz {correlated_flow_viz}\n"
finally:
    print(pushgateway_endpoint_data)
    send_stdout(message=f"Status Code: {response.status_code}", type="INFO")
    send_stdout(message=f"Response content raw: {response.content}", type="INFO")

# send correlated_flow_viz number of segments to pushgateway
try:
    response = requests.post(pushgateway_endpoint, headers=pushgateway_endpoint_headers, data=pushgateway_endpoint_data, verify=False, timeout=5 )
except Exception as e:
    send_stdout(message=f"While trying to push data {pushgateway_endpoint_data} to the endpoint {pushgateway_endpoint}, the returned error was: {e}", type="ERROR")
else:
    send_stdout(message=f"POST data {pushgateway_endpoint_data} to the endpoint {pushgateway_endpoint}", type="SUCCESS")
    send_stdout(message=f"Status Code: {response.status_code}", type="INFO")
    send_stdout(message=f"Response content raw: {response.content}", type="INFO")

job_end = int(time()); send_stdout(message=f"The job ran for: {job_end - job_start} second(s)", type="INFO")