import random
import string

def encode_word(word, rng):
    """
    Encodes a single word:
    - If word length >= 3: moves first letter to end, adds 3 random letters at start and end.
    - If word length < 3: reverses the word.
    """
    if len(word) >= 3:
        first = word[0]
        rest = word[1:] + first
        rand_start = ''.join(rng.choices(string.ascii_letters, k=3))
        rand_end = ''.join(rng.choices(string.ascii_letters, k=3))
        return f"{rand_start}{rest}{rand_end}"
    else:
        return word[::-1]

def decode_word(word, rng):
    """
    Decodes a single word:
    - If word length < 3: reverses the word.
    - If word length >= 7: removes 3 random letters from start and end, moves last letter to front.
    - Otherwise, returns word as is.
    """
    if len(word) < 3:
        return word[::-1]
    elif len(word) >= 7:
        core = word[3:-3]
        if core:
            last = core[-1]
            rest = core[:-1]
            return last + rest
        else:
            return ""
    else:
        return word

def encode_message(message, key):
    """
    Encodes a message using a secret key.
    """
    rng = random.Random(key)
    return ' '.join(encode_word(w, rng) for w in message.split())

def decode_message(message, key):
    """
    Decodes a message using a secret key.
    """
    rng = random.Random(key)
    return ' '.join(decode_word(w, rng) for w in message.split())

def get_key(stored_key):
    """
    Handles key input and verification. Allows up to 3 attempts.
    Key must be numeric.
    Returns the key if correct, or None if too many failed attempts.
    """
    attempts = 0
    while attempts < 3:
        key = input("Enter your secret key (numbers only): ").strip()
        if not key.isdigit():
            print("Key must be numbers only.")
            attempts += 1
            continue
        if stored_key is None:
            return key  # First time, set the key
        elif key == stored_key:
            return key  # Correct key
        else:
            print("Incorrect key. Try again.")
            attempts += 1
    print("Too many incorrect attempts. Exiting.")
    return None

def main():
    stored_key = None
    while True:
        print("\nSelect action:")
        print("0: Decode")
        print("1: Encode")
        print("q: Quit")
        action = input("Enter 0, 1 or q: ").strip()
        if action == 'q':
            print("Goodbye!")
            break

        msg = input("Enter the message: ")

        # Key input and verification
        key = get_key(stored_key)
        if key is None:
            break
        if stored_key is None:
            stored_key = key  # Set the key on first use

        if action == '1':
            encoded = encode_message(msg, stored_key)
            print("Encoded message:", encoded)
        elif action == '0':
            decoded = decode_message(msg, stored_key)
            print("Decoded message:", decoded)
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()
