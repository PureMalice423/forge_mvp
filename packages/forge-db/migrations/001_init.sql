-- Initial FORGE schema placeholder
CREATE TABLE IF NOT EXISTS vault_items (
  id TEXT PRIMARY KEY,
  ciphertext BYTEA NOT NULL,
  blind_index BYTEA
);
