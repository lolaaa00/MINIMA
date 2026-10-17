# Reviewer demo

The final submission should show both adversarial Direct Mode behaviour and one finalized Studionet lifecycle.

## Part A — Direct Mode

Run:

```bash
pytest tests/direct -v
```

Reviewer-relevant cases include:

1. sealed schemas cannot gain fields;
2. duplicate fields are rejected;
3. purpose/schema metadata cannot be an obvious prompt-injection channel;
4. an unauthorised requester cannot open a request;
5. malformed model output becomes ambiguity;
6. missing or duplicate field IDs become ambiguity;
7. one ambiguous field yields no permit;
8. a restricted field does not become necessary merely because of sensitivity;
9. a permit contains exactly the necessary bitmask;
10. purpose revocation invalidates outstanding permits;
11. permit validation pins schema, purpose, action and consumer;
12. expiry is deterministic.

The current suite contains 39 meaningful tests. It additionally exercises invented and boolean field IDs, unsupported verdicts, model-supplied mask injection, reason-code independence, exact leader/validator necessary-mask and ambiguity-mask disagreement, zero consumers, TTL bounds, wildcard requester attribution, transition finality, and revocation authorization.

## Part B — live Studionet lifecycle (61999)

Do not use a preview network.

### 1. Deploy

Deploy `contracts/minima.py` with the repository-local CLI and record the finalized deployment transaction and address in `DEPLOYMENT.md`.

### 2. Create schema

Create a `Shipping profile` schema and add four fields in this exact order:

```text
0 street_address  PERSONAL
1 email           PERSONAL
2 date_of_birth   SENSITIVE
3 passport_number RESTRICTED
```

Seal the schema and record the resulting definition hash.

### 3. Create sealed purpose

Purpose:

> Determine the destination needed to route one physical parcel to the customer's declared delivery address. No notifications, identity verification, age checks, analytics, marketing, or secondary use are part of this purpose.

Bind a real test requester address and a dedicated test consumer address. Use a short but safe TTL for the demonstration.

Seal it and record the purpose hash.

### 4. Resolve a request

From the authorised requester:

- open the request with a real 32-byte action hash;
- resolve it;
- wait for ACCEPTED and then FINALIZED;
- record the request transaction, result and permit ID.

Expected conceptual result:

```text
street_address  NECESSARY
others          NOT_NECESSARY
field_mask      1
```

Do not falsify the proof if live validators classify differently. If the result is ambiguous, sharpen the purpose/field definitions on a fresh purpose version and repeat. Never edit evidence to match a desired verdict.

### 5. Prove binding

Record view outputs showing:

```text
is_permit_valid(correct hashes/action/consumer) == true
is_permit_valid(wrong action hash) == false
is_permit_valid(wrong consumer) == false
```

### 6. Prove revocation

Revoke the purpose or permit and show that the same previously-valid permit becomes invalid without rewriting the historical permit receipt.

## Evidence standard

Every live proof in the final README/DEPLOYMENT file must include:

- contract address;
- exact transaction hash;
- explorer link;
- ACCEPTED versus FINALIZED distinction;
- relevant definition/action hashes;
- result/permit IDs;
- repository commit SHA used for deployment.

No placeholder may remain in the final submitted evidence section.
