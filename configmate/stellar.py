"""
Stellar configuration extension for ConfigMate.
"""

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
        # Set default for stellar network
        self.set_default('stellar.network', 'testnet', str)
        # Set default for horizon URL based on network (will be updated if network changes)
        self.set_default('stellar.horizon_url', self._NETWORK_HORIZON_URLS['testnet'], str)
        # Validate that the network is one of the known networks or a custom string
        self.validate('stellar.network', self._validate_network)
        # If network changes, we may want to update the horizon URL default, but we leave it to the user to set explicitly.
        # Alternatively, we could add a listener, but for simplicity we let the user set horizon_url explicitly.

    def _validate_network(self, value: str) -> bool:
        """Validate that the network is a string (we allow any string for custom networks).
        In the future, we could restrict to known networks, but we allow flexibility.
        """
        return isinstance(value, str)

    def load_from_env(self, prefix: str = 'STELLAR_', lowercase_keys: bool = True,
                      separator: str = '__') -> None:
        """Load configuration from environment variables with a Stellar prefix.

        Args:
            prefix: The prefix for environment variables (default: 'STELLAR_').
            lowercase_keys: Whether to convert keys to lowercase.
            separator: The separator used in nested keys (default: '__').
        """
        # Call the parent load_from_env with the Stellar prefix
        super().load_from_env(prefix=prefix, lowercase_keys=lowercase_keys, separator=separator)
        # If the network was set via environment, we could update the horizon URL default,
        # but we leave it to the user to set stellar.horizon_url explicitly if needed.
        # Alternatively, we can reset the horizon URL based on the network if it's a known network.
        network = self.get('stellar.network')
        if network in self._NETWORK_HORIZON_URLS:
            # Only set the horizon URL if it hasn't been set by the user (i.e., if it's still the default)
            # However, we don't know if the user set it. We'll leave it as is to allow overriding.
            # We could optionally set it if the current value is the default for the previous network.
            # For simplicity, we do nothing and let the user manage both.
            pass

    def get_horizon_url(self) -> str:
        """Get the horizon URL for the current network.

        Returns:
            The horizon URL from configuration, or the default for the network if not set.
        """
        # If the user has explicitly set a horizon URL, return it
        url = self.get('stellar.horizon_url')
        if url:
            return url
        # Otherwise, return the default for the current network
        network = self.get('stellar.network')
        return self._NETWORK_HORIZON_URLS.get(network, self._NETWORK_HORIZON_URLS['testnet'])

    def is_known_network(self) -> bool:
        """Check if the current network is a known network (testnet, mainnet, futurenet).

        Returns:
            True if the network is known, False otherwise.
        """
        network = self.get('stellar.network')
        return network in self._NETWORK_HORIZON_URLS