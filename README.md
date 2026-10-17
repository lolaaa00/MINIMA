# MINIMA

**Consensus-backed field minimisation and least-privilege data permits for GenLayer Intelligent Contracts.**

MINIMA is a standalone reusable Intelligent Contract primitive for systems that already know *why* an agent or application wants access to a dataset, but need a neutral shared decision about the **smallest declared field set actually necessary for that purpose**.

It does not store customer records, secrets, health data, credentials, or any other private payload. It stores only:

- a public field catalogue (names, descriptions, sensitivity labels);
- sealed purpose definitions;
- field-level minimisation decisions;
- definition hashes and action hashes; and
- least-privilege permits.

The central invariant is:

> A MINIMA permit contains exactly the fields that independent validators agree are **NECESSARY** for the sealed purpose. A caller cannot add fields to the permit, and any **AMBIGUOUS** field makes the request fail closed with no permit.

## Why this is a GenLayer primitive

Ordinary smart contracts can enforce bitmasks, owners, expiries, hashes, revocation, and consumer binding. They cannot reliably decide whether a natural-language purpose genuinely requires a declared field such as `street_address`, `email`, `date_of_birth`, or `passport_number`.

MINIMA splits the problem:

- **GenLayer consensus** evaluates only the semantic necessity relation between the frozen purpose and every field definition.
- **Deterministic code** freezes schemas/purposes, validates complete field coverage, derives masks, refuses ambiguity, issues permits, binds hashes/actors/action/expiry, and handles revocation.
- **No LLM chooses data values, recipients, TTLs, consumers, or permissions.**

This is deliberately not a generic `AI decides access` contract. The model has one bounded job: classify every frozen field as `NECESSARY`, `NOT_NECESSARY`, or `AMBIGUOUS`.

## Example

Sealed purpose:

> Determine the destination needed to route one physical parcel to the customer's declared delivery address. No notifications, identity verification, age checks, analytics, marketing, or secondary use are part of this purpose.

Declared schema:

```text
street_address    PERSONAL
email             PERSONAL
date_of_birth     SENSITIVE
passport_number   RESTRICTED
```

Consensus result:

```text
street_address    NECESSARY
email             NOT_NECESSARY
date_of_birth     NOT_NECESSARY
passport_number   NOT_NECESSARY
```

Permit:

```text
field_mask = 0b0001
```

There is no method argument that can turn that into `0b1111` after consensus.

If `email` is `AMBIGUOUS`, MINIMA issues **no permit at all**.

## Protocol model

```text
Schema DRAFT
  │ add field definitions
  ▼
Schema SEALED ───────────────┐
                             │
Purpose DRAFT                │ pins exact schema hash
  │                          │
  ▼                          │
Purpose ACTIVE ──────────────┘
  │
  │ authorised requester + exact action hash
  ▼
Request PENDING
  │
  │ GenLayer consensus over every declared field
  ▼
┌───────────────────────┬───────────────────────┐
│ no ambiguous fields   │ any ambiguous field   │
▼                       ▼
RESOLVED                 AMBIGUOUS
│                        │
│ deterministic          └── no permit
│ necessary_mask
▼
Permit ACTIVE
│
├── schema hash
├── purpose hash
├── requester
├── consumer
├── action hash
├── exact necessary field mask
└── expiry
```

## Consensus design

The leader returns a complete field classification. The custom validator independently runs the same frozen purpose and complete field catalogue.

A proposal is accepted only when:

1. every declared field ID appears exactly once;
2. no unknown or duplicate field is introduced;
3. every verdict is one of the three allowed states;
4. the leader and validator independently agree on the **NECESSARY mask**; and
5. the leader and validator independently agree on the **AMBIGUOUS mask**.

`NOT_NECESSARY` is then the deterministic complement of those economically meaningful masks. This avoids rejecting consensus merely because two validators use different diagnostic language for an excluded field while still requiring exact agreement on what can be released and what remains uncertain.

Malformed or incomplete model output becomes ambiguity over the complete field universe and therefore cannot mint a permit.

Action hashes use one canonical representation: exactly 64 lowercase hexadecimal characters with no `0x` prefix. Alternate casing and malformed digests are rejected before a request is created.

## Public interface

Writes:

```text
create_schema(name, description)
add_field(schema_id, name, description, sensitivity)
seal_schema(schema_id)
create_purpose(schema_id, label, purpose_text, authorized_requester, consumer, ttl_seconds)
seal_purpose(purpose_id)
revoke_purpose(purpose_id)
open_request(purpose_id, action_hash)
resolve_request(request_id)
cancel_request(request_id)
revoke_permit(permit_id)
```

Views:

```text
get_schema(schema_id)
get_field(field_id)
get_purpose(purpose_id)
get_request(request_id)
get_permit(permit_id)
current_schema_hash(schema_id)
current_purpose_hash(purpose_id)
is_permit_valid(permit_id, expected_schema_hash, expected_purpose_hash, expected_action_hash, expected_consumer)
```

## Security boundaries

MINIMA intentionally does **not** claim that:

- a permitted purpose is lawful, ethical, or desirable;
- a schema description is truthful merely because its owner published it;
- private values should ever be put on-chain;
- a field judged necessary should automatically be disclosed by an external database;
- an integrating data vault can skip its own authentication, authorisation, replay controls, or audit logging; or
- the contract can infer undeclared fields or hidden business processes.

MINIMA is a **purpose-to-field minimisation primitive**, not a private-data store and not legal advice.

See `docs/THREAT_MODEL.md`.

## No frontend

There is intentionally **no frontend**. MINIMA belongs in the standalone **Intelligent Contracts** category. A frontend would push the work toward a Project and does not improve the primitive itself.

## Network target — StudioNet only

```text
Network:   Studionet
Chain ID:  61999
RPC:       https://studio.genlayer.com/api
Explorer:  https://explorer-studio.genlayer.com
Currency:  GEN
CLI:       genlayer 0.39.1 (repository-local)
```

The repository is guarded against release-candidate preview configuration. Run `python scripts/preflight.py` before deployment.

## Local setup

Python 3.12 is recommended for the pinned Direct Mode stack.

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
npm install
```

Run the contract checks:

```bash
npm run genlayer -- --version
npm run genlayer -- network set studionet
npm run genlayer -- network info
python scripts/check_studionet.py

GENVM_VERSION=v0.2.16 genvm-lint check contracts/minima.py
pytest tests/direct -v                 # 39 adversarial tests
python scripts/preflight.py
```

The CLI version must be `0.39.1` and the chain guard must report `61999` before any deployment.

## Deployment

MINIMA is finalized on Studionet at [`0x180bC04e85Eb45Fab80354badC12a73ec7a76B66`](https://explorer-studio.genlayer.com/tx/0xce7df652b2c0a063bb74204efb85c6bed960b7ac9e6bb76e3f1fb563c257b29e).

- Deployment commit: `47203f155a46558eeaca0afca9951fa2778e755b`
- Contract source SHA-256: `2209e8b245326a416e8818a740e405a6ec8a3bc5b8d360373976b2f6f5009b73`
- Deployment status: `FINALIZED`
- Live consensus result: necessary mask `3`, excluded mask `28`, ambiguity mask `0`
- Live revocation result: the previously valid permit became invalid

See `DEPLOYMENT.md` for the complete schema, purpose, request, permit, binding, source-parity, transaction, and revocation evidence. GitHub publication and CI remain unclaimed until the separately-created `lolaaa00/minima` remote is connected.

## Repository layout

```text
contracts/minima.py
tests/direct/test_minima.py
tests/integration/
docs/ARCHITECTURE.md
docs/THREAT_MODEL.md
docs/REVIEWER_DEMO.md
docs/SUBMISSION_NOTES_DRAFT.md
scripts/check_studionet.py
scripts/preflight.py
DEPLOYMENT.md
MINIMA_CODEX_MASTER_HANDOFF.txt
```

## License

MIT
