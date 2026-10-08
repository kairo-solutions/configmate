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

    def __init__(self):
        """Initialize Stellar configuration with defaults for network and horizon URL."""
        super().__init__()
        self._horizon_url_explicit = False
        self.set_default('stellar.network', 'testnet', str)
        self.set_default('stellar.horizon_url', self._NETWORK_HORIZON_URLS['testnet'], str)
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
        elif key == 'stellar.network' and not self._horizon_url_explicit:
            default_url = self._NETWORK_HORIZON_URLS['testnet']
            if isinstance(value, str):
                default_url = self._NETWORK_HORIZON_URLS.get(value, default_url)
            super().set('stellar.horizon_url', default_url)
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

    def is_known_network(self) -> bool:
        """Check if the current network is a known network (testnet, mainnet, futurenet).

        Returns:
            True if the network is known, False otherwise.
        """
        network = self.get('stellar.network')
        return network in self._NETWORK_HORIZON_URLS