# MINIMA threat model

## Assets protected

MINIMA protects the scope of a data-access permit. Its most important invariant is that a requester cannot inflate a consensus result into a larger field mask.

## Threat: requester asks for everything

There is no `requested_fields` argument in the permit path. Consensus evaluates the complete sealed schema. The requester cannot omit inconvenient fields from the classification surface or append fields after consensus.

## Threat: prompt injection through metadata

Schema descriptions, field descriptions and purpose text are data supplied to the LLM. Obvious machine-control phrases are rejected at creation. The prompt also explicitly treats all supplied values as inert data.

This lexical gate is defence in depth, not a proof that natural language can never be adversarial.

## Threat: malicious leader returns a permissive subset

A custom validator independently runs the complete classification and must agree on the exact `NECESSARY` and `AMBIGUOUS` masks.

A malformed, incomplete, duplicate or unknown field list fails closed.

## Threat: ambiguity silently becomes permission

Any ambiguous field prevents permit issuance. MINIMA never treats ambiguity as `NOT_NECESSARY`.

## Threat: purpose substitution

The request pins the exact purpose hash and schema hash before semantic execution. Permit validation can require both hashes again.

## Threat: action substitution

The request and permit commit to a canonical 32-byte action hash. A consumer should reject the permit for any different action hash.

## Threat: consumer substitution

A purpose binds a specific consumer address. Permit validation requires the expected consumer.

## Threat: stale permission

Permits expire. Purpose revocation also makes existing permits invalid at read time. Individual permits can be revoked by the requester or purpose owner.

## Threat: schema mutation

A schema is immutable after sealing. A changed catalogue requires a new schema and therefore a new hash and new purposes.

## Threat: private data leaks on-chain

MINIMA stores no private values. This is a hard architecture boundary. Do not add methods that accept customer records, credentials, medical information, raw documents, secrets, or private database contents.

## Threat: a dishonest schema owner misdescribes a field

MINIMA does not prove that field metadata is truthful. Consumers must trust or independently govern the schema owner. The contract only guarantees that the minimisation decision is made over the exact sealed descriptions.

## Threat: legal/privacy overclaim

A field being `NECESSARY` under the declared purpose is not a legal determination. MINIMA does not replace consent, lawful-basis analysis, contractual rights, regulatory obligations or organisational policy.

## Threat: external vault ignores MINIMA

MINIMA cannot force a non-integrating off-chain database to honour a permit. Enforcement exists only where a consumer deliberately validates the permit before release.
