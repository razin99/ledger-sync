Site is using some weird TLS setup and root cert is currently being phased out (Digicert G1)
Set env var:

```
export OPENSSL_CONF=./ssl/openssl.cnf
```

We also have to tell `niquests` to verify the site against the cert in `./ssl/_.mara.gov.pem`
