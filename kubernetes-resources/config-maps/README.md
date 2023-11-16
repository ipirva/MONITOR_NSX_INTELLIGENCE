# Create the configmaps with the scripts to be executed by the cronjobs

```bash
kubectl create configmap druid-broker-config-objects -n nsxi-platform-monitoring --from-file=../../scripts/druid-broker-config-objects.py
kubectl create configmap druid-broker-unique-correlated-flow-viz -n nsxi-platform-monitoring --from-file=../../scripts/druid-broker-unique-correlated-flow-viz.py
kubectl create configmap druid-broker-correlated-flow-viz -n nsxi-platform-monitoring --from-file=../../scripts/druid-broker-correlated-flow-viz.py
```