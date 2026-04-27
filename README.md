# Usage

Site is using some weird TLS setup and root cert is currently being phased out (Digicert G1)
Set env var:

```
export OPENSSL_CONF=./src/ledger_sync/ssl/openssl.cnf
```

We also have to tell `niquests` to verify the site against the cert in `./src/ledger_sync/ssl/_.mara.gov.pem`

# Superset

Superset dropped sqlite support, we have to enable by settings:

```
PREVENT_UNSAFE_DB_CONNECTIONS = False
```

In `config.py` file, as shown in [#9748](https://github.com/apache/superset/issues/9748)
