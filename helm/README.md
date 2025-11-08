# SCB Application Helm Chart

This chart packages the backend application together with PostgreSQL and a Vault instance configured for secret management.

## Prerequisites

* Kubernetes 1.26+
* [Helm 3.12+](https://helm.sh)
* [helm-secrets](https://github.com/jkroepke/helm-secrets) plugin with the `vals` backend
* A running Vault cluster reachable from your workstation
* An AppRole in Vault that can read the paths referenced in `values.secrets.yaml`

## Repository layout

```
helm/
├── Chart.yaml                # Root chart definition
├── values.yaml               # Default configuration
├── values.secrets.yaml       # Sensitive values resolved via Vault
├── env / env-example         # Environment variables for helm-secrets deploys
├── scripts/deploy.sh         # Wrapper around `helm secrets upgrade`
├── templates/                # Application manifests (Deployment, Service, etc.)
└── charts/
    ├── postgres/             # Stateful PostgreSQL subchart
    └── vault/                # Lightweight Vault subchart
```

The chart follows common Helm best practices: configurable names, optional components, helper templates for labels and selectors, and the use of `stringData` for secrets. Dependent services (PostgreSQL and Vault) are implemented as subcharts to keep responsibilities isolated.

## Preparing Vault secrets

1. Initialise and unseal Vault. For a single-node dev cluster you can run:
   ```bash
   vault operator init
   vault operator unseal
   ```
2. Enable KV v2 at `kv/`:
   ```bash
   vault secrets enable -path=kv kv-v2
   ```
3. Create a policy that grants read access to the application secret paths (see `vault/policies/app-policy.hcl` example below):
   ```hcl
   path "kv/data/app/backend" {
     capabilities = ["read"]
   }
   path "kv/data/app/ci" {
     capabilities = ["read"]
   }
   ```
   Apply it with `vault policy write scb-app policies/app-policy.hcl`.
4. Enable AppRole authentication and create a role bound to the policy:
   ```bash
   vault auth enable approle
   vault write auth/approle/role/scb-app token_policies="scb-app" token_ttl=1h token_max_ttl=4h
   vault read auth/approle/role/scb-app/role-id
   vault write -f auth/approle/role/scb-app/secret-id
   ```
5. Store application secrets in Vault:
   ```bash
   vault kv put kv/app/backend \
     POSTGRES_USER=dbuser \
     POSTGRES_PASSWORD=dbpassword \
     AUTH_SECRET_KEY=supersecret \
     DADATA_API_KEY=dadata-key

   vault kv put kv/app/ci \
     role_id=<role-id> \
     secret_id=<secret-id>
   ```

The chart references these paths via `ref+vault://` expressions in `values.secrets.yaml` and `env`. When rendered with `helm secrets`, the plugin will query Vault, inject the actual values, and create a Kubernetes `Secret` manifest.

## Deploying the chart

### Dry run without touching the cluster

```bash
helm template scb-app ./helm -f helm/values.yaml -f helm/values.secrets.yaml --debug
```

### Using helm-secrets with vals

```bash
# Optional: inspect the manifest without installing
helm secrets template scb-app ./helm -f helm/values.yaml -f helm/values.secrets.yaml

# Deploy/upgrade using the wrapper script
./helm/scripts/deploy.sh
```

The script sources `helm/env` (or `env-example` when copied) to populate the `VALS_*` variables required for AppRole authentication.

### Tearing down

```bash
helm secrets uninstall scb-app --namespace app
```

## Customisation tips

* Override any value by creating an additional YAML file and passing it through `-f my-values.yaml`.
* Disable bundled dependencies when targeting managed services:
  ```bash
  helm secrets upgrade --install scb-app ./helm \
    --set postgres.enabled=false \
    --set vault.enabled=false
  ```
* Replace static host paths by providing an existing storage class or an external PVC through the PostgreSQL subchart values.
* To reuse an externally managed secret instead of creating one, set:
  ```yaml
  secret:
    create: false
    existingSecret: my-existing-secret
  ```
  and adjust the `global.database.secretName` value accordingly.

## Vault initialisation helper manifests

The Vault subchart exposes the HTTP API and UI. After installation you can port-forward the service to access the UI:

```bash
kubectl -n vault port-forward svc/scb-app-vault 8200:8200
```

The subchart enables storage persistence via a `volumeClaimTemplates`. Disable persistence for ephemeral environments with `--set vault.server.storage.enabled=false`.

## Validating templates

Run Helm's built-in linter:

```bash
helm lint ./helm
```

And render manifests with the same values the deploy script uses:

```bash
helm secrets template scb-app ./helm -f helm/values.yaml -f helm/values.secrets.yaml
```

## Notes on secrets

* All sensitive data is referenced through Vault URLs; no secret values are stored in the repository.
* The charts only generate application secrets. TLS certificates or other cluster-managed secrets can be supplied externally.
* The PostgreSQL subchart consumes the same secret as the application to ensure credentials remain in sync.
