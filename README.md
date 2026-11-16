# Cert Window

Know when a TLS certificate is approaching expiry before it becomes an outage. Cert Window makes one bounded TLS connection and reports the peer certificate's expiry date.

![Animated certificate beacon](assets/hero.svg)

## Features
- Reads the certificate presented by a hostname and port.
- Classifies expiry as expired, critical (7 days), soon (30 days), or okay.
- Uses the platform trust store and hostname verification.
- Supports JSON output and a configurable timeout.

## Run

Python 3.10+, standard library only.

```bash
python tool.py example.com
python tool.py example.com --port 8443 --timeout 4 --json
python -m unittest -v
```

## Safety and scope
The tool performs a read-only TLS handshake. It does not scan subdomains, inspect private keys, or replace certificate-transparency monitoring. A successful handshake only describes the endpoint reached at that moment.

## Design
A lighthouse-like certificate beacon uses restrained maritime colors. Motion is decorative and reduced-motion aware.

## License
MIT.
