#!/bin/sh

# Number of group compute relations
# This should be less than 1 million and generally less than 100k. 
# If customer is on version older than 4.1.1 and seeing a lot of entries, increase clean up period and manually clean up entries
# Upgrading to 4.1.1 should fix the issue

pushgateway_endpoint="http://pushgateway-service:8080/metrics/job/nsxi-platform/instance/pace"

pace_groupcomputerelationshipconfig=0
pace_groupcomputerelationshipconfig=$(kubectl exec -it postgresql-ha-postgresql-0 -n nsxi-platform -- bash -c 'PGPASSWORD=$POSTGRES_PASSWORD psql -qtAX -d pace -c "SELECT COUNT(*) from groupcomputerelationshipconfig;"')
# 33

if [ ! -z "$pace_groupcomputerelationshipconfig" ]
then
    echo "pace_groupcomputerelationshipconfig $pace_groupcomputerelationshipconfig" | curl -v --data-binary @- $pushgateway_endpoint
else
    echo "[ERROR] pace_groupcomputerelationshipconfig value not set or empty."
fi