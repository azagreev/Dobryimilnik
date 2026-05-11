# Environment and Secrets

Phase 1 separates runtime configuration from committed code.

## Environments

Supported backend environments are:

- `local`
- `prod`

No third environment is introduced in Phase 1.

## Secret Files

The repository intentionally does not include `.env.example`. Local developers create ignored files under `secrets/local/`:

- `secrets/local/postgres_password.txt`
- `secrets/local/backend_secret_key.txt`

Docker Compose passes secret locations to the backend through:

- `POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password`
- `SECRET_KEY_FILE=/run/secrets/backend_secret_key`

The backend reads these files at runtime and does not require committed secret values for settings construction.

## Production Secret Provider

Yandex Lockbox is deferred beyond Phase 1. Production integration will be implemented when deployment and external credentials are in scope.
