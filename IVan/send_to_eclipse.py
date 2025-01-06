import random
from web3 import Web3
import base58
import os

def get_data_for_gaszip(solana_address):
    """
    Generates the input data for the transaction by processing the Solana address.

    Args:
        solana_address (str): The Solana address in Base58 format.

    Returns:
        str: Hexadecimal string prefixed with '0x'.
    """
    # Decode the Solana address from Base58 to bytes
    decoded_bytes = base58.b58decode(solana_address)

    # Convert bytes to hexadecimal string
    hex_address = decoded_bytes.hex()

    # Define prefix and suffix
    prefix = "03"
    suffix = "0148"

    # Combine prefix, hex address, and suffix
    full_hex = prefix + hex_address + suffix

    # Format as a hexadecimal string with '0x' prefix
    full_hex_formatted = f"0x{full_hex}"

    print(f"Full hex data for gasZip: {full_hex_formatted}")

    return full_hex_formatted

def send_native_from_base_to_elcipse(private_key, amount_eth, solana_address,
                                    to_address="0x391E7C679d29bD940d63be94AD22A25d25b5A604",
                                    gas_limit=21726,
                                    max_priority_fee_gwei=0.0001,
                                    max_fee_gwei=0.005428706,
                                    provider_url="https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"):
    """
    Sends an Ethereum transaction with custom input data.

    Args:
        private_key (str): The sender's private key.
        amount_eth (float): The amount of ETH to send.
        solana_address (str): The Solana address to encode in the input data.
        to_address (str): The recipient's Ethereum address.
        gas_limit (int): Gas limit for the transaction.
        max_priority_fee_gwei (float): Max priority fee in Gwei.
        max_fee_gwei (float): Max fee per gas in Gwei.
        provider_url (str): URL of the Ethereum node provider.

    Returns:
        str: Transaction hash.
    """
    # Initialize Web3
    w3 = Web3(Web3.HTTPProvider(provider_url))

    if not w3.is_connected():
        raise ConnectionError("Failed to connect to the Ethereum node.")

    # Derive account from private key
    account = w3.eth.account.from_key(private_key)
    from_address = account.address
    print(f"Sender Address: {from_address}")

    # Get nonce
    nonce = w3.eth.get_transaction_count(from_address)
    print(f"Nonce: {nonce}")

    # Get the input data
    input_data = get_data_for_gaszip(solana_address)

    # Convert ETH amount to Wei
    value = w3.to_wei(amount_eth, 'ether')
    print(f"Value (Wei): {value}")

    # Define gas fees
    max_priority_fee = w3.to_wei(max_priority_fee_gwei, 'gwei')
    max_fee = w3.to_wei(max_fee_gwei, 'gwei')
    print(f"Max Priority Fee (Wei): {max_priority_fee}")
    print(f"Max Fee (Wei): {max_fee}")

    # Build the transaction dictionary
    tx = {
        'nonce': nonce,
        'to': to_address,
        'value': value,
        'gas': gas_limit,
        'maxPriorityFeePerGas': max_priority_fee,
        'maxFeePerGas': max_fee,
        'data': input_data,
        'chainId': 8453,  # Mainnet; change if using a different network
        'type': 2,  # Optional: Explicitly setting transaction type as EIP-1559
    }

    # Estimate gas (optional, since we're setting gas manually)
    # estimated_gas = w3.eth.estimate_gas(tx)
    # tx['gas'] = estimated_gas

    print("Transaction details:")
    for key, value in tx.items():
        print(f"  {key}: {value}")

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Transaction sent with hash: {tx_hash.hex()}")

    return tx_hash.hex()


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



# Example usage
if __name__ == "__main__":

    print("""



      _    _ _     _     _             _____          _
     | |  | (_)   | |   | |           / ____|        | |
     | |__| |_  __| | __| | ___ _ __ | |     ___   __| | ___
     |  __  | |/ _` |/ _` |/ _ \ '_ \| |    / _ \ / _` |/ _ \\
     | |  | | | (_| | (_| |  __/ | | | |___| (_) | (_| |  __/
     |_|  |_|_|\__,_|\__,_|\___|_| |_|\_____\___/ \__,_|\___|

                GasZip to Eclipse by Aero25x
                 https://t.me/hidden_coding


        """)


    # Replace these values with your actual data
    PRIVATE_KEY = os.getenv('PRIVATE_KEY')  # It's safer to load from environment variables
    SOLANA_ADDRESS = "YourSolanaAddressHere"  # Replace with the actual Solana address
    AMOUNT_ETH = round(random.uniform(0.0014, 0.0017999999999999), 16)   # Amount to send in ETH

    if not PRIVATE_KEY or not SOLANA_ADDRESS:
        print("Please set the PRIVATE_KEY and SOLANA_ADDRESS variables.")
    else:
        try:
            tx_hash = send_native_from_base_to_elcipse(
                private_key=PRIVATE_KEY,
                amount_eth=AMOUNT_ETH,
                solana_address=SOLANA_ADDRESS,
                provider_url="https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"  # UPDATE TO BASE RPC
            )
            print(f"Transaction successful with hash: {tx_hash}")
        except Exception as e:
            print(f"An error occurred: {e}")
