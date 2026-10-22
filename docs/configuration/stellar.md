# Stellar Configuration

`StellarConfig` gives Python applications that interact with Stellar one place
to manage the selected network and its Horizon and Soroban RPC endpoints. It
provides matching defaults for Testnet, Mainnet, and Futurenet, while allowing
each endpoint to be overridden for hosted, local, or otherwise custom
networks.

```python
from configmate import StellarConfig

config = StellarConfig()
config.load_from_env()

network = config.get('stellar.network')
horizon_url = config.get_horizon_url()
soroban_rpc_url = config.get_soroban_rpc_url()
```

By default, the network is `testnet`. Changing `stellar.network` updates both
endpoint defaults together unless you explicitly set a custom URL. This keeps
network selection in application configuration and avoids hard-coding endpoint
URLs across Stellar application code.

## Environment variables

`load_from_env()` reads these variables by default:

| Variable | Purpose |
| --- | --- |
| `STELLAR_NETWORK` | Select `testnet`, `mainnet`, `futurenet`, or a custom network name |
| `STELLAR_HORIZON_URL` | Override the Horizon endpoint |
| `STELLAR_SOROBAN_RPC_URL` | Override the Soroban RPC endpoint |

For example, set `STELLAR_NETWORK=mainnet` to use the Mainnet endpoint defaults,
or set either URL variable to use a custom endpoint.

## Features

The `StellarConfig` class extends `Config` and provides:

- Testnet defaults and matching Horizon and Soroban RPC URLs for Testnet,
  Mainnet, and Futurenet
- Automatic loading from environment variables with the `STELLAR_` prefix
- Helpers to retrieve endpoint URLs and identify the three preset networks
- Support for custom network names and endpoint overrides

`is_known_network()` only identifies whether the configured name is one of the
three presets; custom names are allowed. ConfigMate manages configuration only:
it does not provide Stellar SDK functionality or test endpoint connectivity.

## API Reference

For the full API reference, see the [StellarConfig API](../api/stellar_config.md).