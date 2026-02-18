import string
import secrets


def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    char_pool = ""
    password = []

    if use_upper:
        char_pool += string.ascii_uppercase
        password.append(secrets.choice(string.ascii_uppercase))

    if use_lower:
        char_pool += string.ascii_lowercase
        password.append(secrets.choice(string.ascii_lowercase))

    if use_digits:
        char_pool += string.digits
        password.append(secrets.choice(string.digits))

    if use_symbols:
        char_pool += string.punctuation
        password.append(secrets.choice(string.punctuation))

    if not char_pool:
        raise ValueError("No character types selected.")

    # Fill remaining length
    for _ in range(length - len(password)):
        password.append(secrets.choice(char_pool))

    # Shuffle securely
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)


def main():
    print("=== Secure Password Generator ===")

    try:
        length = int(input("Enter desired password length: "))
        if length < 4:
            print("Password length should be at least 4 for good security.")
            return

        print("\nInclude in password?")
        upper = input("Uppercase letters (A-Z)? (y/n): ").lower() == "y"
        lower = input("Lowercase letters (a-z)? (y/n): ").lower() == "y"
        digits = input("Digits (0-9)? (y/n): ").lower() == "y"
        symbols = input("Symbols (!@#...)? (y/n): ").lower() == "y"

        password = generate_password(length, upper, lower, digits, symbols)

        print("\nGenerated Password:")
        print(password)

    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
