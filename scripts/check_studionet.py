"""Fail closed unless the configured RPC reports Studionet chain ID 61999."""

import json
import urllib.request

RPC = "https://studio.genlayer.com/api"
EXPECTED = 61999

payload = json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "method": "eth_chainId",
    "params": [],
}).encode("utf-8")

request = urllib.request.Request(
    RPC,
    data=payload,
    headers={
        "Content-Type": "application/json",
        "User-Agent": "minima-chain-guard/1.0",
    },
    method="POST",
)

try:
    with urllib.request.urlopen(request, timeout=20) as response:
        body = json.loads(response.read().decode("utf-8"))
except Exception as exc:
    raise SystemExit(f"NETWORK GUARD FAIL: could not query {RPC}: {exc}")

raw = body.get("result")
if not isinstance(raw, str):
    raise SystemExit(f"NETWORK GUARD FAIL: malformed eth_chainId response: {body}")

actual = int(raw, 16)
print(f"RPC: {RPC}")
print(f"chainId: {actual}")
if actual != EXPECTED:
    raise SystemExit(f"NETWORK GUARD FAIL: expected {EXPECTED}, got {actual}")

print("NETWORK GUARD PASS: Studionet 61999")
