#!/bin/sh

# Kakfa message rate for raw_flow
# This number should be less than 333 for 5 worker nodes or less, and less than 666 for 8 worker nodes

job_start=$(date +%s)
echo -n "The job started at: " && date -u

pushgateway_endpoint="http://pushgateway-service:8080/metrics/job/nsxi-platform/instance/kafka"

namespace="nsxi-platform"
pod_monitor_container="monitor"
pod_monitor=""
pod_monitor=$(kubectl get pods -n $namespace --no-headers=true -o custom-columns=":metadata.name" --field-selector status.phase=Running | egrep "^monitor-[0-9]{1,}.*")
#monitor-8476cd5bb-fpdb2
kafka_raw_flow=0

if [ ! -z "$pod_monitor" ]
then
    kafka_raw_flow=$(kubectl logs $pod_monitor -c $pod_monitor_container -n $namespace | egrep -owi "Kafka Input rate of topic raw_flow is [0-9]{1,}" | tail -n 1 | awk '{print $NF}')
    
    if [ ! -z "$kafka_raw_flow" ]
    then
        echo "# TYPE kafka_raw_flow gauge\nkafka_raw_flow $kafka_raw_flow" | curl -v --data-binary @- $pushgateway_endpoint
    else
        echo "[ERROR] kafka_raw_flow value not set or empty."
    fi

else
    echo "[ERROR] pod_monitor value not set or empty."
fi

job_end=$(date +%s) && echo -n "The job ran for: " && echo $((job_end-job_start)) seconds