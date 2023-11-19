# MONITOR_NSX_INTELLIGENCE

Get some NSXI parameters monitored. 
The metrics are exported to Prometheus via Pushgateway.
The metrics can be viewed inside Grafana. An exported Dashboard is shared.

Prometheus ClusterIP service: prometheus-service.nsxi-platform-monitoring:8080
Prometheus NodePort 30000

Pushgateway ClusterIP service: pushgateway-service.nsxi-platform-monitoring:8080
Pushgateway NodePort 31000

Grafana ClusterIP service: grafana-service.grafana:3000
Grafana NodePort 32000

1. Kakfa message rate for raw_flow. Prometheus metric: kafka_raw_flow
2. Kakfa message rate for over_flow. Prometheus metric: kafka_over_flow
3. Number of compute objects. Prometheus metric: pace_normalizedcomputeconfig
4. Number of group compute relations. Prometheus metric: pace_groupcomputerelationshipconfig
5. Minio global data storage used. Prometheus metric: minio_total_data_storage
6. Druid total number of config objects in database. Prometheus metrics: druid_config_object_XXX
7. Druid correlated_flow_viz number of segments. Prometheus metric: druid_correlated_flow_viz
8. Druid unique correlated_flow_viz number of segments. Prometheus metric: druid_correlated_flow_viz_unique

This entire repository content is not supported by VMware the company.