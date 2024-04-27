import argparse
import utilis

parser = argparse.ArgumentParser(description="Uisng this script you can generates RSA keys,\
                                 encrypt/decrypt messages, and crack small keys.")
parser.add_argument('-a', '--action', type=str, required=True, default="generate_keys",
                    help='Choose the action you want to perform. Options: generate_keys, encrypt,\
                          decrypt, crack')
parser.add_argument('-b', '--bits', type=int, default=32, help='How much bits the key should have.')
parser.add_argument('-f', '--file', type=str, default=False,
                    help='Name of file to save/read keys and/or encrypted/decrypted messages.')
parser.add_argument('-m', '--message', type=str, help='Message to encrypt.')
args = parser.parse_args()

if args.action == "generate_keys":
    print(f"Generating {args.bits}-bit keys...")
    public_key, private_key = utilis.generate_keys(args.bits)
    print(f"Public key: {public_key}")
    print(f"Private key: {private_key}")
    if args.file:
        to_write = {"public_key": public_key, "private_key": private_key}
        utilis.IO(args.file,to_write)

elif args.action == "encrypt":
    assert args.message is not None, "Please provide a message to encrypt."
    print(f"Encrypting message: {args.message}")
    public_key = utilis.IO(args.file, output="public_key")
    encrypted_message = utilis.encrypt(args.message, public_key)
    print(f"Encrypted message: {encrypted_message}")
    if args.file:
        to_write = {"encrypted_message": encrypted_message}
        utilis.IO(args.file, to_write)

elif args.action == "decrypt":
    encrypted_message = utilis.IO(args.file, output="encrypted_message")
    private_key = utilis.IO(args.file, output="private_key")
    decrypted_message = utilis.decrypt(encrypted_message, private_key)
    print(f"Decrypted message: {decrypted_message}")
    if args.file:
        to_write = {"decrypted_message": decrypted_message}
        utilis.IO(args.file, to_write)

elif args.action == "crack":
    assert args.file, "Please provide a file containing the public key."
    public_key = utilis.IO(args.file, output="public_key")
    private_key = utilis.IO(args.file, output="private_key")
    print(f"Cracking private key of the following public key : {public_key}")
    private_key = utilis.shor_algorithm(public_key)
    print(f"Cracked private key: {private_key}")
    print(f"The private key is {private_key}")
    print(f"The cracking operation was {'successful' if private_key == private_key else 'unsuccessful'}.")
    

else:
    print("Invalid action. Please choose between generate_keys, encrypt, decrypt, and crack.")