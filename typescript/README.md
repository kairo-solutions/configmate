# ConfigMate Stellar endpoints for TypeScript

This small companion module provides typed Horizon and Soroban RPC defaults for
Stellar Testnet, Mainnet, and Futurenet. It complements the primary Python
ConfigMate library; it does not load environment variables or replace the
Stellar TypeScript SDK. It is currently source in this repository and has not
been published to npm.

```ts
import { getStellarEndpoints } from "./.build/stellar-endpoints.js";

const { horizonUrl, sorobanRpcUrl } = getStellarEndpoints("mainnet");
```

Pass endpoint overrides when using a custom provider:

```ts
const endpoints = getStellarEndpoints("testnet", {
  horizonUrl: process.env.STELLAR_HORIZON_URL,
});
```

Build the module and run its tests with `npm ci && npm test` from this
directory. The generated `.build/` directory is ignored by Git.
