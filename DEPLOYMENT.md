# Deployment evidence

**Status: FINALIZED ON STUDIONET (chain ID 61999).**

```text
Network: Studionet
Chain ID: 61999
RPC: https://studio.genlayer.com/api
Explorer: https://explorer-studio.genlayer.com
CLI: genlayer 0.39.1 (repository-local)

Intended repository: https://github.com/lolaaa00/minima
Deployment commit: 47203f155a46558eeaca0afca9951fa2778e755b
Contract source SHA-256: 2209e8b245326a416e8818a740e405a6ec8a3bc5b8d360373976b2f6f5009b73
Contract address: 0x180bC04e85Eb45Fab80354badC12a73ec7a76B66
Deployment transaction: 0xce7df652b2c0a063bb74204efb85c6bed960b7ac9e6bb76e3f1fb563c257b29e
Deployment final status: FINALIZED
Deployer/requester: 0xE36AEeC44999a1C347782b4459BEdd98329B9147
```

[Deployment explorer record](https://explorer-studio.genlayer.com/tx/0xce7df652b2c0a063bb74204efb85c6bed960b7ac9e6bb76e3f1fb563c257b29e)

The deployed source was read back from Studionet and compared byte-for-byte with `contracts/minima.py`: both were 37,341 bytes and both produced the SHA-256 above.

## Canonical lifecycle

All transactions below were checked with the pinned CLI and reported `FINALIZED`.

### Schema 1 — Shipping profile v1

- [Create schema](https://explorer-studio.genlayer.com/tx/0x3178fc8e2ea9f3b2b13c2a4f0d3f31952032aeafe0311eaeaed8f796a7b27975): `0x3178fc8e2ea9f3b2b13c2a4f0d3f31952032aeafe0311eaeaed8f796a7b27975`
- [Add `recipient_name`](https://explorer-studio.genlayer.com/tx/0x77bbb23de61bad4c4f4505ee933465a60c180839fbc29738f5db6ef63b28bd34): `0x77bbb23de61bad4c4f4505ee933465a60c180839fbc29738f5db6ef63b28bd34`
- [Add `delivery_address`](https://explorer-studio.genlayer.com/tx/0xb5857f0e02e898e19e202cf28b83b26f59e96cff426fb37adef88e853c3b1988): `0xb5857f0e02e898e19e202cf28b83b26f59e96cff426fb37adef88e853c3b1988`
- [Add `phone_number`](https://explorer-studio.genlayer.com/tx/0x371338d237d9e155fdff73e70c381cc0672e24bd32a947f726d9e76703c34a49): `0x371338d237d9e155fdff73e70c381cc0672e24bd32a947f726d9e76703c34a49`
- [Add `date_of_birth`](https://explorer-studio.genlayer.com/tx/0xd00a50679ef44d64779f43a81be0528d9a52dc35c5c404b0909fbbb052e1af60): `0xd00a50679ef44d64779f43a81be0528d9a52dc35c5c404b0909fbbb052e1af60`
- [Add `passport_number`](https://explorer-studio.genlayer.com/tx/0x55d8ebec5588c1ba8b919410e990ece17e1a8df924df3d0b74fdf66584d632bd): `0x55d8ebec5588c1ba8b919410e990ece17e1a8df924df3d0b74fdf66584d632bd`
- [Seal schema](https://explorer-studio.genlayer.com/tx/0x664e8dc31773ff09ad0fbd5f8fc0504b7cdbcfdf2ea4ef9dfee59cf47831ce2a): `0x664e8dc31773ff09ad0fbd5f8fc0504b7cdbcfdf2ea4ef9dfee59cf47831ce2a`
- Schema hash: `4a0c898db0dfa9cb746e66cc72e584accc0c9dbf9dc10ccce293fc3ee4631a4c`

The sealed field order is `recipient_name`, `delivery_address`, `phone_number`, `date_of_birth`, `passport_number` (field IDs 1–5; mask bit positions 0–4).

### Purpose 1 — Fulfil one physical delivery

- Purpose text: “Print the intended recipient name and route one ordinary physical parcel to the declared postal delivery address. The carrier does not send notifications and performs no identity, age, passport, analytics, marketing, or secondary processing.”
- Authorized requester: `0xE36AEeC44999a1C347782b4459BEdd98329B9147`
- Consumer: `0xDf4BD302Ce78B36C987aC34ce6B2592491984646`
- TTL: 86,400 seconds
- [Create purpose](https://explorer-studio.genlayer.com/tx/0x3d94cb91d1c470079f6a392b85055f7fe95c3b04ddb954f83ecd54511c0098f5): `0x3d94cb91d1c470079f6a392b85055f7fe95c3b04ddb954f83ecd54511c0098f5`
- [Seal purpose](https://explorer-studio.genlayer.com/tx/0x18b3ba5b465ddeb64babf5bbf0a86412117dcfa1177c529a34ff8a806b4aba15): `0x18b3ba5b465ddeb64babf5bbf0a86412117dcfa1177c529a34ff8a806b4aba15`
- Purpose hash: `cc164c3758360a5ba055d8eb2d8a208e464a0dcb95de1260ca58c8b8aae97d08`

### Request 1 and permit 1

- Action hash: `dacd8ef08416c7cbd78102d94512701290996834154013f9263ce8907d754fa6`
- [Open request](https://explorer-studio.genlayer.com/tx/0x7588ab9143d97c03a9a979b4b8418da9501aece05b16c755ab55cdc4d7e0af25): `0x7588ab9143d97c03a9a979b4b8418da9501aece05b16c755ab55cdc4d7e0af25`
- [Resolve request](https://explorer-studio.genlayer.com/tx/0xb251a52d5c77d44a21bdb9e2d84fcf27ec0f96bee4bfcc53b84b930a2f92ce00): `0xb251a52d5c77d44a21bdb9e2d84fcf27ec0f96bee4bfcc53b84b930a2f92ce00`
- Necessary mask: `3` (`0b00011`): `recipient_name`, `delivery_address`
- Not-necessary mask: `28` (`0b11100`): `phone_number`, `date_of_birth`, `passport_number`
- Ambiguous mask: `0`
- Decision hash: `d50d2ef383f23721b7ac36d0e4c0c6af24a09ebe853167883e887e20fcf8488b`
- Permit field mask: `3`, exactly equal to the consensus-derived necessary mask
- Issued: `2026-10-17T10:16:03.842369+00:00`; expiry epoch: `1792318563`

The correct schema hash, purpose hash, action hash, and consumer returned `true`. Substituting the consumer, action hash, schema hash, or purpose hash independently returned `false`.

### Revocation proof

- [Revoke purpose](https://explorer-studio.genlayer.com/tx/0x2413ab6804ec573e3635a30bcfbeff03805a7a924f2be05c4fda9ecf8c39a4ca): `0x2413ab6804ec573e3635a30bcfbeff03805a7a924f2be05c4fda9ecf8c39a4ca`
- The identical permit validation that was `true` before revocation returned `false` afterward.
- The historical permit remains inspectable; its computed `valid` field is now `false`.

## Evidence boundaries

- Expiry was not awaited live for 24 hours. Deterministic expiry is covered in Direct Mode tests; no live-expiry claim is made.
- Unauthorized-requester rejection is covered in Direct Mode tests; no deliberately reverted live transaction was submitted.
- The intended GitHub repository has not been created or connected in this folder, so no GitHub URL availability, push, or CI run is claimed.
