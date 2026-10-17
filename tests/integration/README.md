# Integration tests

The final integration suite should be created by the finishing agent only after confirming the exact locally installed `genlayer-test`/CLI API on Studionet 61999.

Do not add a fake network test merely to increase test count.

Minimum real integration evidence:

1. deploy `contracts/minima.py` to Studionet 61999;
2. create + seal a four-field schema;
3. create + seal the shipping purpose;
4. open + resolve one request;
5. wait through acceptance and finality;
6. verify the returned permit field mask;
7. prove wrong action hash and wrong consumer fail `is_permit_valid`;
8. revoke purpose/permit and prove the old permit becomes invalid;
9. record transaction hashes and explorer links in `DEPLOYMENT.md`.

The integration test must never target a release-candidate preview network.
