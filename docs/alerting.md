# Alerting — referencia

> Generado por `scripts/gen-alerting-doc.py` desde el chart `kube-prometheus-stack 88.3.0` y `values/kube-prometheus-stack/values.yaml`.

**146 alertas** (critical: 36 · warning: 101 · info: 7 · none: 2) y **96 recording rules**, repartidas en 33 objetos `PrometheusRule`: 30 los genera el chart, 3 son propios del repo.

## Ruteo

Primera coincidencia gana: una alerta cae en **una sola** rama.

- **raiz** → `telegram`  · group_by=alertname,namespace · group_wait=30s · group_interval=5m · repeat_interval=6h
  - **alertname =~ "Watchdog|InfoInhibitor"** → `null`
  - **alertname = "TargetDown"** → `telegram`  · group_by=alertname
  - **severity = "critical"** → `telegram`  · repeat_interval=1h

## Receivers

### `null`

Sin destino: descarta la alerta a propósito.

### `telegram`

- tipo: **telegram**
  - `bot_token_file`: `/etc/alertmanager/secrets/alertmanager-telegram/bot-token`
  - `chat_id`: `7277492400`
  - `message`: `(ver template abajo)`
  - `parse_mode`: `HTML`
  - `send_resolved`: `True`

## Inhibit rules

Silencian la alerta *target* mientras exista la *source* con las mismas labels de `equal`.

| # | source | target | equal |
|---|--------|--------|-------|
| 1 | `severity = "critical"` | `severity =~ "warning|info"` | `namespace, alertname` |
| 2 | `severity = "warning"` | `severity = "info"` | `namespace, alertname` |
| 3 | `alertname = "InfoInhibitor"` | `severity = "info"` | `namespace` |

## Templates

### `telegram.tmpl`

```gotemplate
{{ define "tg.esc" }}{{ . | reReplaceAll "&" "&amp;" | reReplaceAll "<" "&lt;" | reReplaceAll ">" "&gt;" }}{{ end }}

{{ define "telegram.message" }}
{{- if eq .Status "firing" }}🔴 <b>FIRING ({{ .Alerts.Firing | len }})</b>
{{- else }}🟢 <b>RESOLVED ({{ .Alerts.Resolved | len }})</b>
{{- end }} — {{ template "tg.esc" .CommonLabels.alertname }}
{{- /* telegram corta en 4096 chars: tope de 6 alertas por mensaje */}}
{{ range $i, $a := .Alerts.Firing }}{{ if lt $i 6 }}
<b>{{ .Labels.severity | toUpper }}</b> {{ template "tg.esc" .Annotations.summary }}
{{- with .Annotations.description }}
{{ template "tg.esc" . }}
{{- end }}
{{- with .Labels.namespace }} <code>ns={{ . }}</code>{{ end }}
{{- with .Labels.pod }} <code>pod={{ . }}</code>{{ end }}
{{- with .Labels.node }} <code>node={{ . }}</code>{{ end }}
{{- with .Labels.persistentvolumeclaim }} <code>pvc={{ . }}</code>{{ end }}
{{ end }}{{ end }}
{{- if gt (len .Alerts.Firing) 6 }}
<i>Showing 6 of {{ len .Alerts.Firing }}</i>
{{ end }}
{{- with .Alerts.Resolved }}
{{ range $i, $a := . }}{{ if lt $i 6 }}✅ {{ template "tg.esc" .Annotations.summary }}
{{ end }}{{ end }}
{{- if gt (len .) 6 }}<i>Showing 6 of {{ len . }} resolved</i>
{{ end }}
{{- end }}
<a href="{{ .ExternalURL }}">Alertmanager</a>
{{- end }}
```

## Alertas

### Índice

| Alerta | Sev | for | Grupo |
|--------|-----|-----|-------|
| [AlertmanagerClusterCrashlooping](#alertmanagerclustercrashlooping) | `critical` | `5m` | alertmanager.rules |
| [AlertmanagerClusterDown](#alertmanagerclusterdown) | `critical` | `5m` | alertmanager.rules |
| [AlertmanagerClusterFailedToSendAlerts](#alertmanagerclusterfailedtosendalerts) | `critical` | `5m` | alertmanager.rules |
| [AlertmanagerConfigInconsistent](#alertmanagerconfiginconsistent) | `critical` | `20m` | alertmanager.rules |
| [AlertmanagerFailedReload](#alertmanagerfailedreload) | `critical` | `10m` | alertmanager.rules |
| [AlertmanagerMembersInconsistent](#alertmanagermembersinconsistent) | `critical` | `15m` | alertmanager.rules |
| [KubeAPIDown](#kubeapidown) | `critical` | `15m` | kubernetes-system-apiserver |
| [KubeAPIErrorBudgetBurn](#kubeapierrorbudgetburn) | `critical` | `2m` | kube-apiserver-slos |
| [KubeAPIErrorBudgetBurn](#kubeapierrorbudgetburn) | `critical` | `15m` | kube-apiserver-slos |
| [KubeClientCertificateExpiration](#kubeclientcertificateexpiration) | `critical` | `5m` | kubernetes-system-apiserver |
| [KubePersistentVolumeErrors](#kubepersistentvolumeerrors) | `critical` | `5m` | kubernetes-storage |
| [KubePersistentVolumeFillingUp](#kubepersistentvolumefillingup) | `critical` | `1m` | kubernetes-storage |
| [KubePersistentVolumeInodesFillingUp](#kubepersistentvolumeinodesfillingup) | `critical` | `1m` | kubernetes-storage |
| [KubeStateMetricsListErrors](#kubestatemetricslisterrors) | `critical` | `15m` | kube-state-metrics |
| [KubeStateMetricsShardingMismatch](#kubestatemetricsshardingmismatch) | `critical` | `15m` | kube-state-metrics |
| [KubeStateMetricsShardsMissing](#kubestatemetricsshardsmissing) | `critical` | `15m` | kube-state-metrics |
| [KubeStateMetricsWatchErrors](#kubestatemetricswatcherrors) | `critical` | `15m` | kube-state-metrics |
| [KubeletClientCertificateExpiration](#kubeletclientcertificateexpiration) | `critical` | `-` | kubernetes-system-kubelet |
| [KubeletDown](#kubeletdown) | `critical` | `15m` | kubernetes-system-kubelet |
| [KubeletServerCertificateExpiration](#kubeletservercertificateexpiration) | `critical` | `-` | kubernetes-system-kubelet |
| [LonghornBackupFailed](#longhornbackupfailed) | `critical` | `5m` | longhorn |
| [LonghornVolumeStatusCritical](#longhornvolumestatuscritical) | `critical` | `5m` | longhorn |
| [NodeFileDescriptorLimit](#nodefiledescriptorlimit) | `critical` | `15m` | node-exporter |
| [NodeFilesystemAlmostOutOfFiles](#nodefilesystemalmostoutoffiles) | `critical` | `1h` | node-exporter |
| [NodeFilesystemAlmostOutOfSpace](#nodefilesystemalmostoutofspace) | `critical` | `30m` | node-exporter |
| [NodeFilesystemFilesFillingUp](#nodefilesystemfilesfillingup) | `critical` | `1h` | node-exporter |
| [NodeFilesystemSpaceFillingUp](#nodefilesystemspacefillingup) | `critical` | `1h` | node-exporter |
| [NodeRAIDDegraded](#noderaiddegraded) | `critical` | `15m` | node-exporter |
| [PrometheusBadConfig](#prometheusbadconfig) | `critical` | `10m` | prometheus |
| [PrometheusErrorSendingAlertsToAnyAlertmanager](#prometheuserrorsendingalertstoanyalertmanager) | `critical` | `15m` | prometheus |
| [PrometheusRemoteStorageFailures](#prometheusremotestoragefailures) | `critical` | `15m` | prometheus |
| [PrometheusRemoteWriteBehind](#prometheusremotewritebehind) | `critical` | `15m` | prometheus |
| [PrometheusRuleFailures](#prometheusrulefailures) | `critical` | `15m` | prometheus |
| [PrometheusTargetSyncFailure](#prometheustargetsyncfailure) | `critical` | `5m` | prometheus |
| [PveGuestDown](#pveguestdown) | `critical` | `5m` | pve |
| [PveNodeDown](#pvenodedown) | `critical` | `5m` | pve |
| [AlertmanagerClusterFailedPeers](#alertmanagerclusterfailedpeers) | `warning` | `15m` | alertmanager.rules |
| [AlertmanagerClusterFailedToSendAlerts](#alertmanagerclusterfailedtosendalerts) | `warning` | `5m` | alertmanager.rules |
| [AlertmanagerFailedToSendAlerts](#alertmanagerfailedtosendalerts) | `warning` | `5m` | alertmanager.rules |
| [ConfigReloaderSidecarErrors](#configreloadersidecarerrors) | `warning` | `10m` | config-reloaders |
| [KubeAPIErrorBudgetBurn](#kubeapierrorbudgetburn) | `warning` | `1h` | kube-apiserver-slos |
| [KubeAPIErrorBudgetBurn](#kubeapierrorbudgetburn) | `warning` | `3h` | kube-apiserver-slos |
| [KubeAPIInstanceUnreachable](#kubeapiinstanceunreachable) | `warning` | `15m` | kubernetes-system-apiserver |
| [KubeAPITerminatedRequests](#kubeapiterminatedrequests) | `warning` | `5m` | kubernetes-system-apiserver |
| [KubeAggregatedAPIDown](#kubeaggregatedapidown) | `warning` | `5m` | kubernetes-system-apiserver |
| [KubeAggregatedAPIErrors](#kubeaggregatedapierrors) | `warning` | `10m` | kubernetes-system-apiserver |
| [KubeCPUOvercommit](#kubecpuovercommit) | `warning` | `10m` | kubernetes-resources |
| [KubeCPUQuotaOvercommit](#kubecpuquotaovercommit) | `warning` | `5m` | kubernetes-resources |
| [KubeClientCertificateExpiration](#kubeclientcertificateexpiration) | `warning` | `5m` | kubernetes-system-apiserver |
| [KubeClientErrors](#kubeclienterrors) | `warning` | `15m` | kubernetes-system |
| [KubeContainerWaiting](#kubecontainerwaiting) | `warning` | `1h` | kubernetes-apps |
| [KubeDaemonSetMisScheduled](#kubedaemonsetmisscheduled) | `warning` | `15m` | kubernetes-apps |
| [KubeDaemonSetNotScheduled](#kubedaemonsetnotscheduled) | `warning` | `10m` | kubernetes-apps |
| [KubeDaemonSetRolloutStuck](#kubedaemonsetrolloutstuck) | `warning` | `15m` | kubernetes-apps |
| [KubeDeploymentGenerationMismatch](#kubedeploymentgenerationmismatch) | `warning` | `15m` | kubernetes-apps |
| [KubeDeploymentReplicasMismatch](#kubedeploymentreplicasmismatch) | `warning` | `15m` | kubernetes-apps |
| [KubeDeploymentRolloutStuck](#kubedeploymentrolloutstuck) | `warning` | `15m` | kubernetes-apps |
| [KubeHpaMaxedOut](#kubehpamaxedout) | `warning` | `15m` | kubernetes-apps |
| [KubeHpaReplicasMismatch](#kubehpareplicasmismatch) | `warning` | `15m` | kubernetes-apps |
| [KubeJobFailed](#kubejobfailed) | `warning` | `15m` | kubernetes-apps |
| [KubeJobNotCompleted](#kubejobnotcompleted) | `warning` | `-` | kubernetes-apps |
| [KubeMemoryOvercommit](#kubememoryovercommit) | `warning` | `10m` | kubernetes-resources |
| [KubeMemoryQuotaOvercommit](#kubememoryquotaovercommit) | `warning` | `5m` | kubernetes-resources |
| [KubeNodeNotReady](#kubenodenotready) | `warning` | `15m` | kubernetes-system-kubelet |
| [KubeNodeReadinessFlapping](#kubenodereadinessflapping) | `warning` | `15m` | kubernetes-system-kubelet |
| [KubeNodeUnreachable](#kubenodeunreachable) | `warning` | `15m` | kubernetes-system-kubelet |
| [KubePdbNotEnoughHealthyPods](#kubepdbnotenoughhealthypods) | `warning` | `15m` | kubernetes-apps |
| [KubePersistentVolumeFillingUp](#kubepersistentvolumefillingup) | `warning` | `1h` | kubernetes-storage |
| [KubePersistentVolumeInodesFillingUp](#kubepersistentvolumeinodesfillingup) | `warning` | `1h` | kubernetes-storage |
| [KubePodCrashLooping](#kubepodcrashlooping) | `warning` | `15m` | kubernetes-apps |
| [KubePodNotReady](#kubepodnotready) | `warning` | `15m` | kubernetes-apps |
| [KubeQuotaExceeded](#kubequotaexceeded) | `warning` | `15m` | kubernetes-resources |
| [KubeStatefulSetGenerationMismatch](#kubestatefulsetgenerationmismatch) | `warning` | `15m` | kubernetes-apps |
| [KubeStatefulSetReplicasMismatch](#kubestatefulsetreplicasmismatch) | `warning` | `15m` | kubernetes-apps |
| [KubeStatefulSetUpdateNotRolledOut](#kubestatefulsetupdatenotrolledout) | `warning` | `15m` | kubernetes-apps |
| [KubeVersionMismatch](#kubeversionmismatch) | `warning` | `15m` | kubernetes-system |
| [KubeletClientCertificateExpiration](#kubeletclientcertificateexpiration) | `warning` | `-` | kubernetes-system-kubelet |
| [KubeletClientCertificateRenewalErrors](#kubeletclientcertificaterenewalerrors) | `warning` | `15m` | kubernetes-system-kubelet |
| [KubeletInstanceUnreachable](#kubeletinstanceunreachable) | `warning` | `15m` | kubernetes-system-kubelet |
| [KubeletPlegDurationHigh](#kubeletplegdurationhigh) | `warning` | `5m` | kubernetes-system-kubelet |
| [KubeletPodStartUpLatencyHigh](#kubeletpodstartuplatencyhigh) | `warning` | `15m` | kubernetes-system-kubelet |
| [KubeletServerCertificateExpiration](#kubeletservercertificateexpiration) | `warning` | `-` | kubernetes-system-kubelet |
| [KubeletServerCertificateRenewalErrors](#kubeletservercertificaterenewalerrors) | `warning` | `15m` | kubernetes-system-kubelet |
| [LonghornBackupStale](#longhornbackupstale) | `warning` | `30m` | longhorn |
| [LonghornDiskNotSchedulable](#longhorndisknotschedulable) | `warning` | `15m` | longhorn |
| [LonghornVolumeStatusWarning](#longhornvolumestatuswarning) | `warning` | `5m` | longhorn |
| [NodeBondingDegraded](#nodebondingdegraded) | `warning` | `5m` | node-exporter |
| [NodeClockNotSynchronising](#nodeclocknotsynchronising) | `warning` | `10m` | node-exporter |
| [NodeClockSkewDetected](#nodeclockskewdetected) | `warning` | `10m` | node-exporter |
| [NodeDiskIOSaturation](#nodediskiosaturation) | `warning` | `30m` | node-exporter |
| [NodeFileDescriptorLimit](#nodefiledescriptorlimit) | `warning` | `15m` | node-exporter |
| [NodeFilesystemAlmostOutOfFiles](#nodefilesystemalmostoutoffiles) | `warning` | `1h` | node-exporter |
| [NodeFilesystemAlmostOutOfSpace](#nodefilesystemalmostoutofspace) | `warning` | `30m` | node-exporter |
| [NodeFilesystemFilesFillingUp](#nodefilesystemfilesfillingup) | `warning` | `1h` | node-exporter |
| [NodeFilesystemSpaceFillingUp](#nodefilesystemspacefillingup) | `warning` | `1h` | node-exporter |
| [NodeHighNumberConntrackEntriesUsed](#nodehighnumberconntrackentriesused) | `warning` | `-` | node-exporter |
| [NodeMemoryHighUtilization](#nodememoryhighutilization) | `warning` | `15m` | node-exporter |
| [NodeMemoryMajorPagesFaults](#nodememorymajorpagesfaults) | `warning` | `15m` | node-exporter |
| [NodeNetworkInterfaceFlapping](#nodenetworkinterfaceflapping) | `warning` | `2m` | node-network |
| [NodeNetworkReceiveErrs](#nodenetworkreceiveerrs) | `warning` | `1h` | node-exporter |
| [NodeNetworkTransmitErrs](#nodenetworktransmiterrs) | `warning` | `1h` | node-exporter |
| [NodeRAIDDiskFailure](#noderaiddiskfailure) | `warning` | `-` | node-exporter |
| [NodeSystemSaturation](#nodesystemsaturation) | `warning` | `15m` | node-exporter |
| [NodeSystemdServiceCrashlooping](#nodesystemdservicecrashlooping) | `warning` | `15m` | node-exporter |
| [NodeSystemdServiceFailed](#nodesystemdservicefailed) | `warning` | `5m` | node-exporter |
| [NodeTextFileCollectorScrapeError](#nodetextfilecollectorscrapeerror) | `warning` | `-` | node-exporter |
| [PrometheusDuplicateTimestamps](#prometheusduplicatetimestamps) | `warning` | `10m` | prometheus |
| [PrometheusErrorSendingAlertsToSomeAlertmanagers](#prometheuserrorsendingalertstosomealertmanagers) | `warning` | `15m` | prometheus |
| [PrometheusHighQueryLoad](#prometheushighqueryload) | `warning` | `15m` | prometheus |
| [PrometheusKubernetesListWatchFailures](#prometheuskuberneteslistwatchfailures) | `warning` | `15m` | prometheus |
| [PrometheusLabelLimitHit](#prometheuslabellimithit) | `warning` | `15m` | prometheus |
| [PrometheusMissingRuleEvaluations](#prometheusmissingruleevaluations) | `warning` | `15m` | prometheus |
| [PrometheusNotConnectedToAlertmanagers](#prometheusnotconnectedtoalertmanagers) | `warning` | `10m` | prometheus |
| [PrometheusNotIngestingSamples](#prometheusnotingestingsamples) | `warning` | `10m` | prometheus |
| [PrometheusNotificationQueueRunningFull](#prometheusnotificationqueuerunningfull) | `warning` | `15m` | prometheus |
| [PrometheusOperatorListErrors](#prometheusoperatorlisterrors) | `warning` | `15m` | prometheus-operator |
| [PrometheusOperatorNodeLookupErrors](#prometheusoperatornodelookuperrors) | `warning` | `10m` | prometheus-operator |
| [PrometheusOperatorNotReady](#prometheusoperatornotready) | `warning` | `5m` | prometheus-operator |
| [PrometheusOperatorReconcileErrors](#prometheusoperatorreconcileerrors) | `warning` | `10m` | prometheus-operator |
| [PrometheusOperatorRejectedResources](#prometheusoperatorrejectedresources) | `warning` | `5m` | prometheus-operator |
| [PrometheusOperatorStatusUpdateErrors](#prometheusoperatorstatusupdateerrors) | `warning` | `10m` | prometheus-operator |
| [PrometheusOperatorSyncFailed](#prometheusoperatorsyncfailed) | `warning` | `10m` | prometheus-operator |
| [PrometheusOperatorWatchErrors](#prometheusoperatorwatcherrors) | `warning` | `15m` | prometheus-operator |
| [PrometheusOutOfOrderTimestamps](#prometheusoutofordertimestamps) | `warning` | `10m` | prometheus |
| [PrometheusRemoteWriteDesiredShards](#prometheusremotewritedesiredshards) | `warning` | `15m` | prometheus |
| [PrometheusSDRefreshFailure](#prometheussdrefreshfailure) | `warning` | `20m` | prometheus |
| [PrometheusScrapeBodySizeLimitHit](#prometheusscrapebodysizelimithit) | `warning` | `15m` | prometheus |
| [PrometheusScrapeSampleLimitHit](#prometheusscrapesamplelimithit) | `warning` | `15m` | prometheus |
| [PrometheusTSDBCompactionsFailing](#prometheustsdbcompactionsfailing) | `warning` | `4h` | prometheus |
| [PrometheusTSDBReloadsFailing](#prometheustsdbreloadsfailing) | `warning` | `4h` | prometheus |
| [PrometheusTargetLimitHit](#prometheustargetlimithit) | `warning` | `15m` | prometheus |
| [PveClusterNotQuorate](#pveclusternotquorate) | `warning` | `5m` | pve |
| [PveContainerDiskAlmostFull](#pvecontainerdiskalmostfull) | `warning` | `30m` | pve |
| [PveGuestNotBackedUp](#pveguestnotbackedup) | `warning` | `1h` | pve |
| [PveScrapeFailed](#pvescrapefailed) | `warning` | `10m` | pve |
| [PveStorageAlmostFull](#pvestoragealmostfull) | `warning` | `30m` | pve |
| [TargetDown](#targetdown) | `warning` | `10m` | general.rules |
| [CPUThrottlingHigh](#cputhrottlinghigh) | `info` | `15m` | kubernetes-resources |
| [KubeNodeEviction](#kubenodeeviction) | `info` | `0s` | kubernetes-system-kubelet |
| [KubeNodePressure](#kubenodepressure) | `info` | `10m` | kubernetes-system-kubelet |
| [KubeQuotaAlmostFull](#kubequotaalmostfull) | `info` | `15m` | kubernetes-resources |
| [KubeQuotaFullyUsed](#kubequotafullyused) | `info` | `15m` | kubernetes-resources |
| [KubeletTooManyPods](#kubelettoomanypods) | `info` | `15m` | kubernetes-system-kubelet |
| [NodeCPUHighUsage](#nodecpuhighusage) | `info` | `15m` | node-exporter |
| [InfoInhibitor](#infoinhibitor) | `none` | `-` | general.rules |
| [Watchdog](#watchdog) | `none` | `-` | general.rules |

### Detalle

#### alertmanager.rules

<sub>PrometheusRule: `kube-prometheus-stack-kps-alertmanager.rules` (generado por el chart)</sub>

##### AlertmanagerClusterCrashlooping

`critical` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagerclustercrashlooping)

Half or more of the Alertmanager instances within the same cluster are crashlooping.

```promql
( count by (namespace,service,cluster) ( changes(process_start_time_seconds{job="kps-kube-prometheus-stack-alertmanager",container="alertmanager",namespace="observability"}[10m]) > 4 ) / count by (namespace,service,cluster) ( up{job="kps-kube-prometheus-stack-alertmanager",container="alertmanager",namespace="observability"} ) ) >= 0.5
```

##### AlertmanagerClusterDown

`critical` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagerclusterdown)

Half or more of the Alertmanager instances within the same cluster are down.

```promql
( count by (namespace,service,cluster) ( avg_over_time(up{job="kps-kube-prometheus-stack-alertmanager",container="alertmanager",namespace="observability"}[5m]) < 0.5 ) / count by (namespace,service,cluster) ( up{job="kps-kube-prometheus-stack-alertmanager",container="alertmanager",namespace="observability"} ) ) >= 0.5
```

##### AlertmanagerClusterFailedToSendAlerts

`critical` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagerclusterfailedtosendalerts)

All Alertmanager instances in a cluster failed to send notifications to a critical integration.

```promql
min by (namespace,service, integration) ( rate(alertmanager_notifications_failed_total{job="kps-kube-prometheus-stack-alertmanager",container="alertmanager",namespace="observability", integration=~`.*`}[15m]) / ignoring (reason) group_left rate(alertmanager_notifications_total{job="kps-kube-prometheus-stack-alertmanager",container="alertmanager",namespace="observability", integration=~`.*`}[15m]) > 0 ) > 0.01
```

##### AlertmanagerConfigInconsistent

`critical` · `for: 20m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagerconfiginconsistent)

Alertmanager instances within the same cluster have different configurations.

```promql
count by (namespace,service,cluster) ( count_values by (namespace,service,cluster) ("config_hash", alertmanager_config_hash{job="kps-kube-prometheus-stack-alertmanager",container="alertmanager",namespace="observability"}) ) != 1
```

##### AlertmanagerFailedReload

`critical` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagerfailedreload)

Reloading an Alertmanager configuration has failed.

```promql
# Without max_over_time, failed scrapes could create false negatives, see # https://www.robustperception.io/alerting-on-gauges-in-prometheus-2-0 for details. max_over_time(alertmanager_config_last_reload_successful{job="kps-kube-prometheus-stack-alertmanager",container="alertmanager",namespace="observability"}[5m]) == 0
```

##### AlertmanagerMembersInconsistent

`critical` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagermembersinconsistent)

A member of an Alertmanager cluster has not found all other cluster members.

```promql
# Without max_over_time, failed scrapes could create false negatives, see # https://www.robustperception.io/alerting-on-gauges-in-prometheus-2-0 for details. max_over_time(alertmanager_cluster_members{job="kps-kube-prometheus-stack-alertmanager",container="alertmanager",namespace="observability"}[5m]) < on (namespace,service,cluster) group_left count by (namespace,service,cluster) (max_over_time(alertmanager_cluster_members{job="kps-kube-prometheus-stack-alertmanager",container="alertmanager",namespace="observability"}[5m]))
```

##### AlertmanagerClusterFailedPeers

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagerclusterfailedpeers)

An Alertmanager instance has failed peers in the cluster.

```promql
# Without max_over_time, failed scrapes could create false negatives, see # https://www.robustperception.io/alerting-on-gauges-in-prometheus-2-0 for details. max_over_time(alertmanager_cluster_failed_peers{job="kps-kube-prometheus-stack-alertmanager",container="alertmanager",namespace="observability"}[5m]) > 0
```

##### AlertmanagerClusterFailedToSendAlerts

`warning` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagerclusterfailedtosendalerts)

All Alertmanager instances in a cluster failed to send notifications to a non-critical integration.

```promql
min by (namespace,service, integration) ( rate(alertmanager_notifications_failed_total{job="kps-kube-prometheus-stack-alertmanager",container="alertmanager",namespace="observability", integration!~`.*`}[15m]) / ignoring (reason) group_left rate(alertmanager_notifications_total{job="kps-kube-prometheus-stack-alertmanager",container="alertmanager",namespace="observability", integration!~`.*`}[15m]) > 0 ) > 0.01
```

##### AlertmanagerFailedToSendAlerts

`warning` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/alertmanager/alertmanagerfailedtosendalerts)

An Alertmanager instance failed to send notifications.

```promql
( rate(alertmanager_notifications_failed_total{job="kps-kube-prometheus-stack-alertmanager",container="alertmanager",namespace="observability"}[15m]) / ignoring (reason) group_left rate(alertmanager_notifications_total{job="kps-kube-prometheus-stack-alertmanager",container="alertmanager",namespace="observability"}[15m]) ) > 0.01
```

#### config-reloaders

<sub>PrometheusRule: `kube-prometheus-stack-kps-config-reloaders` (generado por el chart)</sub>

##### ConfigReloaderSidecarErrors

`warning` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus-operator/configreloadersidecarerrors)

config-reloader sidecar has not had a successful reload for 10m

```promql
max_over_time(reloader_last_reload_successful{namespace=~".+"}[5m]) == 0
```

#### general.rules

<sub>PrometheusRule: `kube-prometheus-stack-kps-general.rules` (generado por el chart)</sub>

##### TargetDown

`warning` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/general/targetdown)

One or more targets are unreachable.

```promql
100 * (count(up == 0) BY (cluster, job, namespace, service) / count(up) BY (cluster, job, namespace, service)) > 10
```

##### InfoInhibitor

`none` · `for: -` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/general/infoinhibitor)

Info-level alert inhibition.

```promql
group by (namespace) (ALERTS{severity = "info"} == 1) unless on (namespace) group by (namespace) (ALERTS{alertname != "InfoInhibitor", alertstate = "firing", severity =~ "warning|critical"} == 1)
```

##### Watchdog

`none` · `for: -` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/general/watchdog)

An alert that should always be firing to certify that Alertmanager is working properly.

```promql
vector(1)
```

#### kube-apiserver-slos

<sub>PrometheusRule: `kube-prometheus-stack-kps-kube-apiserver-slos` (generado por el chart)</sub>

##### KubeAPIErrorBudgetBurn

`critical` · `for: 2m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeapierrorbudgetburn)

The Kube API server is burning too much error budget.

```promql
sum by (cluster) (apiserver_request:burnrate1h) > (14.40 * 0.01000) and on (cluster) sum by (cluster) (apiserver_request:burnrate5m) > (14.40 * 0.01000)
```

##### KubeAPIErrorBudgetBurn

`critical` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeapierrorbudgetburn)

The Kube API server is burning too much error budget.

```promql
sum by (cluster) (apiserver_request:burnrate6h) > (6.00 * 0.01000) and on (cluster) sum by (cluster) (apiserver_request:burnrate30m) > (6.00 * 0.01000)
```

##### KubeAPIErrorBudgetBurn

`warning` · `for: 1h` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeapierrorbudgetburn)

The Kube API server is burning too much error budget.

```promql
sum by (cluster) (apiserver_request:burnrate1d) > (3.00 * 0.01000) and on (cluster) sum by (cluster) (apiserver_request:burnrate2h) > (3.00 * 0.01000)
```

##### KubeAPIErrorBudgetBurn

`warning` · `for: 3h` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeapierrorbudgetburn)

The Kube API server is burning too much error budget.

```promql
sum by (cluster) (apiserver_request:burnrate3d) > (1.00 * 0.01000) and on (cluster) sum by (cluster) (apiserver_request:burnrate6h) > (1.00 * 0.01000)
```

#### kube-state-metrics

<sub>PrometheusRule: `kube-prometheus-stack-kps-kube-state-metrics` (generado por el chart)</sub>

##### KubeStateMetricsListErrors

`critical` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kube-state-metrics/kubestatemetricslisterrors)

kube-state-metrics is experiencing errors in list operations.

```promql
(sum(rate(kube_state_metrics_list_total{job="kube-state-metrics",result="error"}[5m])) by (cluster) / sum(rate(kube_state_metrics_list_total{job="kube-state-metrics"}[5m])) by (cluster)) > 0.01
```

##### KubeStateMetricsShardingMismatch

`critical` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kube-state-metrics/kubestatemetricsshardingmismatch)

kube-state-metrics sharding is misconfigured.

```promql
stdvar (kube_state_metrics_total_shards{job="kube-state-metrics"}) by (cluster) != 0
```

##### KubeStateMetricsShardsMissing

`critical` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kube-state-metrics/kubestatemetricsshardsmissing)

kube-state-metrics shards are missing.

```promql
2^max(kube_state_metrics_total_shards{job="kube-state-metrics"}) by (cluster) - 1 - sum( 2 ^ max by (cluster, shard_ordinal) (kube_state_metrics_shard_ordinal{job="kube-state-metrics"}) ) by (cluster) != 0
```

##### KubeStateMetricsWatchErrors

`critical` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kube-state-metrics/kubestatemetricswatcherrors)

kube-state-metrics is experiencing errors in watch operations.

```promql
(sum(rate(kube_state_metrics_watch_total{job="kube-state-metrics",result="error"}[5m])) by (cluster) / sum(rate(kube_state_metrics_watch_total{job="kube-state-metrics"}[5m])) by (cluster)) > 0.01
```

#### kubernetes-apps

<sub>PrometheusRule: `kube-prometheus-stack-kps-kubernetes-apps` (generado por el chart)</sub>

##### KubeContainerWaiting

`warning` · `for: 1h` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubecontainerwaiting)

Pod container waiting longer than 1 hour

```promql
kube_pod_container_status_waiting_reason{reason!="CrashLoopBackOff", job="kube-state-metrics", namespace=~".*"} > 0
```

##### KubeDaemonSetMisScheduled

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubedaemonsetmisscheduled)

DaemonSet pods are misscheduled.

```promql
kube_daemonset_status_number_misscheduled{job="kube-state-metrics", namespace=~".*"} > 0
```

##### KubeDaemonSetNotScheduled

`warning` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubedaemonsetnotscheduled)

DaemonSet pods are not scheduled.

```promql
kube_daemonset_status_desired_number_scheduled{job="kube-state-metrics", namespace=~".*"} - kube_daemonset_status_current_number_scheduled{job="kube-state-metrics", namespace=~".*"} > 0
```

##### KubeDaemonSetRolloutStuck

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubedaemonsetrolloutstuck)

DaemonSet rollout is stuck.

```promql
( ( kube_daemonset_status_current_number_scheduled{job="kube-state-metrics", namespace=~".*"} != kube_daemonset_status_desired_number_scheduled{job="kube-state-metrics", namespace=~".*"} ) or ( kube_daemonset_status_number_misscheduled{job="kube-state-metrics", namespace=~".*"} != 0 ) or ( kube_daemonset_status_updated_number_scheduled{job="kube-state-metrics", namespace=~".*"} != kube_daemonset_status_desired_number_scheduled{job="kube-state-metrics", namespace=~".*"} ) or ( kube_daemonset_status_number_available{job="kube-state-metrics", namespace=~".*"} != kube_daemonset_status_desired_number_scheduled{job="kube-state-metrics", namespace=~".*"} ) ) and ( changes(kube_daemonset_status_updated_number_scheduled{job="kube-state-metrics", namespace=~".*"}[5m]) == 0 )
```

##### KubeDeploymentGenerationMismatch

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubedeploymentgenerationmismatch)

Deployment generation mismatch due to possible roll-back

```promql
kube_deployment_status_observed_generation{job="kube-state-metrics", namespace=~".*"} != kube_deployment_metadata_generation{job="kube-state-metrics", namespace=~".*"}
```

##### KubeDeploymentReplicasMismatch

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubedeploymentreplicasmismatch)

Deployment has not matched the expected number of replicas.

```promql
( kube_deployment_spec_replicas{job="kube-state-metrics", namespace=~".*"} > kube_deployment_status_replicas_available{job="kube-state-metrics", namespace=~".*"} ) and ( changes(kube_deployment_status_replicas_updated{job="kube-state-metrics", namespace=~".*"}[10m]) == 0 )
```

##### KubeDeploymentRolloutStuck

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubedeploymentrolloutstuck)

Deployment rollout is not progressing.

```promql
kube_deployment_status_condition{condition="Progressing", status="false",job="kube-state-metrics", namespace=~".*"} != 0
```

##### KubeHpaMaxedOut

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubehpamaxedout)

HPA is running at max replicas

```promql
( kube_horizontalpodautoscaler_status_current_replicas{job="kube-state-metrics", namespace=~".*"} == kube_horizontalpodautoscaler_spec_max_replicas{job="kube-state-metrics", namespace=~".*"} ) and on (namespace, horizontalpodautoscaler, cluster) ( kube_horizontalpodautoscaler_spec_max_replicas{job="kube-state-metrics", namespace=~".*"} != kube_horizontalpodautoscaler_spec_min_replicas{job="kube-state-metrics", namespace=~".*"} )
```

##### KubeHpaReplicasMismatch

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubehpareplicasmismatch)

HPA has not matched desired number of replicas.

```promql
(kube_horizontalpodautoscaler_status_desired_replicas{job="kube-state-metrics", namespace=~".*"} != kube_horizontalpodautoscaler_status_current_replicas{job="kube-state-metrics", namespace=~".*"}) and (kube_horizontalpodautoscaler_status_current_replicas{job="kube-state-metrics", namespace=~".*"} > kube_horizontalpodautoscaler_spec_min_replicas{job="kube-state-metrics", namespace=~".*"}) and (kube_horizontalpodautoscaler_status_current_replicas{job="kube-state-metrics", namespace=~".*"} < kube_horizontalpodautoscaler_spec_max_replicas{job="kube-state-metrics", namespace=~".*"}) and changes(kube_horizontalpodautoscaler_status_current_replicas{job="kube-state-metrics", namespace=~".*"}[15m]) == 0
```

##### KubeJobFailed

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubejobfailed)

Job failed to complete.

```promql
kube_job_failed{job="kube-state-metrics", namespace=~".*"} > 0
```

##### KubeJobNotCompleted

`warning` · `for: -` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubejobnotcompleted)

Job did not complete in time

```promql
time() - max by (namespace, job_name, cluster) (kube_job_status_start_time{job="kube-state-metrics", namespace=~".*"} and kube_job_status_active{job="kube-state-metrics", namespace=~".*"} > 0) > 43200
```

##### KubePdbNotEnoughHealthyPods

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubepdbnotenoughhealthypods)

PDB does not have enough healthy pods.

```promql
( kube_poddisruptionbudget_status_desired_healthy{job="kube-state-metrics", namespace=~".*"} - kube_poddisruptionbudget_status_current_healthy{job="kube-state-metrics", namespace=~".*"} ) > 0
```

##### KubePodCrashLooping

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubepodcrashlooping)

Pod is crash looping.

```promql
max_over_time(kube_pod_container_status_waiting_reason{reason="CrashLoopBackOff", job="kube-state-metrics", namespace=~".*"}[5m]) >= 1
```

##### KubePodNotReady

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubepodnotready)

Pod has been in a non-ready state for more than 15 minutes.

```promql
sum by (namespace, pod, job, cluster) ( max by (namespace, pod, job, cluster) ( kube_pod_status_phase{job="kube-state-metrics", namespace=~".*", phase=~"Pending|Unknown"} or ( kube_pod_status_phase{job="kube-state-metrics", namespace=~".*", phase="Running"} == 1 and on (namespace, pod, cluster) kube_pod_status_ready{job="kube-state-metrics", namespace=~".*", condition="true"} == 0 ) ) * on (namespace, pod, cluster) group_left() topk by (namespace, pod, cluster) ( 1, max by (namespace, pod, owner_kind, cluster) (kube_pod_owner{owner_kind!="Job"}) ) ) > 0 unless on (namespace, pod, cluster) kube_pod_status_reason{job="kube-state-metrics", namespace=~".*", reason="SchedulingGated"} == 1
```

##### KubeStatefulSetGenerationMismatch

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubestatefulsetgenerationmismatch)

StatefulSet generation mismatch due to possible roll-back

```promql
kube_statefulset_status_observed_generation{job="kube-state-metrics", namespace=~".*"} != kube_statefulset_metadata_generation{job="kube-state-metrics", namespace=~".*"}
```

##### KubeStatefulSetReplicasMismatch

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubestatefulsetreplicasmismatch)

StatefulSet has not matched the expected number of replicas.

```promql
( kube_statefulset_status_replicas_ready{job="kube-state-metrics", namespace=~".*"} != kube_statefulset_replicas{job="kube-state-metrics", namespace=~".*"} ) and ( changes(kube_statefulset_status_replicas_updated{job="kube-state-metrics", namespace=~".*"}[10m]) == 0 )
```

##### KubeStatefulSetUpdateNotRolledOut

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubestatefulsetupdatenotrolledout)

StatefulSet update has not been rolled out.

```promql
( max by (namespace, statefulset, job, cluster) ( kube_statefulset_status_current_revision{job="kube-state-metrics", namespace=~".*"} unless kube_statefulset_status_update_revision{job="kube-state-metrics", namespace=~".*"} ) * on (namespace, statefulset, job, cluster) ( kube_statefulset_replicas{job="kube-state-metrics", namespace=~".*"} != kube_statefulset_status_replicas_updated{job="kube-state-metrics", namespace=~".*"} ) ) and on (namespace, statefulset, job, cluster) ( changes(kube_statefulset_status_replicas_updated{job="kube-state-metrics", namespace=~".*"}[5m]) == 0 )
```

#### kubernetes-resources

<sub>PrometheusRule: `kube-prometheus-stack-kps-kubernetes-resources` (generado por el chart)</sub>

##### KubeCPUOvercommit

`warning` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubecpuovercommit)

Cluster has overcommitted CPU resource requests.

```promql
# Non-HA clusters. ( ( sum by (cluster) (namespace_cpu:kube_pod_container_resource_requests:sum{}) - sum by (cluster) (kube_node_status_allocatable{job="kube-state-metrics",resource="cpu"}) > 0 ) and count by (cluster) (max by (cluster, node) (kube_node_role{job="kube-state-metrics", role="control-plane"})) < 3 ) or # HA clusters. ( sum by (cluster) (namespace_cpu:kube_pod_container_resource_requests:sum{}) - ( # Skip clusters with only one allocatable node. ( sum by (cluster) (kube_node_status_allocatable{job="kube-state-metrics",resource="cpu"}) - max by (cluster) (kube_node_status_allocatable{job="kube-state-metrics",resource="cpu"}) ) > 0 ) > 0 )
```

##### KubeCPUQuotaOvercommit

`warning` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubecpuquotaovercommit)

Cluster has overcommitted CPU resource requests.

```promql
sum by (cluster) ( min without(resource) (kube_resourcequota{job="kube-state-metrics", type="hard", resource=~"(cpu|requests.cpu)"}) ) / sum by (cluster) ( kube_node_status_allocatable{resource="cpu", job="kube-state-metrics"} ) > 1.5
```

##### KubeMemoryOvercommit

`warning` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubememoryovercommit)

Cluster has overcommitted memory resource requests.

```promql
# Non-HA clusters. ( ( sum by (cluster) (namespace_memory:kube_pod_container_resource_requests:sum{}) - sum by (cluster) (kube_node_status_allocatable{job="kube-state-metrics",resource="memory"}) > 0 ) and count by (cluster) (max by (cluster, node) (kube_node_role{job="kube-state-metrics", role="control-plane"})) < 3 ) or # HA clusters. ( sum by (cluster) (namespace_memory:kube_pod_container_resource_requests:sum{}) - ( # Skip clusters with only one allocatable node. ( sum by (cluster) (kube_node_status_allocatable{job="kube-state-metrics",resource="memory"}) - max by (cluster) (kube_node_status_allocatable{job="kube-state-metrics",resource="memory"}) ) > 0 ) > 0 )
```

##### KubeMemoryQuotaOvercommit

`warning` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubememoryquotaovercommit)

Cluster has overcommitted memory resource requests.

```promql
sum by (cluster) ( min without(resource) (kube_resourcequota{job="kube-state-metrics", type="hard", resource=~"(memory|requests.memory)"}) ) / sum by (cluster) ( kube_node_status_allocatable{resource="memory", job="kube-state-metrics"} ) > 1.5
```

##### KubeQuotaExceeded

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubequotaexceeded)

Namespace quota has exceeded the limits.

```promql
topk by (cluster, namespace, resource, resourcequota) (1, max without (instance, job, type) ( kube_resourcequota{job="kube-state-metrics", type="used"} ) ) / on (cluster, namespace, resource, resourcequota) group_left() topk by (cluster, namespace, resource, resourcequota) (1, max without (instance, job, type) ( kube_resourcequota{job="kube-state-metrics", type="hard"} ) > 0 ) > 1
```

##### CPUThrottlingHigh

`info` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/cputhrottlinghigh)

Processes experience elevated CPU throttling.

```promql
sum without (id, metrics_path, name, image, endpoint, job, node) ( topk by (cluster, namespace, pod, container, instance) (1, increase( container_cpu_cfs_throttled_periods_total{container!="", job="kubelet", metrics_path="/metrics/cadvisor", } [5m]) ) ) / on (cluster, namespace, pod, container, instance) group_left sum without (id, metrics_path, name, image, endpoint, job, node) ( topk by (cluster, namespace, pod, container, instance) (1, increase( container_cpu_cfs_periods_total{job="kubelet", metrics_path="/metrics/cadvisor", } [5m]) ) ) > ( 25 / 100 )
```

##### KubeQuotaAlmostFull

`info` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubequotaalmostfull)

Namespace quota is going to be full.

```promql
topk by (cluster, namespace, resource, resourcequota) (1, max without (instance, job, type) ( kube_resourcequota{job="kube-state-metrics", type="used"} ) ) / on (cluster, namespace, resource, resourcequota) group_left() topk by (cluster, namespace, resource, resourcequota) (1, max without (instance, job, type) ( kube_resourcequota{job="kube-state-metrics", type="hard"} ) > 0 ) > 0.9 < 1
```

##### KubeQuotaFullyUsed

`info` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubequotafullyused)

Namespace quota is fully used.

```promql
topk by (cluster, namespace, resource, resourcequota) (1, max without (instance, job, type) ( kube_resourcequota{job="kube-state-metrics", type="used"} ) ) / on (cluster, namespace, resource, resourcequota) group_left() topk by (cluster, namespace, resource, resourcequota) (1, max without (instance, job, type) ( kube_resourcequota{job="kube-state-metrics", type="hard"} ) > 0 ) == 1
```

#### kubernetes-storage

<sub>PrometheusRule: `kube-prometheus-stack-kps-kubernetes-storage` (generado por el chart)</sub>

##### KubePersistentVolumeErrors

`critical` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubepersistentvolumeerrors)

PersistentVolume is having issues with provisioning.

```promql
kube_persistentvolume_status_phase{phase=~"Failed|Pending",job="kube-state-metrics"} > 0
```

##### KubePersistentVolumeFillingUp

`critical` · `for: 1m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubepersistentvolumefillingup)

PersistentVolume is filling up.

```promql
( kubelet_volume_stats_available_bytes{job="kubelet", namespace=~".*", metrics_path="/metrics"} / kubelet_volume_stats_capacity_bytes{job="kubelet", namespace=~".*", metrics_path="/metrics"} ) < 0.03 and kubelet_volume_stats_used_bytes{job="kubelet", namespace=~".*", metrics_path="/metrics"} > 0 unless on (cluster, namespace, persistentvolumeclaim) kube_persistentvolumeclaim_access_mode{ access_mode="ReadOnlyMany"} == 1 unless on (cluster, namespace, persistentvolumeclaim) kube_persistentvolumeclaim_labels{label_excluded_from_alerts="true"} == 1
```

##### KubePersistentVolumeInodesFillingUp

`critical` · `for: 1m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubepersistentvolumeinodesfillingup)

PersistentVolumeInodes are filling up.

```promql
( kubelet_volume_stats_inodes_free{job="kubelet", namespace=~".*", metrics_path="/metrics"} / kubelet_volume_stats_inodes{job="kubelet", namespace=~".*", metrics_path="/metrics"} ) < 0.03 and kubelet_volume_stats_inodes_used{job="kubelet", namespace=~".*", metrics_path="/metrics"} > 0 unless on (cluster, namespace, persistentvolumeclaim) kube_persistentvolumeclaim_access_mode{ access_mode="ReadOnlyMany"} == 1 unless on (cluster, namespace, persistentvolumeclaim) kube_persistentvolumeclaim_labels{label_excluded_from_alerts="true"} == 1
```

##### KubePersistentVolumeFillingUp

`warning` · `for: 1h` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubepersistentvolumefillingup)

PersistentVolume is filling up.

```promql
( kubelet_volume_stats_available_bytes{job="kubelet", namespace=~".*", metrics_path="/metrics"} / kubelet_volume_stats_capacity_bytes{job="kubelet", namespace=~".*", metrics_path="/metrics"} ) < 0.15 and kubelet_volume_stats_used_bytes{job="kubelet", namespace=~".*", metrics_path="/metrics"} > 0 and predict_linear(kubelet_volume_stats_available_bytes{job="kubelet", namespace=~".*", metrics_path="/metrics"}[6h], 4 * 24 * 3600) < 0 unless on (cluster, namespace, persistentvolumeclaim) kube_persistentvolumeclaim_access_mode{ access_mode="ReadOnlyMany"} == 1 unless on (cluster, namespace, persistentvolumeclaim) kube_persistentvolumeclaim_labels{label_excluded_from_alerts="true"} == 1
```

##### KubePersistentVolumeInodesFillingUp

`warning` · `for: 1h` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubepersistentvolumeinodesfillingup)

PersistentVolumeInodes are filling up.

```promql
( kubelet_volume_stats_inodes_free{job="kubelet", namespace=~".*", metrics_path="/metrics"} / kubelet_volume_stats_inodes{job="kubelet", namespace=~".*", metrics_path="/metrics"} ) < 0.15 and kubelet_volume_stats_inodes_used{job="kubelet", namespace=~".*", metrics_path="/metrics"} > 0 and predict_linear(kubelet_volume_stats_inodes_free{job="kubelet", namespace=~".*", metrics_path="/metrics"}[6h], 4 * 24 * 3600) < 0 unless on (cluster, namespace, persistentvolumeclaim) kube_persistentvolumeclaim_access_mode{ access_mode="ReadOnlyMany"} == 1 unless on (cluster, namespace, persistentvolumeclaim) kube_persistentvolumeclaim_labels{label_excluded_from_alerts="true"} == 1
```

#### kubernetes-system

<sub>PrometheusRule: `kube-prometheus-stack-kps-kubernetes-system` (generado por el chart)</sub>

##### KubeClientErrors

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeclienterrors)

Kubernetes API server client is experiencing errors.

```promql
(sum(rate(rest_client_requests_total{job="apiserver",code=~"5.."}[5m])) by (cluster, instance, job, namespace) / sum(rate(rest_client_requests_total{job="apiserver"}[5m])) by (cluster, instance, job, namespace)) > 0.01
```

##### KubeVersionMismatch

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeversionmismatch)

Different semantic versions of Kubernetes components running.

```promql
count by (cluster) (count by (git_version, cluster) (label_replace(kubernetes_build_info{job!~"kube-dns|coredns"},"git_version","$1","git_version","(v[0-9]*.[0-9]*).*"))) > 1
```

#### kubernetes-system-apiserver

<sub>PrometheusRule: `kube-prometheus-stack-kps-kubernetes-system-apiserver` (generado por el chart)</sub>

##### KubeAPIDown

`critical` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeapidown)

Target disappeared from Prometheus target discovery.

```promql
absent(up{job="apiserver"})
```

##### KubeClientCertificateExpiration

`critical` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeclientcertificateexpiration)

Client certificate is about to expire.

```promql
histogram_quantile(0.01, sum without (namespace, service, endpoint) (rate(apiserver_client_certificate_expiration_seconds_bucket{job="apiserver"}[5m]))) < 86400 and on (job, cluster, instance) apiserver_client_certificate_expiration_seconds_count{job="apiserver"} > 0
```

##### KubeAPIInstanceUnreachable

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeapiinstanceunreachable)

KubeAPI instance is unreachable.

```promql
up{job="apiserver"} == 0
```

##### KubeAPITerminatedRequests

`warning` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeapiterminatedrequests)

The kubernetes apiserver has terminated {{ $value | humanizePercentage }} of its incoming requests.

```promql
sum by (cluster) (rate(apiserver_request_terminations_total{job="apiserver"}[10m])) / ( sum by (cluster) (rate(apiserver_request_total{job="apiserver"}[10m])) + sum by (cluster) (rate(apiserver_request_terminations_total{job="apiserver"}[10m])) ) > 0.20
```

##### KubeAggregatedAPIDown

`warning` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeaggregatedapidown)

Kubernetes aggregated API is down.

```promql
(1 - max by (name, namespace, cluster)(avg_over_time(aggregator_unavailable_apiservice{job="apiserver"}[10m]))) * 100 < 85
```

##### KubeAggregatedAPIErrors

`warning` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeaggregatedapierrors)

Kubernetes aggregated API has reported errors.

```promql
sum by (cluster, instance, name, reason)(increase(aggregator_unavailable_apiservice_total{job="apiserver"}[1m])) > 0
```

##### KubeClientCertificateExpiration

`warning` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeclientcertificateexpiration)

Client certificate is about to expire.

```promql
histogram_quantile(0.01, sum without (namespace, service, endpoint) (rate(apiserver_client_certificate_expiration_seconds_bucket{job="apiserver"}[5m]))) < 604800 and on (job, cluster, instance) apiserver_client_certificate_expiration_seconds_count{job="apiserver"} > 0
```

#### kubernetes-system-kubelet

<sub>PrometheusRule: `kube-prometheus-stack-kps-kubernetes-system-kubelet` (generado por el chart)</sub>

##### KubeletClientCertificateExpiration

`critical` · `for: -` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeletclientcertificateexpiration)

Kubelet client certificate is about to expire.

```promql
kubelet_certificate_manager_client_ttl_seconds < 86400
```

##### KubeletDown

`critical` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeletdown)

Target disappeared from Prometheus target discovery.

```promql
count by (cluster) (kube_node_info{job="kube-state-metrics"}) unless on (cluster) count by (cluster) (up{job="kubelet", metrics_path="/metrics"} == 1)
```

##### KubeletServerCertificateExpiration

`critical` · `for: -` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeletservercertificateexpiration)

Kubelet server certificate is about to expire.

```promql
kubelet_certificate_manager_server_ttl_seconds < 86400
```

##### KubeNodeNotReady

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubenodenotready)

Node is not ready.

```promql
kube_node_status_condition{job="kube-state-metrics",condition="Ready",status="true"} == 0 and on (cluster, node) kube_node_spec_unschedulable{job="kube-state-metrics"} == 0
```

##### KubeNodeReadinessFlapping

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubenodereadinessflapping)

Node readiness status is flapping.

```promql
sum(changes(kube_node_status_condition{job="kube-state-metrics",status="true",condition="Ready"}[15m])) by (cluster, node) > 2 and on (cluster, node) kube_node_spec_unschedulable{job="kube-state-metrics"} == 0
```

##### KubeNodeUnreachable

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubenodeunreachable)

Node is unreachable.

```promql
(kube_node_spec_taint{job="kube-state-metrics",key="node.kubernetes.io/unreachable",effect="NoSchedule"} unless ignoring(key,value) kube_node_spec_taint{job="kube-state-metrics",key=~"ToBeDeletedByClusterAutoscaler|cloud.google.com/impending-node-termination|aws-node-termination-handler/spot-itn"}) == 1
```

##### KubeletClientCertificateExpiration

`warning` · `for: -` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeletclientcertificateexpiration)

Kubelet client certificate is about to expire.

```promql
kubelet_certificate_manager_client_ttl_seconds < 604800
```

##### KubeletClientCertificateRenewalErrors

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeletclientcertificaterenewalerrors)

Kubelet has failed to renew its client certificate.

```promql
increase(kubelet_certificate_manager_client_expiration_renew_errors[5m]) > 0
```

##### KubeletInstanceUnreachable

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeletinstanceunreachable)

Kubelet instance is unreachable.

```promql
up{job="kubelet", metrics_path="/metrics"} == 0
```

##### KubeletPlegDurationHigh

`warning` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeletplegdurationhigh)

Kubelet Pod Lifecycle Event Generator is taking too long to relist.

```promql
node_quantile:kubelet_pleg_relist_duration_seconds:histogram_quantile{quantile="0.99"} >= 10
```

##### KubeletPodStartUpLatencyHigh

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeletpodstartuplatencyhigh)

Kubelet Pod startup latency is too high.

```promql
histogram_quantile(0.99, sum by (cluster, instance, le) ( topk by (cluster, instance, le, operation_type) (1, rate(kubelet_pod_worker_duration_seconds_bucket{job="kubelet", metrics_path="/metrics"}[5m]) ) ) ) * on (cluster, instance) group_left(node) topk by (cluster, instance, node) (1, kubelet_node_name{job="kubelet", metrics_path="/metrics"} ) > 60
```

##### KubeletServerCertificateExpiration

`warning` · `for: -` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeletservercertificateexpiration)

Kubelet server certificate is about to expire.

```promql
kubelet_certificate_manager_server_ttl_seconds < 604800
```

##### KubeletServerCertificateRenewalErrors

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubeletservercertificaterenewalerrors)

Kubelet has failed to renew its server certificate.

```promql
increase(kubelet_server_expiration_renew_errors[5m]) > 0
```

##### KubeNodeEviction

`info` · `for: 0s` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubenodeeviction)

Node is evicting pods.

```promql
sum(rate(kubelet_evictions{job="kubelet", metrics_path="/metrics"}[15m])) by (cluster, eviction_signal, instance) * on (cluster, instance) group_left(node) max by (cluster, instance, node) ( kubelet_node_name{job="kubelet", metrics_path="/metrics"} ) > 0
```

##### KubeNodePressure

`info` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubenodepressure)

Node has as active Condition.

```promql
kube_node_status_condition{job="kube-state-metrics",condition=~"(MemoryPressure|DiskPressure|PIDPressure)",status="true"} == 1 and on (cluster, node) kube_node_spec_unschedulable{job="kube-state-metrics"} == 0
```

##### KubeletTooManyPods

`info` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/kubernetes/kubelettoomanypods)

Kubelet is running at capacity.

```promql
( max by (cluster, instance) ( kubelet_running_pods{job="kubelet", metrics_path="/metrics"} > 1 ) * on (cluster, instance) group_left(node) max by (cluster, instance, node) ( kubelet_node_name{job="kubelet", metrics_path="/metrics"} ) ) / on (cluster, node) group_left() max by (cluster, node) ( kube_node_status_capacity{job="kube-state-metrics", resource="pods"} != 1 ) > 0.95
```

#### longhorn

<sub>PrometheusRule: `workloads/observability/longhorn.prometheusrule.yaml` (propio del repo)</sub>

##### LonghornBackupFailed

`critical` · `for: 5m`

Longhorn backup failed for volume {{ $labels.volume }}

```promql
longhorn_backup_state == 4
```

##### LonghornVolumeStatusCritical

`critical` · `for: 5m`

Longhorn volume {{ $labels.pvc_namespace }}/{{ $labels.pvc }} is Faulted

```promql
longhorn_volume_robustness{state="faulted"} == 1
```

##### LonghornBackupStale

`warning` · `for: 30m`

No backup of {{ $labels.pvc_namespace }}/{{ $labels.pvc }} in over 26h

```promql
(time() - longhorn_volume_last_backup_at) > 26 * 3600 and longhorn_volume_last_backup_at > 0
```

##### LonghornDiskNotSchedulable

`warning` · `for: 15m`

Longhorn disk {{ $labels.disk }} on {{ $labels.node }} is not schedulable

```promql
longhorn_disk_status{condition="schedulable"} == 0
```

##### LonghornVolumeStatusWarning

`warning` · `for: 5m`

Longhorn volume {{ $labels.pvc_namespace }}/{{ $labels.pvc }} is Degraded

```promql
longhorn_volume_robustness{state="degraded"} == 1
```

#### node-exporter

<sub>PrometheusRule: `kube-prometheus-stack-kps-node-exporter` (generado por el chart)</sub>

##### NodeFileDescriptorLimit

`critical` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodefiledescriptorlimit)

Kernel is predicted to exhaust file descriptors limit soon.

```promql
( node_filefd_allocated{job="node-exporter"} * 100 / node_filefd_maximum{job="node-exporter"} > 90 )
```

##### NodeFilesystemAlmostOutOfFiles

`critical` · `for: 1h` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodefilesystemalmostoutoffiles)

Filesystem has less than 3% inodes left.

```promql
( node_filesystem_files_free{job="node-exporter",fstype!="",mountpoint!=""} / node_filesystem_files{job="node-exporter",fstype!="",mountpoint!=""} * 100 < 3 and node_filesystem_readonly{job="node-exporter",fstype!="",mountpoint!=""} == 0 )
```

##### NodeFilesystemAlmostOutOfSpace

`critical` · `for: 30m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodefilesystemalmostoutofspace)

Filesystem has less than 3% space left.

```promql
( node_filesystem_avail_bytes{job="node-exporter",fstype!="",mountpoint!=""} / node_filesystem_size_bytes{job="node-exporter",fstype!="",mountpoint!=""} * 100 < 3 and node_filesystem_readonly{job="node-exporter",fstype!="",mountpoint!=""} == 0 )
```

##### NodeFilesystemFilesFillingUp

`critical` · `for: 1h` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodefilesystemfilesfillingup)

Filesystem is predicted to run out of inodes within the next 4 hours.

```promql
( node_filesystem_files_free{job="node-exporter",fstype!="",mountpoint!=""} / node_filesystem_files{job="node-exporter",fstype!="",mountpoint!=""} * 100 < 20 and predict_linear(node_filesystem_files_free{job="node-exporter",fstype!="",mountpoint!=""}[6h], 4*60*60) < 0 and node_filesystem_readonly{job="node-exporter",fstype!="",mountpoint!=""} == 0 )
```

##### NodeFilesystemSpaceFillingUp

`critical` · `for: 1h` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodefilesystemspacefillingup)

Filesystem is predicted to run out of space within the next 4 hours.

```promql
( node_filesystem_avail_bytes{job="node-exporter",fstype!="",mountpoint!=""} / node_filesystem_size_bytes{job="node-exporter",fstype!="",mountpoint!=""} * 100 < 10 and predict_linear(node_filesystem_avail_bytes{job="node-exporter",fstype!="",mountpoint!=""}[6h], 4*60*60) < 0 and node_filesystem_readonly{job="node-exporter",fstype!="",mountpoint!=""} == 0 )
```

##### NodeRAIDDegraded

`critical` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/noderaiddegraded)

RAID Array is degraded.

```promql
node_md_disks_required{job="node-exporter",device=~"(/dev/)?(mmcblk.p.+|nvme.+|rbd.+|sd.+|vd.+|xvd.+|dm-.+|md.+|dasd.+)"} - ignoring (state) (node_md_disks{state="active",job="node-exporter",device=~"(/dev/)?(mmcblk.p.+|nvme.+|rbd.+|sd.+|vd.+|xvd.+|dm-.+|md.+|dasd.+)"}) > 0
```

##### NodeBondingDegraded

`warning` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodebondingdegraded)

Bonding interface is degraded.

```promql
(node_bonding_slaves{job="node-exporter"} - node_bonding_active{job="node-exporter"}) != 0
```

##### NodeClockNotSynchronising

`warning` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodeclocknotsynchronising)

Clock not synchronising.

```promql
min_over_time(node_timex_sync_status{job="node-exporter"}[5m]) == 0 and node_timex_maxerror_seconds{job="node-exporter"} >= 16
```

##### NodeClockSkewDetected

`warning` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodeclockskewdetected)

Clock skew detected.

```promql
( node_timex_offset_seconds{job="node-exporter"} > 0.05 and deriv(node_timex_offset_seconds{job="node-exporter"}[5m]) >= 0 ) or ( node_timex_offset_seconds{job="node-exporter"} < -0.05 and deriv(node_timex_offset_seconds{job="node-exporter"}[5m]) <= 0 )
```

##### NodeDiskIOSaturation

`warning` · `for: 30m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodediskiosaturation)

Disk IO queue is high.

```promql
rate(node_disk_io_time_weighted_seconds_total{job="node-exporter", device=~"(/dev/)?(mmcblk.p.+|nvme.+|rbd.+|sd.+|vd.+|xvd.+|dm-.+|md.+|dasd.+)"}[5m]) > 10
```

##### NodeFileDescriptorLimit

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodefiledescriptorlimit)

Kernel is predicted to exhaust file descriptors limit soon.

```promql
( node_filefd_allocated{job="node-exporter"} * 100 / node_filefd_maximum{job="node-exporter"} > 70 )
```

##### NodeFilesystemAlmostOutOfFiles

`warning` · `for: 1h` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodefilesystemalmostoutoffiles)

Filesystem has less than 5% inodes left.

```promql
( node_filesystem_files_free{job="node-exporter",fstype!="",mountpoint!=""} / node_filesystem_files{job="node-exporter",fstype!="",mountpoint!=""} * 100 < 5 and node_filesystem_readonly{job="node-exporter",fstype!="",mountpoint!=""} == 0 )
```

##### NodeFilesystemAlmostOutOfSpace

`warning` · `for: 30m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodefilesystemalmostoutofspace)

Filesystem has less than 5% space left.

```promql
( node_filesystem_avail_bytes{job="node-exporter",fstype!="",mountpoint!=""} / node_filesystem_size_bytes{job="node-exporter",fstype!="",mountpoint!=""} * 100 < 5 and node_filesystem_readonly{job="node-exporter",fstype!="",mountpoint!=""} == 0 )
```

##### NodeFilesystemFilesFillingUp

`warning` · `for: 1h` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodefilesystemfilesfillingup)

Filesystem is predicted to run out of inodes within the next 24 hours.

```promql
( node_filesystem_files_free{job="node-exporter",fstype!="",mountpoint!=""} / node_filesystem_files{job="node-exporter",fstype!="",mountpoint!=""} * 100 < 40 and predict_linear(node_filesystem_files_free{job="node-exporter",fstype!="",mountpoint!=""}[6h], 24*60*60) < 0 and node_filesystem_readonly{job="node-exporter",fstype!="",mountpoint!=""} == 0 )
```

##### NodeFilesystemSpaceFillingUp

`warning` · `for: 1h` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodefilesystemspacefillingup)

Filesystem is predicted to run out of space within the next 24 hours.

```promql
( node_filesystem_avail_bytes{job="node-exporter",fstype!="",mountpoint!=""} / node_filesystem_size_bytes{job="node-exporter",fstype!="",mountpoint!=""} * 100 < 15 and predict_linear(node_filesystem_avail_bytes{job="node-exporter",fstype!="",mountpoint!=""}[6h], 24*60*60) < 0 and node_filesystem_readonly{job="node-exporter",fstype!="",mountpoint!=""} == 0 )
```

##### NodeHighNumberConntrackEntriesUsed

`warning` · `for: -` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodehighnumberconntrackentriesused)

Number of conntrack are getting close to the limit.

```promql
(node_nf_conntrack_entries{job="node-exporter"} / node_nf_conntrack_entries_limit) > 0.75
```

##### NodeMemoryHighUtilization

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodememoryhighutilization)

Host is running out of memory.

```promql
100 - (node_memory_MemAvailable_bytes{job="node-exporter"} / node_memory_MemTotal_bytes{job="node-exporter"} * 100) > 90
```

##### NodeMemoryMajorPagesFaults

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodememorymajorpagesfaults)

Memory major page faults are occurring at very high rate.

```promql
rate(node_vmstat_pgmajfault{job="node-exporter"}[5m]) > 500
```

##### NodeNetworkReceiveErrs

`warning` · `for: 1h` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodenetworkreceiveerrs)

Network interface is reporting many receive errors.

```promql
rate(node_network_receive_errs_total{job="node-exporter"}[2m]) / rate(node_network_receive_packets_total{job="node-exporter"}[2m]) > 0.01
```

##### NodeNetworkTransmitErrs

`warning` · `for: 1h` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodenetworktransmiterrs)

Network interface is reporting many transmit errors.

```promql
rate(node_network_transmit_errs_total{job="node-exporter"}[2m]) / rate(node_network_transmit_packets_total{job="node-exporter"}[2m]) > 0.01
```

##### NodeRAIDDiskFailure

`warning` · `for: -` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/noderaiddiskfailure)

Failed device in RAID array.

```promql
node_md_disks{state="failed",job="node-exporter",device=~"(/dev/)?(mmcblk.p.+|nvme.+|rbd.+|sd.+|vd.+|xvd.+|dm-.+|md.+|dasd.+)"} > 0
```

##### NodeSystemSaturation

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodesystemsaturation)

System saturated, load per core is very high.

```promql
node_load1{job="node-exporter"} / count without (cpu, mode) (node_cpu_seconds_total{job="node-exporter", mode="idle"}) > 2
```

##### NodeSystemdServiceCrashlooping

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodesystemdservicecrashlooping)

Systemd service keeps restaring, possibly crash looping.

```promql
increase(node_systemd_service_restart_total{job="node-exporter"}[5m]) > 2
```

##### NodeSystemdServiceFailed

`warning` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodesystemdservicefailed)

Systemd service has entered failed state.

```promql
node_systemd_unit_state{job="node-exporter", state="failed"} == 1
```

##### NodeTextFileCollectorScrapeError

`warning` · `for: -` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodetextfilecollectorscrapeerror)

Node Exporter text file collector failed to scrape.

```promql
node_textfile_scrape_error{job="node-exporter"} == 1
```

##### NodeCPUHighUsage

`info` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/node/nodecpuhighusage)

High CPU usage.

```promql
sum without(mode) (avg without (cpu) (rate(node_cpu_seconds_total{job="node-exporter", mode!~"idle|iowait"}[2m]))) * 100 > 90
```

#### node-network

<sub>PrometheusRule: `kube-prometheus-stack-kps-node-network` (generado por el chart)</sub>

##### NodeNetworkInterfaceFlapping

`warning` · `for: 2m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/general/nodenetworkinterfaceflapping)

Network interface is often changing its status

```promql
changes(node_network_up{job="node-exporter",device!~"veth.+"}[2m]) > 2
```

#### prometheus

<sub>PrometheusRule: `kube-prometheus-stack-kps-prometheus` (generado por el chart)</sub>

##### PrometheusBadConfig

`critical` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusbadconfig)

Failed Prometheus configuration reload.

```promql
# Without max_over_time, failed scrapes could create false negatives, see # https://www.robustperception.io/alerting-on-gauges-in-prometheus-2-0 for details. max_over_time(prometheus_config_last_reload_successful{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) == 0
```

##### PrometheusErrorSendingAlertsToAnyAlertmanager

`critical` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheuserrorsendingalertstoanyalertmanager)

Prometheus encounters more than 3% errors sending alerts to any Alertmanager.

```promql
min without (alertmanager) ( rate(prometheus_notifications_errors_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability",alertmanager!~``}[5m]) / rate(prometheus_notifications_sent_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability",alertmanager!~``}[5m]) ) * 100 > 3
```

##### PrometheusRemoteStorageFailures

`critical` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusremotestoragefailures)

Prometheus fails to send samples to remote storage.

```promql
( (rate(prometheus_remote_storage_failed_samples_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) or rate(prometheus_remote_storage_samples_failed_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m])) / ( (rate(prometheus_remote_storage_failed_samples_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) or rate(prometheus_remote_storage_samples_failed_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m])) + (rate(prometheus_remote_storage_succeeded_samples_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) or rate(prometheus_remote_storage_samples_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m])) ) ) * 100 > 1
```

##### PrometheusRemoteWriteBehind

`critical` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusremotewritebehind)

Prometheus remote write is behind.

```promql
# Without max_over_time, failed scrapes could create false negatives, see # https://www.robustperception.io/alerting-on-gauges-in-prometheus-2-0 for details. ( max_over_time(prometheus_remote_storage_queue_highest_timestamp_seconds{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) - max_over_time(prometheus_remote_storage_queue_highest_sent_timestamp_seconds{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) ) > 120
```

##### PrometheusRuleFailures

`critical` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusrulefailures)

Prometheus is failing rule evaluations.

```promql
increase(prometheus_rule_evaluation_failures_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) > 0
```

##### PrometheusTargetSyncFailure

`critical` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheustargetsyncfailure)

Prometheus has failed to sync targets.

```promql
increase(prometheus_target_sync_failed_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[30m]) > 0
```

##### PrometheusDuplicateTimestamps

`warning` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusduplicatetimestamps)

Prometheus is dropping samples with duplicate timestamps.

```promql
rate(prometheus_target_scrapes_sample_duplicate_timestamp_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) > 0
```

##### PrometheusErrorSendingAlertsToSomeAlertmanagers

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheuserrorsendingalertstosomealertmanagers)

More than 1% of alerts sent by Prometheus to a specific Alertmanager were affected by errors.

```promql
( rate(prometheus_notifications_errors_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) / rate(prometheus_notifications_sent_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) ) * 100 > 1
```

##### PrometheusHighQueryLoad

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheushighqueryload)

Prometheus is reaching its maximum capacity serving concurrent requests.

```promql
avg_over_time(prometheus_engine_queries{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) / max_over_time(prometheus_engine_queries_concurrent_max{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) > 0.8
```

##### PrometheusKubernetesListWatchFailures

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheuskuberneteslistwatchfailures)

Requests in Kubernetes SD are failing.

```promql
increase(prometheus_sd_kubernetes_failures_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) > 0
```

##### PrometheusLabelLimitHit

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheuslabellimithit)

Prometheus has dropped targets because some scrape configs have exceeded the labels limit.

```promql
increase(prometheus_target_scrape_pool_exceeded_label_limits_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) > 0
```

##### PrometheusMissingRuleEvaluations

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusmissingruleevaluations)

Prometheus is missing rule evaluations due to slow rule group evaluation.

```promql
increase(prometheus_rule_group_iterations_missed_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) > 0
```

##### PrometheusNotConnectedToAlertmanagers

`warning` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusnotconnectedtoalertmanagers)

Prometheus is not connected to any Alertmanagers.

```promql
# Without max_over_time, failed scrapes could create false negatives, see # https://www.robustperception.io/alerting-on-gauges-in-prometheus-2-0 for details. max_over_time(prometheus_notifications_alertmanagers_discovered{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) < 1
```

##### PrometheusNotIngestingSamples

`warning` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusnotingestingsamples)

Prometheus is not ingesting samples.

```promql
( sum without(type) (rate(prometheus_tsdb_head_samples_appended_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m])) <= 0 and ( sum without(scrape_job) (prometheus_target_metadata_cache_entries{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}) > 0 or sum without(rule_group) (prometheus_rule_group_rules{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}) > 0 ) )
```

##### PrometheusNotificationQueueRunningFull

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusnotificationqueuerunningfull)

Prometheus alert notification queue predicted to run full in less than 30m.

```promql
# Without min_over_time, failed scrapes could create false negatives, see # https://www.robustperception.io/alerting-on-gauges-in-prometheus-2-0 for details. ( predict_linear(prometheus_notifications_queue_length{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m], 60 * 30) > min_over_time(prometheus_notifications_queue_capacity{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) )
```

##### PrometheusOutOfOrderTimestamps

`warning` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusoutofordertimestamps)

Prometheus drops samples with out-of-order timestamps.

```promql
rate(prometheus_target_scrapes_sample_out_of_order_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) > 0
```

##### PrometheusRemoteWriteDesiredShards

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusremotewritedesiredshards)

Prometheus remote write desired shards calculation wants to run more than configured max shards.

```promql
# Without max_over_time, failed scrapes could create false negatives, see # https://www.robustperception.io/alerting-on-gauges-in-prometheus-2-0 for details. ( max_over_time(prometheus_remote_storage_shards_desired{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) > max_over_time(prometheus_remote_storage_shards_max{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) )
```

##### PrometheusSDRefreshFailure

`warning` · `for: 20m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheussdrefreshfailure)

Failed Prometheus SD refresh.

```promql
increase(prometheus_sd_refresh_failures_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[10m]) > 0
```

##### PrometheusScrapeBodySizeLimitHit

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusscrapebodysizelimithit)

Prometheus has dropped some targets that exceeded body size limit.

```promql
increase(prometheus_target_scrapes_exceeded_body_size_limit_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) > 0
```

##### PrometheusScrapeSampleLimitHit

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheusscrapesamplelimithit)

Prometheus has failed scrapes that have exceeded the configured sample limit.

```promql
increase(prometheus_target_scrapes_exceeded_sample_limit_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) > 0
```

##### PrometheusTSDBCompactionsFailing

`warning` · `for: 4h` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheustsdbcompactionsfailing)

Prometheus has issues compacting blocks.

```promql
increase(prometheus_tsdb_compactions_failed_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[3h]) > 0
```

##### PrometheusTSDBReloadsFailing

`warning` · `for: 4h` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheustsdbreloadsfailing)

Prometheus has issues reloading blocks from disk.

```promql
increase(prometheus_tsdb_reloads_failures_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[3h]) > 0
```

##### PrometheusTargetLimitHit

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus/prometheustargetlimithit)

Prometheus has dropped targets because some scrape configs have exceeded the targets limit.

```promql
increase(prometheus_target_scrape_pool_exceeded_target_limit_total{job="kps-kube-prometheus-stack-prometheus",namespace="observability"}[5m]) > 0
```

#### prometheus-operator

<sub>PrometheusRule: `kube-prometheus-stack-kps-prometheus-operator` (generado por el chart)</sub>

##### PrometheusOperatorListErrors

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus-operator/prometheusoperatorlisterrors)

Errors while performing list operations in controller.

```promql
(sum by (cluster,controller,namespace) (rate(prometheus_operator_list_operations_failed_total{job="kps-kube-prometheus-stack-operator",namespace="observability"}[10m])) / sum by (cluster,controller,namespace) (rate(prometheus_operator_list_operations_total{job="kps-kube-prometheus-stack-operator",namespace="observability"}[10m]))) > 0.4
```

##### PrometheusOperatorNodeLookupErrors

`warning` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus-operator/prometheusoperatornodelookuperrors)

Errors while reconciling Prometheus.

```promql
rate(prometheus_operator_node_address_lookup_errors_total{job="kps-kube-prometheus-stack-operator",namespace="observability"}[5m]) > 0.1
```

##### PrometheusOperatorNotReady

`warning` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus-operator/prometheusoperatornotready)

Prometheus operator not ready

```promql
min by (cluster,controller,namespace) (max_over_time(prometheus_operator_ready{job="kps-kube-prometheus-stack-operator",namespace="observability"}[5m]) == 0)
```

##### PrometheusOperatorReconcileErrors

`warning` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus-operator/prometheusoperatorreconcileerrors)

Errors while reconciling objects.

```promql
(sum by (cluster,controller,namespace) (rate(prometheus_operator_reconcile_errors_total{job="kps-kube-prometheus-stack-operator",namespace="observability"}[5m]))) / (sum by (cluster,controller,namespace) (rate(prometheus_operator_reconcile_operations_total{job="kps-kube-prometheus-stack-operator",namespace="observability"}[5m]))) > 0.1
```

##### PrometheusOperatorRejectedResources

`warning` · `for: 5m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus-operator/prometheusoperatorrejectedresources)

Resources rejected by Prometheus operator

```promql
min_over_time(prometheus_operator_managed_resources{state="rejected",job="kps-kube-prometheus-stack-operator",namespace="observability"}[5m]) > 0
```

##### PrometheusOperatorStatusUpdateErrors

`warning` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus-operator/prometheusoperatorstatusupdateerrors)

Errors while updating objects status.

```promql
(sum by (cluster,controller,namespace) (rate(prometheus_operator_status_update_errors_total{job="kps-kube-prometheus-stack-operator",namespace="observability"}[5m]))) / (sum by (cluster,controller,namespace) (rate(prometheus_operator_status_update_operations_total{job="kps-kube-prometheus-stack-operator",namespace="observability"}[5m]))) > 0.1
```

##### PrometheusOperatorSyncFailed

`warning` · `for: 10m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus-operator/prometheusoperatorsyncfailed)

Last controller reconciliation failed

```promql
min_over_time(prometheus_operator_syncs{status="failed",job="kps-kube-prometheus-stack-operator",namespace="observability"}[5m]) > 0
```

##### PrometheusOperatorWatchErrors

`warning` · `for: 15m` · [runbook](https://runbooks.prometheus-operator.dev/runbooks/prometheus-operator/prometheusoperatorwatcherrors)

Errors while performing watch operations in controller.

```promql
(sum by (cluster,controller,namespace) (rate(prometheus_operator_watch_operations_failed_total{job="kps-kube-prometheus-stack-operator",namespace="observability"}[5m])) / sum by (cluster,controller,namespace) (rate(prometheus_operator_watch_operations_total{job="kps-kube-prometheus-stack-operator",namespace="observability"}[5m]))) > 0.4
```

#### pve

<sub>PrometheusRule: `workloads/pve-exporter/prometheusrule.yaml` (propio del repo)</sub>

##### PveGuestDown

`critical` · `for: 5m`

Proxmox guest {{ $labels.name }} ({{ $labels.id }}) is not running

```promql
( (max by (id) (pve_up{id=~"(qemu|lxc)/.+"}) == 0) and on (id) (max by (id) (last_over_time(pve_onboot_status[1d])) == 1) ) * on (id) group_left (name, node) topk by (id) (1, last_over_time(pve_guest_info{name!=""}[1d]))
```

##### PveNodeDown

`critical` · `for: 5m`

Proxmox node {{ $labels.id }} is offline

```promql
max by (id) (pve_up{id=~"node/.+"}) == 0
```

##### PveClusterNotQuorate

`warning` · `for: 5m`

Proxmox cluster {{ $labels.id }} has lost quorum

```promql
max by (id) (pve_cluster_info{quorate="0"}) == 1
```

##### PveContainerDiskAlmostFull

`warning` · `for: 30m`

Root disk of {{ $labels.name }} ({{ $labels.id }}) is {{ $value | humanizePercentage }} full

```promql
( max by (id) (pve_disk_usage_bytes{id=~"lxc/.+"}) / (max by (id) (pve_disk_size_bytes{id=~"lxc/.+"}) > 0) > 0.9 ) * on (id) group_left (name, node) topk by (id) (1, last_over_time(pve_guest_info{name!=""}[1d]))
```

##### PveGuestNotBackedUp

`warning` · `for: 1h`

Proxmox guest {{ $labels.name }} ({{ $labels.id }}) is not covered by any backup job

```promql
max by (id) (pve_not_backed_up_info) * on (id) group_left (name, node) topk by (id) (1, last_over_time(pve_guest_info{name!="", template="0"}[1d]))
```

##### PveScrapeFailed

`warning` · `for: 10m`

Cannot scrape the Proxmox API on {{ $labels.instance }}

```promql
up{job="pve"} == 0
```

##### PveStorageAlmostFull

`warning` · `for: 30m`

Proxmox storage {{ $labels.id }} is {{ $value | humanizePercentage }} full

```promql
max by (id) (pve_disk_usage_bytes{id=~"storage/.+"}) / (max by (id) (pve_disk_size_bytes{id=~"storage/.+"}) > 0) > 0.85
```

## Recording rules

| Grupo | Serie |
|-------|-------|
| k8s.rules.container_cpu_usage_seconds_total | `node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate` |
| k8s.rules.container_cpu_usage_seconds_total | `node_namespace_pod_container:container_cpu_usage_seconds_total:sum_rate5m` |
| k8s.rules.container_memory_cache | `node_namespace_pod_container:container_memory_cache` |
| k8s.rules.container_memory_rss | `node_namespace_pod_container:container_memory_rss` |
| k8s.rules.container_memory_swap | `node_namespace_pod_container:container_memory_swap` |
| k8s.rules.container_memory_working_set_bytes | `node_namespace_pod_container:container_memory_working_set_bytes` |
| k8s.rules.container_resource | `cluster:namespace:pod_cpu:active:kube_pod_container_resource_limits` |
| k8s.rules.container_resource | `cluster:namespace:pod_cpu:active:kube_pod_container_resource_requests` |
| k8s.rules.container_resource | `cluster:namespace:pod_memory:active:kube_pod_container_resource_limits` |
| k8s.rules.container_resource | `cluster:namespace:pod_memory:active:kube_pod_container_resource_requests` |
| k8s.rules.container_resource | `namespace_cpu:kube_pod_container_resource_limits:sum` |
| k8s.rules.container_resource | `namespace_cpu:kube_pod_container_resource_requests:sum` |
| k8s.rules.container_resource | `namespace_memory:kube_pod_container_resource_limits:sum` |
| k8s.rules.container_resource | `namespace_memory:kube_pod_container_resource_requests:sum` |
| k8s.rules.pod_owner | `namespace_workload_pod:kube_pod_owner:relabel` |
| k8s.rules.pod_owner | `namespace_workload_pod:kube_pod_owner:relabel` |
| k8s.rules.pod_owner | `namespace_workload_pod:kube_pod_owner:relabel` |
| k8s.rules.pod_owner | `namespace_workload_pod:kube_pod_owner:relabel` |
| k8s.rules.pod_owner | `namespace_workload_pod:kube_pod_owner:relabel` |
| k8s.rules.pod_owner | `namespace_workload_pod:kube_pod_owner:relabel` |
| k8s.rules.pod_owner | `namespace_workload_pod:kube_pod_owner:relabel` |
| k8s.rules.pod_owner | `namespace_workload_pod:kube_pod_owner:relabel` |
| kube-apiserver-availability.rules | `apiserver_request:availability30d` |
| kube-apiserver-availability.rules | `apiserver_request:availability30d` |
| kube-apiserver-availability.rules | `apiserver_request:availability30d` |
| kube-apiserver-availability.rules | `cluster_verb_scope:apiserver_request_sli_duration_seconds_count:increase1h` |
| kube-apiserver-availability.rules | `cluster_verb_scope:apiserver_request_sli_duration_seconds_count:increase30d` |
| kube-apiserver-availability.rules | `cluster_verb_scope_le:apiserver_request_sli_duration_seconds_bucket:increase1h` |
| kube-apiserver-availability.rules | `cluster_verb_scope_le:apiserver_request_sli_duration_seconds_bucket:increase30d` |
| kube-apiserver-availability.rules | `code:apiserver_request_total:increase30d` |
| kube-apiserver-availability.rules | `code:apiserver_request_total:increase30d` |
| kube-apiserver-availability.rules | `code_resource:apiserver_request_total:rate5m` |
| kube-apiserver-availability.rules | `code_resource:apiserver_request_total:rate5m` |
| kube-apiserver-availability.rules | `code_verb:apiserver_request_total:increase1h` |
| kube-apiserver-availability.rules | `code_verb:apiserver_request_total:increase1h` |
| kube-apiserver-availability.rules | `code_verb:apiserver_request_total:increase1h` |
| kube-apiserver-availability.rules | `code_verb:apiserver_request_total:increase1h` |
| kube-apiserver-availability.rules | `code_verb:apiserver_request_total:increase30d` |
| kube-apiserver-burnrate.rules | `apiserver_request:burnrate1d` |
| kube-apiserver-burnrate.rules | `apiserver_request:burnrate1d` |
| kube-apiserver-burnrate.rules | `apiserver_request:burnrate1h` |
| kube-apiserver-burnrate.rules | `apiserver_request:burnrate1h` |
| kube-apiserver-burnrate.rules | `apiserver_request:burnrate2h` |
| kube-apiserver-burnrate.rules | `apiserver_request:burnrate2h` |
| kube-apiserver-burnrate.rules | `apiserver_request:burnrate30m` |
| kube-apiserver-burnrate.rules | `apiserver_request:burnrate30m` |
| kube-apiserver-burnrate.rules | `apiserver_request:burnrate3d` |
| kube-apiserver-burnrate.rules | `apiserver_request:burnrate3d` |
| kube-apiserver-burnrate.rules | `apiserver_request:burnrate5m` |
| kube-apiserver-burnrate.rules | `apiserver_request:burnrate5m` |
| kube-apiserver-burnrate.rules | `apiserver_request:burnrate6h` |
| kube-apiserver-burnrate.rules | `apiserver_request:burnrate6h` |
| kube-apiserver-histogram.rules | `cluster_quantile:apiserver_request_sli_duration_seconds:histogram_quantile` |
| kube-apiserver-histogram.rules | `cluster_quantile:apiserver_request_sli_duration_seconds:histogram_quantile` |
| kube-prometheus-general.rules | `count:up0` |
| kube-prometheus-general.rules | `count:up1` |
| kube-prometheus-node-recording.rules | `cluster:node_cpu:ratio` |
| kube-prometheus-node-recording.rules | `cluster:node_cpu:sum_rate5m` |
| kube-prometheus-node-recording.rules | `instance:node_cpu:rate:sum` |
| kube-prometheus-node-recording.rules | `instance:node_cpu:ratio` |
| kube-prometheus-node-recording.rules | `instance:node_network_receive_bytes:rate:sum` |
| kube-prometheus-node-recording.rules | `instance:node_network_transmit_bytes:rate:sum` |
| kubelet.rules | `node_quantile:kubelet_pleg_relist_duration_seconds:histogram_quantile` |
| kubelet.rules | `node_quantile:kubelet_pleg_relist_duration_seconds:histogram_quantile` |
| kubelet.rules | `node_quantile:kubelet_pleg_relist_duration_seconds:histogram_quantile` |
| node-exporter.rules | `instance:node_cpu_utilisation:rate5m` |
| node-exporter.rules | `instance:node_load1_per_cpu:ratio` |
| node-exporter.rules | `instance:node_memory_utilisation:ratio` |
| node-exporter.rules | `instance:node_network_receive_bytes_excluding_lo:rate5m` |
| node-exporter.rules | `instance:node_network_receive_bytes_physical:rate5m` |
| node-exporter.rules | `instance:node_network_receive_drop_excluding_lo:rate5m` |
| node-exporter.rules | `instance:node_network_receive_drop_physical:rate5m` |
| node-exporter.rules | `instance:node_network_transmit_bytes_excluding_lo:rate5m` |
| node-exporter.rules | `instance:node_network_transmit_bytes_physical:rate5m` |
| node-exporter.rules | `instance:node_network_transmit_drop_excluding_lo:rate5m` |
| node-exporter.rules | `instance:node_network_transmit_drop_physical:rate5m` |
| node-exporter.rules | `instance:node_num_cpu:sum` |
| node-exporter.rules | `instance:node_vmstat_pgmajfault:rate5m` |
| node-exporter.rules | `instance_device:node_disk_io_time_seconds:rate5m` |
| node-exporter.rules | `instance_device:node_disk_io_time_weighted_seconds:rate5m` |
| node.rules | `:node_memory_MemAvailable_bytes:sum` |
| node.rules | `cluster:node_cpu:ratio_rate5m` |
| node.rules | `node:node_cpu_utilization:ratio_rate5m` |
| node.rules | `node:node_num_cpu:sum` |
| node.rules | `node_namespace_pod:kube_pod_info:` |
| workload-resources | `node_namespace_workload_pod:container_network_receive_bytes_total:sum_rate5m` |
| workload-resources | `node_namespace_workload_pod:container_network_transmit_bytes_total:sum_rate5m` |
| workload-resources | `node_namespace_workload_pod_container:container_cpu_usage_seconds_total:sum_rate5m` |
| workload-resources | `node_namespace_workload_pod_container:container_memory_cache:sum` |
| workload-resources | `node_namespace_workload_pod_container:container_memory_rss:sum` |
| workload-resources | `node_namespace_workload_pod_container:container_memory_usage_bytes:sum` |
| workload-resources | `node_namespace_workload_pod_container:container_memory_working_set_bytes:sum` |
| workload-resources | `node_namespace_workload_pod_container:kube_pod_container_resource_limits_cpu:sum` |
| workload-resources | `node_namespace_workload_pod_container:kube_pod_container_resource_limits_memory:sum` |
| workload-resources | `node_namespace_workload_pod_container:kube_pod_container_resource_requests_cpu:sum` |
| workload-resources | `node_namespace_workload_pod_container:kube_pod_container_resource_requests_memory:sum` |

