import logging



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




# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Set root logger level to debug to capture all messages

# Create a console handler and set level to info
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(console_formatter)

# Create a file handler and set level to debug
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
# Customize the formatter to exclude the log level name
file_formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(file_formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def logme(data, type="info"):
    if type == "info":
        logger.info(data)
    elif type == "error":
        logger.error(f"ERROR: {data}")
    elif type == "warning":
        logger.warning(f"WARNING: {data}")
    elif type == "debug":
        logger.debug(data)
    else:
        logger.info(data)

    # print(data)




