# Stellar SDK Usage Example

ConfigMate keeps network and endpoint settings in one place. The Stellar
Python SDK provides clients that communicate with Horizon and Soroban RPC.
Install the SDK separately with `pip install stellar-sdk`; it is not a required
ConfigMate dependency. The Stellar Python SDK currently requires Python 3.10
or newer.

```python
from configmate import StellarConfig
from stellar_sdk import Server, SorobanServer

config = StellarConfig()
config.load_from_env()

horizon = Server(config.get_horizon_url())
soroban = SorobanServer(config.get_soroban_rpc_url())
```

The constructors create clients; requests happen when you call SDK methods. For
example, `horizon.root().call()` fetches Horizon's root resource and
`soroban.get_health()` checks the configured Soroban RPC endpoint. These calls
require network access. Keep Testnet and Mainnet credentials and operational
policies separate in your application.

See the [Stellar Python SDK documentation](https://stellar-sdk.readthedocs.io/)
for client APIs and transaction guidance.
