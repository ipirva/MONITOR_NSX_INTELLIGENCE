#!/bin/sh

# Kakfa message rate for over_flow
# This number should generally be less than 999

pushgateway_endpoint="http://pushgateway-service:8080/metrics/job/nsxi-platform/instance/kafka"

namespace="nsxi-platform"
pod_monitor=$(kubectl get pods -n $namespace --no-headers=true -o custom-columns=":metadata.name" --field-selector status.phase=Running | egrep "^monitor-[0-9]{1,}.*"
monitor-8476cd5bb-fpdb2)
pod_monitor_container="monitor"
kafka_over_flow=0
kafka_over_flow=$(kubectl logs $pod -c $pod_monitor_container -n $namespace | egrep -owi "Kafka Input rate of topic over_flow is [0-9]{1,}" | tail -n 1 | awk '{print $NF}')
echo "kafka_over_flow $kafka_over_flow" | curl -v --data-binary @- $pushgateway_endpoint