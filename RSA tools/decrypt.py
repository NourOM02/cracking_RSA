import argparse
import json

def decrypt(encrypted_message, private_key):
    # unpack the public key
    d, n = private_key

    # decrypt the message
    decrypted_message = [pow(char, d, n) for char in encrypted_message]

    # convert the decrypted message to a string
    message = ''.join([chr(char) for char in decrypted_message])

    return message

# Load public key
try :
    keys = json.load(open('keys.json'))
    private_key = keys['private_key']
except FileNotFoundError:
    print("No keys found. Please generate keys first by running generate_keys.py")

parser = argparse.ArgumentParser(description="A script to decrypt a message using pre-defined keys")

# Load encrypted message
try :
    message_f = json.load(open('message.json'))
    encrypted_message = message_f['encrypted_message']
    # decrypt the message
    message = decrypt(encrypted_message, private_key)
    print(f"Decrypted message: {message}")
    message_f.update({'decrypted_message': message})
except FileNotFoundError:
    print("No message found. Please encrypt a message first by running encrypt.py")



