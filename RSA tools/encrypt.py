import argparse
import json

def encrypt(message, public_key):
    # unpack the public key
    e, n = public_key

    # convert the message to a list of integers
    message = [ord(char) for char in message]

    # encrypt the message
    encrypted_message = [pow(char, e, n) for char in message]

    return encrypted_message

# Load public key
try :
    keys = json.load(open('keys.json'))
    public_key = keys['public_key']
except FileNotFoundError:
    print("No keys found. Please generate keys first by running generate_keys.py")

parser = argparse.ArgumentParser(description="A script to encrypt a message using pre-defined keys")

# add the arguments
parser.add_argument('--message', type=str, default="Hello world !", help='message to encrypt')

# parse the arguments
args = parser.parse_args()

# encrypt the message
encrypted_message = encrypt(args.message, public_key)

print(f"Encrypted message: {encrypted_message}")

# Save the encrypted message to a file
with open('message.json', 'w') as f:
    json.dump({'message': args.message, 'encrypted_message': encrypted_message}, f)