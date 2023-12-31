#!/bin/sh

# Number of compute objects
# This should generally be less than 10000

job_start=$(date +%s)
echo -n "The job started at: " && date -u

pushgateway_endpoint="http://pushgateway-service:8080/metrics/job/nsxi-platform/instance/pace"

pace_normalizedcomputeconfig=0
pace_normalizedcomputeconfig=$(kubectl exec -it postgresql-ha-postgresql-0 -n nsxi-platform -- bash -c 'PGPASSWORD=$POSTGRES_PASSWORD psql -qtAX -d pace -c "SELECT COUNT(*) from normalizedcomputeconfig;"')
# 14
echo "[INFO] pace_normalizedcomputeconfig $pace_normalizedcomputeconfig"

if [ ! -z "$pace_normalizedcomputeconfig" ]
then
    printf "# TYPE pace_normalizedcomputeconfig gauge\npace_normalizedcomputeconfig $pace_normalizedcomputeconfig\n" | curl -v --data-binary @- $pushgateway_endpoint
else
    echo "[ERROR] pace_normalizedcomputeconfig value not set or empty."
fi

job_end=$(date +%s) && echo -n "The job ran for: " && echo $((job_end-job_start)) seconds