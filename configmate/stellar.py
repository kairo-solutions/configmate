"""
Stellar configuration extension for ConfigMate.
"""

from typing import Any

from .config import Config


class StellarConfig(Config):
    """A configuration manager with Stellar-specific defaults and validation."""

    # Default horizon URLs for known networks
    _NETWORK_HORIZON_URLS = {
        'testnet': 'https://horizon-testnet.stellar.org',
        'mainnet': 'https://horizon.stellar.org',
        'futurenet': 'https://horizon-futurenet.stellar.org',
    }
    _NETWORK_SOROBAN_RPC_URLS = {
        'testnet': 'https://soroban-testnet.stellar.org',
        'mainnet': 'https://soroban-rpc.stellar.org',
        'futurenet': 'https://rpc-futurenet.stellar.org',
    }

    def __init__(self):
        """Initialize Stellar configuration with defaults for network and horizon URL."""
        super().__init__()
        self._horizon_url_explicit = False
        self._soroban_rpc_url_explicit = False
        self.set_default('stellar.network', 'testnet', str)
        self.set_default('stellar.horizon_url', self._NETWORK_HORIZON_URLS['testnet'], str)
        self.set_default(
            'stellar.soroban_rpc_url',
            self._NETWORK_SOROBAN_RPC_URLS['testnet'],
            str,
        )
        self.validate('stellar.network', self._validate_network)

    def _validate_network(self, value: str) -> bool:
        """Validate that the network is a string (we allow any string for custom networks).
        In the future, we could restrict to known networks, but we allow flexibility.
        """
        return isinstance(value, str)

    def set(self, key: str, value: Any) -> None:
        """Set a value and keep the default Horizon URL in sync with the network."""
        if key == 'stellar.horizon_url':
            self._horizon_url_explicit = True
        elif key == 'stellar.soroban_rpc_url':
            self._soroban_rpc_url_explicit = True
        elif key == 'stellar.network':
            default_url = self._NETWORK_HORIZON_URLS['testnet']
            default_rpc_url = self._NETWORK_SOROBAN_RPC_URLS['testnet']
            if isinstance(value, str):
                default_url = self._NETWORK_HORIZON_URLS.get(value, default_url)
                default_rpc_url = self._NETWORK_SOROBAN_RPC_URLS.get(value, default_rpc_url)
            if not self._horizon_url_explicit:
                super().set('stellar.horizon_url', default_url)
            if not self._soroban_rpc_url_explicit:
                super().set('stellar.soroban_rpc_url', default_rpc_url)
        super().set(key, value)

    def load_from_env(self, prefix: str = 'STELLAR_', lowercase_keys: bool = True,
                      separator: str = '__') -> None:
        """Load configuration from environment variables with a Stellar prefix.

        Args:
            prefix: The prefix for environment variables (default: 'STELLAR_').
            lowercase_keys: Whether to convert keys to lowercase.
            separator: The separator used in nested keys (default: '__').
        """
        self._load_from_env(
            prefix,
            lowercase_keys,
            separator,
            key_prefix='stellar',
        )

    def get_horizon_url(self) -> str:
        """Get the horizon URL for the current network.

        Returns:
            The horizon URL from configuration, or the default for the network if not set.
        """
        url = self.get('stellar.horizon_url')
        if url:
            return url
        network = self.get('stellar.network')
        return self._NETWORK_HORIZON_URLS.get(network, self._NETWORK_HORIZON_URLS['testnet'])

    def get_soroban_rpc_url(self) -> str:
        """Get the Soroban RPC URL for the current network."""
        url = self.get('stellar.soroban_rpc_url')
        if url:
            return url
        network = self.get('stellar.network')
        return self._NETWORK_SOROBAN_RPC_URLS.get(
            network,
            self._NETWORK_SOROBAN_RPC_URLS['testnet'],
        )

    def is_known_network(self) -> bool:
        """Check if the current network is a known network (testnet, mainnet, futurenet).

        Returns:
            True if the network is known, False otherwise.
        """
        network = self.get('stellar.network')
        return network in self._NETWORK_HORIZON_URLS