# Can Quantum computers break RSA encryption ?
----------------------------------------------

I created this repository to answer my curiosity after watching Vertitasium's video [How Quantum Computers Break The Internet... Starting Now](https://www.youtube.com/watch?v=-UrdExQW0cs). It contains tools to generate RSA keys, encrypt/decrypt messages and "break" keys. Obviously, breaking keys only works for small ones, otherwise we are truly in danger. For this purpose, I implemented Shor's algorithm which is not the best algorithm in the context of our laptops, but in terms of quantum computing, the encryption will break once a capable quantum computer is built. This repository is for educational purposes, if you want to understand how public and private keys are generated using RSA, how to encrypt/decrypt messages or how our keys may be broken one day 🫠

If you are more interested about the topic you can refer to this [medium article]()

## How to use
First you need to clone the repository or download the source code. Refer to `requirements.txt` for dependencies.

This a command line tool, that contains 4 functions that you can choose from using the action argument :

### 1. Generate keys

Use this function to generate public and private keys. It is possible to specify the number of bits of the generated keys and if you want to save them to a *json* file. (Note that saving them to a file is necessary to use the other functions.)

Command :

```bash
python main.py -a generate_keys -b number_of_bits -f name_of_file
```

Example (without saving to a file) :

```bash
python main.py -a generate_keys -b 1024
```

Example (saving to a file) :

```bash
python main.py -a generate_keys -b 1024 -f tmp.json
```

### 2. Encrypt message
After the generation of a public and private key, use this function to encrypt a message (string). It reads keys from the *json* file specified in the command. The output is a list of encrypted characters that is automatically appended to the same *json* file.

Command :

```bash
python main.py -a encrypt -m message_to_encrypt -f keys_file
```

Example :

```bash
python main.py -a encrypt -m "cracking RSA" -f tmp.json
```

### 3. Decrypt message
Once we have an encrypted message we can decrypt it using this function. Note that we need to specify the *json* file that contains the private key and message.

Command :

```bash
python main.py -a decrypt -f name_of_file
```

Example :

```bash
python main.py -a decrypt -f tmp.json
```

### 4. Breaking keys
By specifying **crack** as the action to use with the script, the script will return the private key for the public key that is contained in the *json* file. Note that the time needed starts to gets annoying starting from 32 bits.

Command :

```bash
python main.py -a crack -f name_of_file
```

Example :

```bash
python main.py -a crack -f tmp.json
```

## Feel Free to contribute
In the open source community contributing is the fuel ⚡⚡ Feel free to give me your suggestion by opening issues or by pull requets !

I searched everywhere how can I convert public and private keys from (e,n) and (d,n) respectively to the format we get when we use ssh-keygen in the terminal. If you happen to have an idea, I'll be glad to hear from you 😊