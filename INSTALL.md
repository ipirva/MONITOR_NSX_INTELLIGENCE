# Deployment Steps

This project uses: Prometheus, Pushgateway and Grafana.

Prometheus and Pushgateway are deployed under the Kubernetes namespace nsxi-platform-monitoring
Grafana is deployed under the Kubernetes namespace grafana

1. Kubernetes Service Account
The prerequisite folder contains authorization.yaml manifest to create the Service Account needed by some of the Kubernetes deployed cronjobs.

```bash
kubectl apply -f authorization.yaml
```

2. Kubernetes NetworkPolicy
Kubernetes CronJobs are used to query for NSX Intelligence running parameters. Some of the Kubernetes CronJobs need to do API requests on NSX Intelligence services. Specific networking flows must be allowed by the Kubernetes NetworkPolicies used within the NSX Intelligence deployment.

To address this for druid-broker, inside the prerequisite folder the file druid-broker_np_patch.txt specifies the needed patch for the druid-broker NetworkPolicy

```bash
kubectl patch networkpolicy.networking.k8s.io druid-broker -n nsxi-platform --type='json' -p='[ { "op": "add", "path": "/spec/ingress/0/from/1", "value": { "namespaceSelector": { "matchLabels": { "kubernetes.io/metadata.name": "nsxi-platform-monitoring" } } } } ]'
```

3. Prometheus and Pushgateway Deployemnt
All the needed Kubernetes manifests (Namespace, Deployment / Replicaset, PVC, NodePort Service) are available under the folder prometheus

```bash
kubectl apply -f prometheus/
```

Prometheus and Pushgateway endpoints are exposed as ClusterIP, NodePort services.

Prometheus ClusterIP service: prometheus-service.nsxi-platform-monitoring:8080
Prometheus NodePort 30000

Pushgateway ClusterIP service: pushgateway-service.nsxi-platform-monitoring:8080
Pushgateway NodePort 31000

4. Grafana Deployemnt
All the needed Kubernetes manifests (Namespace, Deployment / Replicaset, PVC, NodePort Service) are available under the folder grafana

```bash
kubectl apply -f grafana/
```

Grafana endpoint is exposed as ClusterIP, NodePort services.

Grafana ClusterIP service: grafana-service.grafana:3000
Grafana NodePort 32000

5. Kubernetes CronJobs
The NSX Intelligence monitored parameters are grabbed by Kubernetes CronJobs and pushed (API calls) to Pushgateway.
Prometheus will scrap the metrics from Pushgateway and will store them in its internal/native TSDB.

The docker images used to run the CronJobs are defined under the images folder and published actually to Docker Hub.

The scripts which run inside the CronJobs are saved inside Kubernetes Configmaps and they are mounted by the CronJobs at execution time.
The scripts' sources used to create the Configmaps are available under the [scripts](https://github.com/ipirva/MONITOR_NSX_INTELLIGENCE/tree/main/scripts) folder

[Deploy the Kubernetes Configmaps](https://github.com/ipirva/MONITOR_NSX_INTELLIGENCE/blob/main/kubernetes-resources/config-maps/README.md)

Deploy the Kubernetes CronJobs:
```bash
kubectl apply -f kubernetes-resources/cronjobs/
```

6. Import the Grafana Dashboards
Connect to Grafana web UI and import the Dashboards from the JSON sources found inside the folder grafana_dashboard
The available Dashboards are:

*6.1. Prometheus and Pushgateway running metrics (CPU, Memory, Prometheus WAL size, Prometheus TSDB size)
*6.2. NSX Intelligence metrics

