import assert from "node:assert/strict";
import { test } from "node:test";
import { getStellarEndpoints } from "../.build/stellar-endpoints.js";

test("defaults to Stellar Testnet endpoints", () => {
  assert.deepEqual(getStellarEndpoints(), {
    network: "testnet",
    horizonUrl: "https://horizon-testnet.stellar.org",
    sorobanRpcUrl: "https://soroban-testnet.stellar.org",
  });
});

test("selects matching endpoints for each known network", () => {
  assert.equal(
    getStellarEndpoints("mainnet").sorobanRpcUrl,
    "https://soroban-rpc.stellar.org",
  );
  assert.equal(
    getStellarEndpoints("futurenet").horizonUrl,
    "https://horizon-futurenet.stellar.org",
  );
});

test("allows custom endpoint overrides", () => {
  assert.deepEqual(
    getStellarEndpoints("mainnet", { horizonUrl: "https://stellar.example" }),
    {
      network: "mainnet",
      horizonUrl: "https://stellar.example",
      sorobanRpcUrl: "https://soroban-rpc.stellar.org",
    },
  );
});
