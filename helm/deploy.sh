#!/bin/bash

set -a
source .env
set +a


helm secrets \
    --evaluate-templates \
    -b vals \
    upgrade --install app app -n app -f vault-secrets.yaml

#vals eval -f vault-secrets.yaml