#!/usr/bin/env python3
"""Inspect the expiry window of a remote TLS certificate."""
import argparse, datetime as dt, json, socket, ssl

def expiry_status(not_after, now=None):
    now=now or dt.datetime.now(dt.timezone.utc)
    expiry=dt.datetime.strptime(not_after,"%b %d %H:%M:%S %Y %Z").replace(tzinfo=dt.timezone.utc)
    days=(expiry-now).total_seconds()/86400
    state="expired" if days < 0 else "critical" if days <= 7 else "soon" if days <= 30 else "okay"
    return {"expires_at":expiry.isoformat(),"days_remaining":round(days,2),"status":state}

def inspect(host, port=443, timeout=5):
    context=ssl.create_default_context()
    with socket.create_connection((host,port),timeout=timeout) as raw:
        with context.wrap_socket(raw,server_hostname=host) as tls:
            cert=tls.getpeercert()
    if not cert or "notAfter" not in cert: raise RuntimeError("peer did not provide a parseable certificate expiry")
    return {"host":host,"port":port,**expiry_status(cert["notAfter"])}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("host"); p.add_argument("--port",type=int,default=443); p.add_argument("--timeout",type=float,default=5); p.add_argument("--json",action="store_true")
    a=p.parse_args(argv)
    if not 0 < a.timeout <= 30: p.error("--timeout must be between 0 and 30 seconds")
    try: result=inspect(a.host,a.port,a.timeout)
    except (OSError,ssl.SSLError,RuntimeError,ValueError) as exc: p.error(str(exc))
    print(json.dumps(result,indent=2) if a.json else f'{result["host"]}:{result["port"]} — {result["status"]}, {result["days_remaining"]} days left (expires {result["expires_at"]})')
    return 1 if result["status"] in ("expired","critical") else 0
if __name__=="__main__": raise SystemExit(main())
