{{- define "scb-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "scb-app.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "scb-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" -}}
{{- end -}}

{{- define "scb-app.labels" -}}
helm.sh/chart: {{ include "scb-app.chart" . }}
{{ include "scb-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- define "scb-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "scb-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{- define "scb-app.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
{{- default (include "scb-app.fullname" .) .Values.serviceAccount.name -}}
{{- else -}}
{{- default "default" .Values.serviceAccount.name -}}
{{- end -}}
{{- end -}}

{{- define "scb-app.configMapName" -}}
{{- default (printf "%s-config" (include "scb-app.fullname" .)) .Values.config.name -}}
{{- end -}}

{{- define "scb-app.secretName" -}}
{{- if .Values.secret.existingSecret -}}
{{- .Values.secret.existingSecret -}}
{{- else -}}
{{- default (printf "%s-secret" (include "scb-app.fullname" .)) .Values.secret.name -}}
{{- end -}}
{{- end -}}

{{- define "scb-app.serviceName" -}}
{{- default (include "scb-app.fullname" .) .Values.service.name -}}
{{- end -}}

{{- define "scb-app.postgresStatefulBase" -}}
{{- if and .Values.postgres.enabled .Subcharts.postgres -}}
{{- include "postgres.fullname" .Subcharts.postgres -}}
{{- else -}}
{{- default "postgres" .Values.postgres.fullnameOverride -}}
{{- end -}}
{{- end -}}

{{- define "scb-app.postgresServiceName" -}}
{{- if .Values.postgres.service.name -}}
{{- .Values.postgres.service.name -}}
{{- else -}}
{{- if and .Values.postgres.enabled .Subcharts.postgres -}}
{{- printf "%s-rw" (include "scb-app.postgresStatefulBase" .) -}}
{{- else -}}
postgres-clusterip
{{- end -}}
{{- end -}}
{{- end -}}

{{- define "scb-app.postgresServiceHost" -}}
{{- if .Values.postgres.service.host -}}
{{- .Values.postgres.service.host -}}
{{- else -}}
{{- printf "%s.%s.svc.cluster.local" (include "scb-app.postgresServiceName" .) .Release.Namespace -}}
{{- end -}}
{{- end -}}

{{- define "scb-app.postgresReadWriteHost" -}}
{{- if .Values.postgres.service.readWriteHost -}}
{{- .Values.postgres.service.readWriteHost -}}
{{- else -}}
{{- $base := include "scb-app.postgresStatefulBase" . -}}
{{- printf "%s-0.%s.%s.svc.cluster.local" $base $base .Release.Namespace -}}
{{- end -}}
{{- end -}}
