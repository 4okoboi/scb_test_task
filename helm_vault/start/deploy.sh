#!/bin/bash

set -a
source .env
set +a


helm secrets \
    --evaluate-templates \
    -b vals \
    install  {{release}} {{chart}}