#!/bin/sh

# The sum of the folder sizes should typically be less than 60GB * number of minio pods, where /data/minio/druid using the bulk of storage (>90%).
# Typically not a concern except for https://kb.vmware.com/s/article/91696 in 4.0.1.

job_start=$(date +%s)
echo -n "The job started at: " && date -u

pushgateway_endpoint="http://pushgateway-service:8080/metrics/job/nsxi-platform/instance/minio"

minio_total_data_storage=0
minio_total_data_storage=$(kubectl exec minio-0 -n nsxi-platform -- du -k --max-depth=1 /data/minio/ | awk '{ sum += $1 } END { print sum }')
# 770380 in Kilo Bytes
echo "[INFO] minio_total_data_storage $minio_total_data_storage"

if [ ! -z "$minio_total_data_storage" ]
then
    printf "# TYPE minio_total_data_storage gauge\nminio_total_data_storage $minio_total_data_storage\n" | curl -v --data-binary @- $pushgateway_endpoint
else
    echo "[ERROR] minio_total_data_storage value not set or empty."
fi

job_end=$(date +%s) && echo -n "The job ran for: " && echo $((job_end-job_start)) seconds