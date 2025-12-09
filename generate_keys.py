import os
import argparse

def generate_key(path, size):
    with open(path, "wb") as f:
        f.write(os.urandom(size))
    print(f"Generated {size}-byte key: {path}")

def main():
    parser = argparse.ArgumentParser(description="Generate AES and IV keys for monitor system.")
    parser.add_argument("--output", required=True, help="Directory where keys will be saved.")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    keys = {
        "client_aes.key": 32,
        "client_iv.key": 16,
        "server_aes.key": 32,
        "server_iv.key": 16,
        "webserver_aes.key": 32,
        "webserver_iv.key": 16,
        "crowler_aes.key": 32,
        "crowler_iv.key": 16,
    }

    for filename, size in keys.items():
        generate_key(os.path.join(args.output, filename), size)

    print("Key generation complete.")
    print("For RSA signature keys, run:")
    print("  openssl genpkey -algorithm RSA -out webserver_signature.key -pkeyopt rsa_keygen_bits:2048")
    print("  openssl rsa -in webserver_signature.key -pubout -out client_signature.pub")

if __name__ == "__main__":
    main()
