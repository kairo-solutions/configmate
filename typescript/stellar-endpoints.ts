const endpoints = {
  testnet: {
    horizonUrl: "https://horizon-testnet.stellar.org",
    sorobanRpcUrl: "https://soroban-testnet.stellar.org",
  },
  mainnet: {
    horizonUrl: "https://horizon.stellar.org",
    sorobanRpcUrl: "https://soroban-rpc.stellar.org",
  },
  futurenet: {
    horizonUrl: "https://horizon-futurenet.stellar.org",
    sorobanRpcUrl: "https://rpc-futurenet.stellar.org",
  },
} as const;

export type StellarNetwork = keyof typeof endpoints;

export interface StellarEndpointOverrides {
  horizonUrl?: string;
  sorobanRpcUrl?: string;
}

export function getStellarEndpoints(
  network: StellarNetwork = "testnet",
  overrides: StellarEndpointOverrides = {},
) {
  return {
    network,
    horizonUrl: overrides.horizonUrl ?? endpoints[network].horizonUrl,
    sorobanRpcUrl: overrides.sorobanRpcUrl ?? endpoints[network].sorobanRpcUrl,
  };
}
