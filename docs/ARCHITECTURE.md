# MINIMA architecture

## Primitive boundary

MINIMA answers exactly one semantic question:

> For this sealed purpose and this sealed field catalogue, which declared fields are strictly necessary?

It deliberately does not fetch or store the values of those fields.

## Definition immutability

A schema hash commits to the schema name, description, ordered field catalogue, field descriptions, positions, and sensitivity labels.

A purpose hash commits to:

- the exact sealed schema hash;
- purpose label and purpose text;
- authorised requester;
- consumer;
- permit TTL.

An access request pins both hashes plus an exact 32-byte action hash before consensus runs.

## Field bitmask

A schema supports at most 24 fields. Position `i` corresponds to bit `1 << i`.

Consensus produces:

- `necessary_mask`;
- `ambiguous_mask`.

The contract derives:

```text
not_necessary_mask = universe & ~(necessary_mask | ambiguous_mask)
```

If `ambiguous_mask != 0`, no permit can be issued.

If ambiguity is zero:

```text
permit.field_mask = necessary_mask
```

No caller-controlled mask participates in that assignment.

## Why only NECESSARY and AMBIGUOUS are consensus-critical

The economic/security distinction is inclusion versus uncertainty:

- `NECESSARY` means the field may appear in the permit.
- `AMBIGUOUS` means the entire request fails closed.
- every remaining field is excluded.

Requiring validators to distinguish `convenient` from `unrelated` would create disagreement over diagnostics without changing the permit. MINIMA therefore uses only one excluded category, `NOT_NECESSARY`.

## Permit binding

A permit is bound to:

```text
request_id
requester
consumer
schema_id
purpose_id
schema_hash
purpose_hash
action_hash
field_mask
expiry
decision_hash
```

An integrating consumer should require all expected hashes and its own consumer address when calling `is_permit_valid`.

## Revocation

The schema itself is immutable once sealed.

A purpose owner may revoke a purpose. `is_permit_valid` checks the current purpose status, so revocation invalidates outstanding permits immediately without editing their historical receipt.

The requester or purpose owner may also revoke an individual permit.

## Private-data boundary

The contract must never be extended to persist the private values described by its schema.

The safe architecture is:

```text
MINIMA                         external / consumer vault
public schema metadata  --->  maps field IDs to actual protected columns
permit field mask       --->  enforces which columns may be read
```

The consumer remains responsible for authentication, field-level release, replay protection, auditing, encryption and jurisdiction-specific obligations.
