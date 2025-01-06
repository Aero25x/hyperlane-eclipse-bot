#		    Created by Aero25x
#		      For HiddenCode
#
#		https://t.me/hidden_coding
#
#
#      _    _ _     _     _             _____          _
#     | |  | (_)   | |   | |           / ____|        | |
#     | |__| |_  __| | __| | ___ _ __ | |     ___   __| | ___
#     |  __  | |/ _` |/ _` |/ _ \ '_ \| |    / _ \ / _` |/ _ \
#     | |  | | | (_| | (_| |  __/ | | | |___| (_) | (_| |  __/
#     |_|  |_|_|\__,_|\__,_|\___|_| |_|\_____\___/ \__,_|\___|
#
#
#	For More Software and bots visit Our Market:
#		https://t.me/hcmarket_bot
#
#




import random
import string
import csv

# Define the modulus once for reuse
MODULUS_HEX = "5533627"
MODULUS = int(MODULUS_HEX, 16)  # Converts hexadecimal to integer

def generate_vr(k=0):
    """
    Generates a correct vr value that satisfies vr % MODULUS == 1.

    Parameters:
    - k (int): Multiplier for the modulus.

    Returns:
    - str: Hexadecimal representation of vr without '0x' prefix.
    """
    vr = k * MODULUS + 1
    return hex(vr)[2:].upper()  # Remove '0x' prefix and convert to uppercase

def check_vr(vr_hex):
    """
    Checks if the given vr satisfies vr % MODULUS == 1.

    Parameters:
    - vr_hex (str): Hexadecimal string representation of vr.

    Returns:
    - bool: True if condition is met, False otherwise.
    """
    vr = int(vr_hex, 16)  # Convert hex string back to integer
    return vr % MODULUS == 1

def generate_incorrect_vr(k=0, delta=None):
    """
    Generates an incorrect vr value that does NOT satisfy vr % MODULUS == 1.
    By default, it adds a random delta to the correct vr to ensure incorrectness.

    Parameters:
    - k (int): Multiplier for the modulus.
    - delta (int, optional): The amount to adjust vr to make it incorrect.
      If None, a random delta between 2 and MODULUS-1 is used.

    Returns:
    - str: Hexadecimal representation of incorrect vr without '0x' prefix.
    """
    if delta is None:
        # Choose a random delta that is not 1 to avoid accidentally generating a correct vr
        delta = random.choice([d for d in range(2, MODULUS) if d != 1])
    vr_correct = k * MODULUS + 1
    vr_incorrect = vr_correct + delta
    return hex(vr_incorrect)[2:].upper()  # Remove '0x' prefix and convert to uppercase

def generate_random_key(length=20):
    """
    Generates a random alphanumeric key of specified length.

    Parameters:
    - length (int): Length of the key. Default is 20.

    Returns:
    - str: Randomly generated alphanumeric key.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def main():
    # Define the number of correct and incorrect entries
    num_correct = 50
    num_incorrect = 200

    # List to hold all entries
    entries = []

    # Generate correct vr entries
    for _ in range(num_correct):
        k = random.randint(100, 999)  # Random k between 100 and 999
        vr_hex = generate_vr(k)
        is_correct = check_vr(vr_hex)
        assert is_correct, "Generated vr should satisfy vr % MODULUS == 1"

        name = "Phoenix + Support"
        price = 250
        entry = {
            'name on button': name,
            'data': vr_hex,
            'price': price
        }
        entries.append(entry)

    # Generate incorrect vr entries
    for _ in range(num_incorrect):
        k = random.randint(100, 999)  # Random k between 100 and 999
        vr_incorrect_hex = generate_incorrect_vr(k, 2)
        is_correct = check_vr(vr_incorrect_hex)
        assert not is_correct, "Generated vr should NOT satisfy vr % MODULUS == 1"

        name = "Phoenix"
        price = 180

        entry = {
            'name on button': name,
            'data': vr_incorrect_hex,
            'price': price
        }
        entries.append(entry)

    # Shuffle the entries to mix correct and incorrect ones
    random.shuffle(entries)

    # Define the CSV file name
    csv_file = 'fill_me.csv'

    # Write to CSV
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['name on button', 'data', 'price'])
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry)

    print(f"CSV file '{csv_file}' has been generated with {num_correct + num_incorrect} entries.")

if __name__ == "__main__":
    main()
