# Stellar Configuration

ConfigMate includes optional Stellar-specific configuration loading for applications that interact with the Stellar network.

```python
from configmate import StellarConfig

# Create a Stellar configuration instance
stellar_config = StellarConfig()

# Load from environment variables with STELLAR_ prefix
# e.g., STELLAR_NETWORK=mainnet STELLAR_HORIZON_URL=https://custom.horizon.example
stellar_config.load_from_env()

# Get the horizon URL for the current network
horizon_url = stellar_config.get_horizon_url()

# Check if using a known network
if stellar_config.is_known_network():
    print(f"Using known network: {stellar_config.get('stellar.network')}")
else:
    print(f"Using custom network: {stellar_config.get('stellar.network')}")

# Access other configuration values as usual
network = stellar_config.get('stellar.network')
```

## Features

The `StellarConfig` class extends `Config` and provides:

- Defaults for `stellar.network` (testnet) and `stellar.horizon_url` (based on network)
- Automatic loading from environment variables with `STELLAR_` prefix
- Validation for the network field
- Helper methods like `get_horizon_url()` and `is_known_network()`

## API Reference

For the full API reference, see the [StellarConfig API](../api/stellar_config.md).