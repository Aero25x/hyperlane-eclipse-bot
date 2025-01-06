import re
import asyncio
import aiohttp
from aiohttp import ClientConnectorError, ClientProxyConnectionError, ClientHttpProxyError



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





def is_ip(string):
    """Check if the string is a valid IP address."""
    pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    if pattern.match(string):
        parts = string.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    return False

def is_port(string):
    """Check if the string is a valid port number."""
    return string.isdigit() and 0 < int(string) <= 65535

async def check_proxy(session, ip, port, username, password):
    """Test if the proxy is working by making an HTTP request asynchronously."""
    proxy_details = f"{ip}:{port}:{username}:{password}"
    proxy_url = f'http://{username}:{password}@{ip}:{port}'
    test_url = 'http://httpbin.org/ip'  # This service returns the requester's IP address

    try:
        async with session.get(test_url, proxy=proxy_url, timeout=5) as response:
            if response.status == 200:
                print(f"{proxy_details} -> WORK")
            else:
                print(f"{proxy_details} -> NOT WORK (Status: {response.status})")
    except (ClientConnectorError, ClientProxyConnectionError, ClientHttpProxyError, asyncio.TimeoutError, aiohttp.ClientError):
        print(f"{proxy_details} -> NOT WORK")

async def main():
    """Main function to read proxies and initiate asynchronous checks."""
    # Read proxy data from 'proxy.txt' file
    try:
        with open("proxy.txt", "r") as f:
            proxy_data = f.read()
    except FileNotFoundError:
        print("The file 'proxy.txt' was not found.")
        return

    # Prepare a list of valid proxies
    proxies = []
    for line in proxy_data.strip().split('\n'):
        elements = line.strip().split(':')
        if len(elements) != 4:
            print(f"Invalid line format: {line}")
            continue

        ip = port = username = password = None
        for elem in elements:
            if is_ip(elem):
                ip = elem
            elif is_port(elem):
                port = elem
            else:
                if username is None:
                    username = elem
                else:
                    password = elem

        if all([ip, port, username, password]):
            proxies.append((ip, port, username, password))
        else:
            print(f"Could not parse proxy details from line: {line}")

    if not proxies:
        print("No valid proxies to check.")
        return

    # Set up an aiohttp session with a connector
    connector = aiohttp.TCPConnector(ssl=False)  # Disable SSL verification if needed
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for proxy in proxies:
            task = asyncio.create_task(check_proxy(session, *proxy))
            tasks.append(task)

        # Optionally, limit the number of concurrent tasks
        # To prevent overwhelming your system or the target server
        # You can use a semaphore for this purpose
        semaphore = asyncio.Semaphore(100)  # Adjust the limit as needed

        async def sem_task(task):
            async with semaphore:
                await task

        # Wrap tasks with semaphore
        sem_tasks = [sem_task(task) for task in tasks]

        # Run all tasks concurrently
        await asyncio.gather(*sem_tasks)

if __name__ == "__main__":

    print("Created for HiddenCode Community")
    print("for wallet generation use Kozel App - https://t.me/hcmarket_bot?start=project_1")
    asyncio.run(main())
