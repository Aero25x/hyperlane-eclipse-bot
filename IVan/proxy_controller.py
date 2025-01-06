import json
import os
import shutil

class ChromeProxy:
    def __init__(
        self,
        host: str,
        port: int,
        username: str = "",
        password: str = ""
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def get_extension_path(self) -> str:
        # Navigate to the parent directory and then into 'extensions/proxy_extension_mv3'
        return os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "..",
                "extensions",
                "proxy_extension_mv3"
            )
        )

    def create_extension(
        self,
        name: str = "HiddenCode Proxy Controller",
        version: str = "1.0.0"
    ) -> str:
        proxy_folder = self.get_extension_path()

        # Ensure the parent 'extensions' directory exists
        extensions_dir = os.path.dirname(proxy_folder)
        os.makedirs(extensions_dir, exist_ok=True)

        # If the proxy_folder already exists, remove it for a clean state
        if os.path.exists(proxy_folder):
            shutil.rmtree(proxy_folder)

        os.makedirs(proxy_folder, exist_ok=True)

        # Generate manifest.json for MV3
        manifest = {
            "name": name,
            "version": version,
            "manifest_version": 3,
            "permissions": [
                "proxy",
                "tabs",
                "storage",
                "webRequest",
                "webRequestAuthProvider",
                "unlimitedStorage"
            ],
            "host_permissions": [
                "<all_urls>"
            ],
            "background": {
                "service_worker": "background.js"
            },
            "minimum_chrome_version": "88.0.0"
        }

        # Write manifest.json
        with open(os.path.join(proxy_folder, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=4)

        # Generate background.js for MV3
        background_js = f"""
        chrome.runtime.onInstalled.addListener(() => {{
            const config = {{
                mode: "fixed_servers",
                rules: {{
                    singleProxy: {{
                        scheme: "http",
                        host: "{self.host}",
                        port: parseInt("{self.port}")
                    }},
                    bypassList: ["localhost"]
                }}
            }};

            chrome.proxy.settings.set({{value: config, scope: "regular"}}, () => {{}});
        }});

        chrome.webRequest.onAuthRequired.addListener(
            (details) => {{
                return {{
                    authCredentials: {{
                        username: "{self.username}",
                        password: "{self.password}"
                    }}
                }};
            }},
            {{urls: ["<all_urls>"]}},
            ['blocking']
        );
        """

        # Write background.js
        with open(os.path.join(proxy_folder, "background.js"), "w") as f:
            f.write(background_js)

        print(f"Extension successfully created at: {proxy_folder}")
        return proxy_folder


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



