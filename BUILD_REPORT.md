# MINIMA build report

Prepared as a standalone GenLayer Intelligent Contract package for `lolaaa00/minima`.

## Completed in this package

- contract implementation: `contracts/minima.py`;
- independent custom validator path using `run_nondet_unsafe`;
- immutable schema and purpose hashes;
- complete-field classification validation;
- ambiguity fail-closed behaviour;
- exact consensus-derived least-privilege permit mask;
- requester / consumer / schema / purpose / action / TTL binding;
- purpose and permit revocation;
- 39 adversarial Direct Mode test cases;
- threat model, architecture and reviewer demo;
- stable Studionet network manifest;
- repository-local GenLayer CLI pin at `0.39.1`;
- strict preflight that rejects preview-network contamination;
- deployment evidence template with no fabricated address or transaction;
- detailed Codex handoff.

## Checks actually run on 2026-10-17

- `npm install` — PASS; lockfile generated;
- `npm run genlayer -- --version` — PASS, `0.39.1`;
- `GENVM_VERSION=v0.2.16 genvm-lint check contracts/minima.py` — PASS, 3 checks and SDK validation;
- `pytest tests/direct -q` — PASS, 39 tests;
- `python scripts/check_studionet.py` — PASS, live RPC chain ID `61999`;
- `python scripts/preflight.py` — PASS.

## Open release gates

This folder began without Git metadata. A local repository was initialized, but the owner has not yet supplied the separately-created `lolaaa00/minima` remote. No push or GitHub Actions run is claimed.

Live deployment, finalized lifecycle transactions, source parity against deployed code, and explorer evidence remain pending until a funded Studionet signer is available. `DEPLOYMENT.md` intentionally retains explicit `PENDING` fields.

`npm audit` reports six vulnerabilities in transitive dependencies of the exact required `genlayer@0.39.1` CLI (four moderate, two critical). The suggested automated fix replaces the required CLI with an incompatible version, so it was not applied. The CLI remains development-only and exactly pinned as required.

The finishing agent must run those checks locally and fix any runtime/tooling incompatibility before submission.
