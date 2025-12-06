export interface VaultConfig {
  dbPath: string;
}

export class Vault {
  private config: VaultConfig;

  constructor(config: VaultConfig) {
    this.config = config;
  }

  // placeholder for libsodium + pglite integration
  async init(): Promise<void> {
    return;
  }
}
