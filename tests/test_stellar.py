"""
Tests for StellarConfig
"""

import os
from configmate.stellar import StellarConfig


def test_defaults():
    """Test default values."""
    config = StellarConfig()
    assert config.get('stellar.network') == 'testnet'
    assert config.get('stellar.horizon_url') == 'https://horizon-testnet.stellar.org'


def test_get_horizon_url():
    """Test get_horizon_url method."""
    config = StellarConfig()
    # Default horizon URL for testnet
    assert config.get_horizon_url() == 'https://horizon-testnet.stellar.org'

    # Set custom horizon URL
    config.set('stellar.horizon_url', 'https://custom.example')
    assert config.get_horizon_url() == 'https://custom.example'

    # Set network to mainnet, horizon URL should default to mainnet if not set
    config.set('stellar.network', 'mainnet')
    # Note: we didn't set horizon URL, so it should default to mainnet
    # But note: in our implementation, we don't automatically update the horizon URL when network changes.
    # So the horizon URL remains the custom one unless we set it.
    # Actually, in our get_horizon_url method, if the user has set a horizon URL (even if it's from a previous network),
    # we return it. So we need to reset the horizon URL to None to test the default.
    config.set('stellar.horizon_url', None)
    assert config.get_horizon_url() == 'https://horizon.stellar.org'


def test_is_known_network():
    """Test is_known_network method."""
    config = StellarConfig()
    # Default is testnet, which is known
    assert config.is_known_network() is True

    # Set to mainnet
    config.set('stellar.network', 'mainnet')
    assert config.is_known_network() is True

    # Set to futurenet
    config.set('stellar.network', 'futurenet')
    assert config.is_known_network() is True

    # Set to unknown network
    config.set('stellar.network', 'unknown')
    assert config.is_known_network() is False


def test_load_from_env():
    """Test loading from environment variables."""
    # Set environment variables
    os.environ['STELLAR_NETWORK'] = 'mainnet'
    os.environ['STELLAR_HORIZON_URL'] = 'https://env.example'

    config = StellarConfig()
    config.load_from_env()

    assert config.get('stellar.network') == 'mainnet'
    assert config.get('stellar.horizon_url') == 'https://env.example'

    # Clean up
    del os.environ['STELLAR_NETWORK']
    del os.environ['STELLAR_HORIZON_URL']


def test_validation():
    """Test validation of network field."""
    config = StellarConfig()
    # The validation currently only checks that it's a string, so any string passes.
    # We'll test that it accepts a string and rejects non-string.
    config.validate('stellar.network', lambda v: isinstance(v, str))
    # This should not raise
    config.set('stellar.network', 'testnet')

    # If we set a non-string, the validation in the Config class will catch it via type hints?
    # Actually, the validation we added in StellarConfig is just for being a string.
    # The type hint is set to str in set_default, so the type check will run.
    # Let's test that setting a non-string fails the type check.
    # We'll use validate_all to see if there's a type mismatch.
    config.set('stellar.network', 123)
    errors = config.validate_all()
    # There should be a type mismatch error
    assert any("Type mismatch for key 'stellar.network'" in err for err in errors)