Drop any locally-required root CA certs here (PEM, `.crt` extension) —
e.g. a corporate proxy or antivirus TLS-inspection cert your machine needs
to reach PyPI through. Picked up automatically by the Dockerfile via
`update-ca-certificates`. Gitignored: machine-specific, not shared.
