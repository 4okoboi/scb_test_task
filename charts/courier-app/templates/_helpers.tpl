{{- define "courier-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "courier-app.fullname" -}}
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

{{- define "courier-app.labels" -}}
helm.sh/chart: {{ include "courier-app.chart" . }}
{{ include "courier-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- define "courier-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "courier-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{- define "courier-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" -}}
{{- end -}}

{{- define "courier-app.backend.fullname" -}}
{{ printf "%s-backend" (include "courier-app.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end -}}

{{- define "courier-app.postgres.fullname" -}}
{{ printf "%s-postgres" (include "courier-app.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end -}}

{{- define "courier-app.postgres.headless" -}}
{{ printf "%s-headless" (include "courier-app.postgres.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end -}}

{{- define "courier-app.namespace" -}}
{{- if .Values.namespace.name -}}
{{ .Values.namespace.name }}
{{- else -}}
{{ .Release.Namespace }}
{{- end -}}
{{- end -}}

{{- define "courier-app.postgres.pvcName" -}}
{{- if .Values.postgres.persistence.existingClaim -}}
{{ .Values.postgres.persistence.existingClaim }}
{{- else -}}
{{ printf "%s-pvc" (include "courier-app.postgres.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end -}}
{{- end -}}

{{- define "courier-app.postgres.waitServiceFQDN" -}}
{{- printf "%s.%s.svc.cluster.local" (include "courier-app.postgres.fullname" .) (include "courier-app.namespace" .) -}}
{{- end -}}

{{- define "courier-app.postgres.primaryHost" -}}
{{- printf "%s-0.%s.%s.svc.cluster.local" (include "courier-app.postgres.fullname" .) (include "courier-app.postgres.headless" .) (include "courier-app.namespace" .) -}}
{{- end -}}
