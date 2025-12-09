# Monitor Configuration Package with Key Generator

This package contains:

- INI configuration files for all monitors
- A Python script (`generate_keys.py`) for generating AES and IV keys
- Instructions for generating RSA signature keys

## Key Generation

### AES + IV Keys
Run:

    python generate_keys.py --output keys/

This will generate:
- client_aes.key (32 bytes)
- client_iv.key (16 bytes)
- server_aes.key (32 bytes)
- server_iv.key (16 bytes)
- webserver_aes.key (32 bytes)
- webserver_iv.key (16 bytes)
- crowler_aes.key (32 bytes)
- crowler_iv.key (16 bytes)

### RSA Signature Keys (Webserver)

Run:

    openssl genpkey -algorithm RSA -out webserver_signature.key -pkeyopt rsa_keygen_bits:2048
    openssl rsa -in webserver_signature.key -pubout -out client_signature.pub

Place generated keys inside the `keys/` directory.

## Usage

Each monitor reads its own INI configuration file and uses:

- paths to AES keys
- IV files
- optional RSA signature keys

Ensure the folder structure matches your deployment environment.

