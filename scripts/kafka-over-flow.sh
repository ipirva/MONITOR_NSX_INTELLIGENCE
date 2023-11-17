#!/bin/sh

# Kakfa message rate for over_flow
# This number should generally be less than 999

job_start=$(date +%s)
echo -n "The job started at: " && date -u

pushgateway_endpoint="http://pushgateway-service:8080/metrics/job/nsxi-platform/instance/kafka"

namespace="nsxi-platform"
pod_monitor=""
pod_monitor=$(kubectl get pods -n $namespace --no-headers=true -o custom-columns=":metadata.name" --field-selector status.phase=Running | egrep "^monitor-[0-9]{1,}.*")
# monitor-8476cd5bb-fpdb2
pod_monitor_container="monitor"
echo "[INFO] pod_monitor $pod_monitor"

kafka_over_flow=0

if [ ! -z "$pod_monitor" ]
then
    kafka_over_flow=$(kubectl logs $pod_monitor -c $pod_monitor_container -n $namespace | egrep -owi "Kafka Input rate of topic over_flow is [0-9]{1,}" | tail -n 1 | awk '{print $NF}')
    
    echo "[INFO] kafka_over_flow $kafka_over_flow"

    if [ ! -z "$kafka_over_flow" ]
    then
        printf "# TYPE kafka_over_flow gauge\nkafka_over_flow $kafka_over_flow\n" | curl -v --data-binary @- $pushgateway_endpoint
    else
        echo "[ERROR] kafka_over_flow value not set or empty."
    fi

else
    echo "[ERROR] pod_monitor value not set or empty."
fi

job_end=$(date +%s) && echo -n "The job ran for: " && echo $((job_end-job_start)) seconds