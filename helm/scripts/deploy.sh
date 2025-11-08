#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
DEFAULT_CHART_DIR=$(dirname "$SCRIPT_DIR")
CHART_DIR=${CHART_PATH:-$DEFAULT_CHART_DIR}
ENV_FILE="${CHART_DIR}/env"

if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  CHART_DIR=${CHART_PATH:-$DEFAULT_CHART_DIR}
fi

HELM_BIN=${HELM_BIN:-helm}
RELEASE_NAME=${RELEASE_NAME:-scb-app}
NAMESPACE=${NAMESPACE:-default}
VALUES_FILES=${VALUES_FILES:-"values.yaml values.secrets.yaml"}
KUBE_CONTEXT=${KUBE_CONTEXT:-}

export HELM_SECRETS_DRIVER=${HELM_SECRETS_DRIVER:-vals}
export VALS_ADDR=${VALS_ADDR:-}
export VALS_AUTH=${VALS_AUTH:-}
export VALS_AUTH_APPROLE_ROLE_ID=${VALS_AUTH_APPROLE_ROLE_ID:-}
export VALS_AUTH_APPROLE_SECRET_ID=${VALS_AUTH_APPROLE_SECRET_ID:-}

COMMAND=($HELM_BIN secrets upgrade --install "$RELEASE_NAME" "$CHART_DIR")

for file in $VALUES_FILES; do
  if [[ "$file" = /* ]]; then
    COMMAND+=(-f "$file")
  else
    COMMAND+=(-f "$CHART_DIR/$file")
  fi
done

if [[ -n "$NAMESPACE" ]]; then
  COMMAND+=(--namespace "$NAMESPACE" --create-namespace)
fi

if [[ -n "$KUBE_CONTEXT" ]]; then
  COMMAND+=(--kube-context "$KUBE_CONTEXT")
fi

COMMAND+=("$@")

printf 'Executing:'
printf ' %q' "${COMMAND[@]}"
printf '\n'
exec "${COMMAND[@]}"
