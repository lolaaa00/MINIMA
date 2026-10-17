# Reviewer demo

The package includes both adversarial Direct Mode behaviour and one finalized Studionet lifecycle. Exact live values and explorer links are in `DEPLOYMENT.md`.

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

### 1. Deployment result

The source was deployed from commit `47203f155a46558eeaca0afca9951fa2778e755b`, finalized at `0x180bC04e85Eb45Fab80354badC12a73ec7a76B66`, then read back and verified byte-identical.

### 2. Create schema

The live `Shipping profile v1` schema contains these fields in this exact order:

```text
0 recipient_name   PERSONAL
1 delivery_address PERSONAL
2 phone_number     PERSONAL
3 date_of_birth    SENSITIVE
4 passport_number  RESTRICTED
```

It was sealed with hash `4a0c898db0dfa9cb746e66cc72e584accc0c9dbf9dc10ccce293fc3ee4631a4c`.

### 3. Create sealed purpose

Live purpose:

> Print the intended recipient name and route one ordinary physical parcel to the declared postal delivery address. The carrier does not send notifications and performs no identity, age, passport, analytics, marketing, or secondary processing.

It binds the recorded requester, a dedicated consumer, and a one-day TTL. It was sealed with hash `cc164c3758360a5ba055d8eb2d8a208e464a0dcb95de1260ca58c8b8aae97d08`.

### 4. Resolve a request

From the authorised requester:

- open the request with a real 32-byte action hash;
- resolve it;
- wait for ACCEPTED and then FINALIZED;
- record the request transaction, result and permit ID.

Finalized result:

```text
recipient_name   NECESSARY
delivery_address NECESSARY
others           NOT_NECESSARY
field_mask       3
```

The ambiguity mask was zero. The exact on-chain result—not an expected result—is recorded in `DEPLOYMENT.md`.

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
