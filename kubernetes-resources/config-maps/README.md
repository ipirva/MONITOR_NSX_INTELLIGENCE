# Create the configmaps with the scripts to be executed by the cronjobs

```bash
namespace="nsxi-platform-monitoring"
kubectl create configmap druid-broker-config-objects -n $namespace --from-file=../../scripts/druid-broker-config-objects.py
kubectl create configmap druid-broker-unique-correlated-flow-viz -n $namespace --from-file=../../scripts/druid-broker-unique-correlated-flow-viz.py
kubectl create configmap druid-broker-correlated-flow-viz -n $namespace --from-file=../../scripts/druid-broker-correlated-flow-viz.py

kubectl create configmap kafka-over-flow -n $namespace --from-file=../../scripts/kafka-over-flow.sh
kubectl create configmap kafka-raw-flow -n $namespace --from-file=../../scripts/kafka-raw-flow.sh
kubectl create configmap minio-total-data-storage -n $namespace --from-file=../../scripts/minio-total-data-storage.sh
kubectl create configmap pace-normalizedcomputeconfig -n $namespace --from-file=../../scripts/pace-normalizedcomputeconfig.sh
kubectl create configmap pace-groupcomputerelationshipconfig -n $namespace --from-file=../../scripts/pace-groupcomputerelationshipconfig.sh
```