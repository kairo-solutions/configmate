# Stellar Usage Example

This example shows how to use ConfigMate for Stellar network configuration.

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

# Example: Initialize Stellar SDK (if you have the stellar-sdk installed)
# from stellar_sdk import Server
# server = Server(horizon_url)
```