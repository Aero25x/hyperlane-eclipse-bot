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
import json
import re
import logging

def generate_random_user_agent():
    VER = None
    """
    Generates a random desktop user agent string based on real-world distributions:
    - 75% Windows
    - 10% Linux (Ubuntu)
    - 15% Mac

    Returns:
        tuple: A random, realistic desktop user agent string and its version.
    """
    systems = ['windows', 'ubuntu', 'mac']
    system_weights = [75, 10, 15]  # Percentages
    system_type = random.choices(systems, weights=system_weights, k=1)[0]

    browsers_per_system = {
        'windows': ['chrome'],
        'ubuntu': ['chrome'],
        'mac': ['chrome']
    }

    available_browsers = browsers_per_system[system_type]

    browser_weights = {
        'chrome': 50,
        'firefox': 30,
        'opera': 15,
        'safari': 5  # Only for Mac
    }

    selected_browser = random.choices(
        available_browsers,
        weights=[browser_weights[b] for b in available_browsers],
        k=1
    )[0]

    browser_versions = {
        'chrome': list(range(125, 131)),  # Chrome versions 110 to 126
        'firefox': list(range(90, 100)),  # Firefox versions 90 to 99
        'opera': list(range(80, 97)),     # Opera versions 80 to 96
        'safari': ['605.1.15', '537.36']   # Safari uses specific WebKit versions
    }

    if selected_browser in ['chrome', 'firefox', 'opera']:
        major_version = random.choice(browser_versions[selected_browser])
        if selected_browser in ['chrome', 'opera']:
            minor_version = random.randint(0, 9)
            build_version = random.randint(1000, 9999)
            patch_version = random.randint(0, 99)

            VER = major_version

            version = f"{major_version}.{minor_version}.{build_version}.{patch_version}"

        elif selected_browser == 'firefox':
            VER = random.choice(browser_versions['firefox'])
            version = f"{VER}.0"
    elif selected_browser == 'safari':
        VER = browser_versions['safari']
        version = random.choice(browser_versions['safari'])

    if system_type == 'windows':
        windows_versions = ['10.0', '11.0']
        windows_version = random.choice(windows_versions)
        architecture = random.choice(['Win64; x64', 'WOW64'])
        if selected_browser == 'chrome':
            user_agent = (f"Mozilla/5.0 (Windows NT {windows_version}; {architecture}) "
                          f"AppleWebKit/537.36 (KHTML, like Gecko) "
                          f"Chrome/{version} Safari/537.36")
        elif selected_browser == 'firefox':
            user_agent = (f"Mozilla/5.0 (Windows NT {windows_version}; {architecture}; rv:{version}) "
                          f"Gecko/20100101 Firefox/{version}")
        elif selected_browser == 'opera':
            user_agent = (f"Mozilla/5.0 (Windows NT {windows_version}; {architecture}) "
                          f"AppleWebKit/537.36 (KHTML, like Gecko) "
                          f"Chrome/{random.choice(browser_versions['chrome'])}.0.{random.randint(1000,9999)}.0 "
                          f"Opera/{version} Safari/537.36")

    elif system_type == 'ubuntu':
        ubuntu_versions = ['20.04', '22.04', '18.04']
        ubuntu_version = random.choice(ubuntu_versions)
        if selected_browser == 'chrome':
            user_agent = (f"Mozilla/5.0 (X11; Ubuntu; Linux x86_64) "
                          f"AppleWebKit/537.36 (KHTML, like Gecko) "
                          f"Chrome/{version} Safari/537.36")
        elif selected_browser == 'firefox':
            user_agent = (f"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:{version}) "
                          f"Gecko/20100101 Firefox/{version}")
        elif selected_browser == 'opera':
            user_agent = (f"Mozilla/5.0 (X11; Ubuntu; Linux x86_64) "
                          f"AppleWebKit/537.36 (KHTML, like Gecko) "
                          f"Chrome/{random.choice(browser_versions['chrome'])}.0.{random.randint(1000,9999)}.0 "
                          f"Opera/{version} Safari/537.36")

    elif system_type == 'mac':
        mac_versions = ['10_15_7', '11_6', '12_6', '13_3']  # Catalina, Big Sur, Monterey, Ventura
        mac_version = random.choice(mac_versions)
        cpu_arch = random.choice(['Intel Mac OS X', 'Apple Silicon Mac OS X'])
        if selected_browser == 'chrome':
            user_agent = (f"Mozilla/5.0 (Macintosh; {cpu_arch} {mac_version}) "
                          f"AppleWebKit/537.36 (KHTML, like Gecko) "
                          f"Chrome/{version} Safari/537.36")
        elif selected_browser == 'firefox':
            user_agent = (f"Mozilla/5.0 (Macintosh; {cpu_arch} {mac_version}; rv:{version}) "
                          f"Gecko/20100101 Firefox/{version}")
        elif selected_browser == 'opera':
            user_agent = (f"Mozilla/5.0 (Macintosh; {cpu_arch} {mac_version}) "
                          f"AppleWebKit/537.36 (KHTML, like Gecko) "
                          f"Chrome/{random.choice(browser_versions['chrome'])}.0.{random.randint(1000,9999)}.0 "
                          f"Opera/{version} Safari/537.36")
        elif selected_browser == 'safari':
            webkit_version = version.split('.')[0] + '.' + version.split('.')[1]
            user_agent = (f"Mozilla/5.0 (Macintosh; {cpu_arch} {mac_version}) "
                          f"AppleWebKit/{webkit_version} (KHTML, like Gecko) "
                          f"Version/{version} Safari/{version}")
    else:
        user_agent = "Mozilla/5.0"

    return user_agent, str(VER)

def validate_ipv4(ip):
    """
    Validates an IPv4 address.

    Args:
        ip (str): The IP address to validate.

    Returns:
        bool: True if valid IPv4, False otherwise.
    """
    pattern = re.compile(r"""
        ^
        (?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}
        (?:25[0-5]|2[0-4]\d|[01]?\d\d?)
        $
    """, re.VERBOSE)
    return bool(pattern.match(ip))

def parse_proxy(proxy):
    """
    Parses the proxy string and extracts username, password, IP, and port.

    Supports two formats:
    1. username:password@IP:port
    2. IP:port:username:password

    Args:
        proxy (str): The proxy string to parse.

    Returns:
        dict or None: Dictionary with keys 'username', 'password', 'ip', 'port' if valid, else None.
    """
    # Format 1: username:password@IP:port
    if '@' in proxy:
        try:
            credentials, address = proxy.split('@')
            username, password = credentials.split(':')
            ip, port = address.split(':')
            return {
                'username': username,
                'password': password,
                'ip': ip,
                'port': port
            }
        except ValueError:
            return None
    else:
        # Format 2: IP:port:username:password
        parts = proxy.split(':')
        if len(parts) != 4:
            return None
        ip, port, username, password = parts
        return {
            'username': username,
            'password': password,
            'ip': ip,
            'port': port
        }

def validate_proxy(proxy):
    """
    Validates the proxy format. Ensures it has username and password, and is IPv4.

    Supports two formats:
    1. username:password@IP:port
    2. IP:port:username:password

    Args:
        proxy (str): The proxy string to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    parsed = parse_proxy(proxy)
    if not parsed:
        logging.error(f"Proxy '{proxy}' does not match the required formats.")
        return False

    username = parsed['username']
    password = parsed['password']
    ip = parsed['ip']
    port = parsed['port']

    # Validate username and password are non-empty
    if not username or not password:
        logging.error(f"Proxy '{proxy}' is missing username or password.")
        return False

    # Validate IP
    if not validate_ipv4(ip):
        logging.error(f"Proxy '{proxy}' has invalid IPv4 address: {ip}.")
        return False

    # Validate port is a number between 1 and 65535
    if not port.isdigit() or not (1 <= int(port) <= 65535):
        logging.error(f"Proxy '{proxy}' has invalid port: {port}.")
        return False

    return True

def normalize_proxy(proxy):
    """
    Normalizes the proxy to the format username:password@IP:port.

    Args:
        proxy (str): The original proxy string.

    Returns:
        str: Normalized proxy string or original if already in the desired format.
    """
    parsed = parse_proxy(proxy)
    if not parsed:
        return proxy  # Return as is if parsing failed; should not happen if validated

    return f"{parsed['username']}:{parsed['password']}@{parsed['ip']}:{parsed['port']}"

def update_wallets_with_user_agents(wallets_path, proxy_path):
    """
    Reads the wallets from the specified JSON file, adds a random user agent to each wallet,
    assigns a validated proxy, and writes the updated wallets back to the file.

    Args:
        wallets_path (str): Path to the wallets JSON file.
        proxy_path (str): Path to the proxy list file.
    """
    try:
        # Step 1: Read existing wallets
        with open(wallets_path, "r", encoding="utf-8") as f:
            wallets = json.load(f)

        # Step 2: Read and validate proxies
        try:
            with open(proxy_path, "r", encoding="utf-8") as f:
                raw_proxies = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            logging.error(f"Proxy file '{proxy_path}' not found.")
            raw_proxies = []

        valid_proxies = []
        for proxy in raw_proxies:
            if validate_proxy(proxy):
                normalized = normalize_proxy(proxy)
                valid_proxies.append(normalized)
            else:
                # Error already logged in validate_proxy
                continue

        proxies_len = len(valid_proxies)

        if proxies_len == 0 and raw_proxies:
            logging.warning("No valid proxies found after validation. Proxies will be left empty for all wallets.")

        # Step 3: Update each wallet with a random user agent and proxy
        for i, wallet in enumerate(wallets):
            wallet['ua'], wallet['ua_version'] = generate_random_user_agent()

            if proxies_len > 0:
                l_proxy = valid_proxies[i % proxies_len]
            else:
                l_proxy = ''

            wallet['proxy'] = l_proxy

        # Step 4: Write the updated wallets back to the file
        with open(wallets_path, "w", encoding="utf-8") as f:
            json.dump(wallets, f, indent=4)

        print(f"Successfully updated {len(wallets)} wallets with random user agents.")
        if proxies_len > 0:
            print(f"Assigned proxies to wallets from '{proxy_path}'.")
        else:
            print("No valid proxies assigned due to validation failures.")

    except FileNotFoundError:
        logging.error(f"The file '{wallets_path}' does not exist.")
        print(f"Error: The file '{wallets_path}' does not exist.")
    except json.JSONDecodeError:
        logging.error(f"The file '{wallets_path}' is not a valid JSON file.")
        print(f"Error: The file '{wallets_path}' is not a valid JSON file.")
    except Exception as e:
        logging.exception("An unexpected error occurred.")
        print(f"An unexpected error occurred: {e}")

# Настройка логирования
logging.basicConfig(
    filename='proxy_errors.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)

# Пример использования
if __name__ == "__main__":
    print("Random Desktop User Agents (Extended):")
    update_wallets_with_user_agents("wallets.json", "proxy.txt")
