#!/bin/bash

set -a
source .env
set +a


helm secrets \
    --evaluate-templates \
    -b vals \
    upgrade --install vault-app app -n vault -f vault-secrets.yaml