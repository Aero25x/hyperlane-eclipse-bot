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





import os
from IVan.browserController import main as browserControllerMain
import asyncio
import logging
from IVan.logger import logme
import random
import json

from tqdm import tqdm  # Import tqdm for progress bar

logme("""

              Created by @Aero25X

""")


useOnlyLast = 0  # Set to 0 to use all accounts, or set to a number to use only the last n accounts


async def main():
    # for wallet generation use Kozel App - https://t.me/hcmarket_bot?start=project_1
    with open("wallets.json", "r") as f:
        wallets = json.load(f)
    # for wallet generation use Kozel App - https://t.me/hcmarket_bot?start=project_1
    with open("wallets_evm.json", "r") as f:
        wallets_evm = json.load(f)


    if len(wallets) != len(wallets_evm):
        print(f"Incorrect wallets amount entered: SOLANA: {len(wallets)} != EVM {len(wallets_evm)}")
        return
    else:
        # wallets = [wallet for i, wallet in enumerate(wallets)]
        for i, wallet in enumerate(wallets_evm):
            wallets[i]['evm_address'] = wallet['address']
            wallets[i]['evm_privateKey'] = wallet['privateKey']

    with open("schema.json", "r") as f:
        schema = json.load(f)

    random.shuffle(wallets)

    for i, wallet in enumerate(wallets):
        await browserControllerMain(i, wallet, schema)

    logme("All Tasks Finished")



print(r"""

      _    _ _     _     _             _____          _
     | |  | (_)   | |   | |           / ____|        | |
     | |__| |_  __| | __| | ___ _ __ | |     ___   __| | ___
     |  __  | |/ _` |/ _` |/ _ \ '_ \| |    / _ \ / _` |/ _ \
     | |  | | | (_| | (_| |  __/ | | | |___| (_) | (_| |  __/
     |_|  |_|_|\__,_|\__,_|\___|_| |_|\_____\___/ \__,_|\___|


		https://t.me/hidden_coding

for wallet generation use Kozel App - https://t.me/hcmarket_bot?start=project_1

""")





if __name__ == '__main__':
    # Remove any existing log files
    for filename in os.listdir():
        if filename.startswith("web.telegram"):
            os.remove(filename)


    # Define the loggers to disable
    loggers_to_disable = [
        "websockets.client",
        "nodriver.core.config",
        "nodriver.core.browser",
        "uc.connection",
        "asyncio",
        "certutil"
    ]

    # Disable logging for each specified logger
    for logger_name in loggers_to_disable:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.CRITICAL)
        logger.propagate = False

    # Optionally, configure the root logger or other loggers as needed
    logging.basicConfig(level=logging.INFO)


    asyncio.run(main())
