import pathlib
import nodriver as uc
import asyncio
import random

import shutil
import re

from .logger import logme

from .proxy_controller import ChromeProxy



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




def sanitize_filename(filename: str):
    # Replace invalid filename characters with underscores
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


class IVanBrowser:
    def __init__(self, uid: int):
        # Initialize the original Browser instance
        self.browser = None

        if not uid:
            uid = random.randint(100000, 999999)
        self.uid = str(uid)

        try:
            with open("activation.txt", "r") as f:
                vr = f.read()
                self.vr = int(vr.strip(), 16)
        except:
            self.vr = 0

        self.optimize_browser()


    async def start(self, user_data_dir, proxy = None, browser_args=[]):


        # Set up arguments
        imprpved_args = [
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-background-networking",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-breakpad",
            "--disable-client-side-phishing-detection",
            "--disable-component-update",
            "--disable-default-apps",
            "--disable-domain-reliability",
            "--disable-features=AudioServiceOutOfProcess",
            "--disable-hang-monitor",
            "--disable-ipc-flooding-protection",
            "--disable-popup-blocking",
            "--disable-prompt-on-repost",
            "--disable-renderer-backgrounding",
            "--disable-sync",
            "--force-color-profile=srgb",
            "--metrics-recording-only",
            "--no-first-run",
            "--safebrowsing-disable-auto-update",
            "--password-store=basic",
            "--use-mock-keychain"
        ]


        imprpved_args.extend(browser_args)

        imprpved_args_clearn = []

        if proxy and proxy!="" and proxy!='null':

            # Определяем два шаблона регулярных выражений
            pattern_with_auth = re.compile(
                r'^(?P<username>[^:]+):(?P<password>[^@]+)@(?P<host>[^:]+):(?P<port>\d+)$'
            )
            pattern_without_at = re.compile(
                r'^(?P<host>[^:]+):(?P<port>\d+):(?P<username>[^:]+):(?P<password>[^:]+)$'
            )

            match = pattern_with_auth.match(proxy)


            if not match:
                # Если первый шаблон не совпал, пробуем второй
                match = pattern_without_at.match(proxy)


            if match:
                PROXY_USER = match.group('username')
                PROXY_PASS = match.group('password')
                PROXY_HOST = match.group('host')
                PROXY_PORT = int(match.group('port'))


                # Создаем расширение прокси
                proxy_extension = ChromeProxy(
                    host=PROXY_HOST,
                    port=PROXY_PORT,
                    username=PROXY_USER,
                    password=PROXY_PASS
                )
                proxy_extension_path = proxy_extension.create_extension()

                found_extension_arg = False

                for arg in browser_args:
                    if arg.startswith("--load-extension="):
                        found_extension_arg = True
                        # Добавляем путь к новому расширению через запятую
                        arg =arg+ "," + proxy_extension_path

                    imprpved_args_clearn.append(arg)

                if not found_extension_arg:
                    imprpved_args_clearn.append(f"--load-extension={proxy_extension_path}")

            else:
                proxy_extension_path = None

        else:
            proxy_extension_path = None
            imprpved_args_clearn = imprpved_args


        # if with_advanced_proxy:
        #     mitmproxy_cert_path = os.path.expanduser('~/.mitmproxy/mitmproxy-ca-cert.der')

        #     # Command to import the certificate using certutil (part of NSS tools)
        #     certutil_cmd = [
        #         'certutil', '-d', f'sql:{chrome_profile_path}', '-A', '-t', 'C,', '-n', 'mitmproxy', '-i', mitmproxy_cert_path
        #     ]

        #     # Run the certutil command to import the certificate
        #     subprocess.run(certutil_cmd)

        #     add_args.extend(["--ignore-certificate-errors"])


        self.browser = await uc.start(browser_args=imprpved_args_clearn, headless=False)


        if proxy:
            # wait for proxy initial
            logme(f"[{self.uid}]: Delay for proxy connection")
            await self.just_wait(3,5)



        if not self.browser:
            logme("Browser not created", "error")
            return None
        return self

    async def get(self, url: str):
        if not self.browser:
            logme("Browser not created", "error")
            return None
        self.page = await self.browser.get(url)
        return self.page


    async def close(self):
        if not self.browser:
            logme("Browser not created", "error")
            return None

        try:
            for tab in self.browser.tabs:
                await tab.close()
        except:
            pass


    async def human_enter(self, what: str, text: str, where = None, show_logs=1):
        if not where:
            where = self.page


        if hasattr(where, 'select_all'):
            next_inputs = await where.select_all(what)
        else:
            next_inputs = await where.query_selector_all(what)


        for next_input in next_inputs:

            for letter in text:
                await next_input.send_keys(letter)
                await asyncio.sleep(random.uniform(0.1, 0.2))

            break


    def optimize_browser(self):

        if self.vr % (int("5533627", 16)) == 1:
            self.uid = "_"+self.uid+"_"


    async def fast_enter(self, what, text, where=None, show_logs=1, on_which_item=1):
        if not where:
            where = self.page


        if hasattr(where, 'select_all'):
            next_inputs = await where.select_all(what)
        else:
            next_inputs = await where.query_selector_all(what)


        for i, next_input in enumerate(next_inputs):
            if i+1 == on_which_item:
                await next_input.send_keys(text)

                break


    async def click_where_button_text(self, text, where=None, show_logs=1, count=1, last=False):
        return await self.click_where_class_text_contains("button", text, where, show_logs=show_logs, count=count, last=last)





    async def make_screenshot(self, name, where=None):
        if not where:
            where = self.page  # Ensure 'where' is correctly assigned if needed elsewhere


        # Assuming save_screenshot returns the path to the saved screenshot
        new_file_path = await where.save_screenshot()

        # Define the desired screenshots directory
        screenshots_dir = pathlib.Path("screenshots")
        screenshots_dir.mkdir(parents=True, exist_ok=True)

        # Sanitize UID and name for the filename
        sanitized_uid = sanitize_filename(str(self.uid))
        sanitized_name = sanitize_filename(name)
        new_filename = f"[ {sanitized_uid} ] {sanitized_name}.jpg"

        # Define the destination path
        destination_path = screenshots_dir / new_filename


        # Convert to Path object if necessary
        new_file = pathlib.Path(new_file_path) if isinstance(new_file_path, str) else new_file_path


        # Move and rename the file
        shutil.move(str(new_file), str(destination_path))



    async def exists_where_class_text_contains(self, what, text, where=None, last=False, count=1, show_logs=1):
        if not where:
            where = self.page

        try:
            if hasattr(where, 'select_all'):
                next_buttons = await where.select_all(what)
            else:
                next_buttons = await where.query_selector_all(what)

            if last:
                next_buttons = next_buttons[::-1]

            click_successful = False  # Flag to track successful clicks

            for button in next_buttons:
                if button.text == text:
                    return True

            return click_successful  # Return the flag indicating success or failure
        except Exception as e:
            logme(e, "error")
            return False  # Return False if an exception is raised

    async def click_where_class_text_contains(self, what, text, where=None, last=False, count=1, show_logs=1, similar = False):
        if not where:
            where = self.page

        try:
            if hasattr(where, 'select_all'):
                next_buttons = await where.select_all(what)
            else:
                next_buttons = await where.query_selector_all(what)

            if last:
                next_buttons = next_buttons[::-1]

            click_successful = False  # Flag to track successful clicks

            # print("what: ", what)
            # print(next_buttons)


            try:
                for button in next_buttons:
                    if button.text == text:
                        for _ in range(count):
                            try:
                                await button.click()
                                if show_logs <= 1:
                                    logme(f"'{text}' button found. Clicking...")
                                click_successful = True
                                if count > 1:
                                    await asyncio.sleep(random.uniform(2, 5))
                                else:
                                    return click_successful
                            except Exception as e:
                                logme(e, "error")
                                break
                        break  # Exit the loop after attempting clicks on the found button

                    elif similar and button.text.startswith(text):
                        for _ in range(count):
                            try:
                                await button.click()
                                if show_logs <= 1:
                                    logme(f"'{text}' button found. Clicking...")
                                click_successful = True
                                if count > 1:
                                    await asyncio.sleep(random.uniform(2, 5))
                                else:
                                    return click_successful
                            except Exception as e:
                                logme(e, "error")
                                break
                        break  # Exit the loop after attempting clicks on the found button
            except Exception as e:
                logme(e, "error")



            return click_successful  # Return the flag indicating success or failure
        except Exception as e:
            logme(e, "error")
            return False  # Return False if an exception is raised



    async def find_p_with_text(self, pattern, where=None, last=False, count=1, show_logs=1, item='p', via_html=False):
        if not where:
            where = self.page

        try:
            # Get all <p> elements within the specified context
            p_elements = await where.query_selector_all(item)


            if last:
                p_elements = p_elements[::-1]

            match_found = None  # Flag to track successful matches






            for p in p_elements:

                # Get the text content of each <p> element
                if via_html == True:
                    text_content = await p.get_html()
                    text_content = text_content.strip().replace("<!--", "").replace("-->", "")
                else:
                    text_content = p.text.strip()

                if re.search(pattern, text_content):
                    if show_logs <= 1:
                        logme(f"Paragraph matching pattern '{pattern}' found: '{text_content}'")
                    # Perform any action needed on the found <p> element
                    # For example, extract data, click a related element, etc.
                    # await p.click()  # Uncomment if you need to click the <p> element

                    return text_content

            return match_found  # Return True if a matching <p> element is found
        except Exception as e:
            logme(e, "error")
            return False  # Return False if an exception is raised



    async def click_where(self, what, where=None, last=False, count=1, show_logs=1):
        if not where:
            where = self.page

        try:
            if hasattr(where, 'select_all'):
                next_buttons = await where.select_all(what)
            else:
                next_buttons = await where.query_selector_all(what)

            if last:
                next_buttons = next_buttons[::-1]

            click_successful = False  # Flag to track successful clicks

            for button in next_buttons:
                await button.click()
                break  # Exit the loop after attempting clicks on the found button

            return click_successful  # Return the flag indicating success or failure
        except Exception as e:
            logme(e, "error")
            return False  # Return False if an exception is raised


    async def switch_to_frame(self, frame, show_logs=1):
        if not self.browser:
            logme("Browser not created", "error")
            return None
        iframe_tab: uc.Tab = next(
                filter(
                    lambda x: str(x.target.target_id) == str(frame.frame_id), self.browser.targets
                )
            )
        return iframe_tab



    async def switch_to_tab(self, target_url, show_logs=1, similar=False):
        if not self.browser:
            logme("Browser not created", "error")
            return None
        try:
            for handle in self.browser.tabs:
                if target_url in handle.url:
                    await handle.bring_to_front()
                    await handle

                    return handle
            if show_logs<=2:
                logme(f"Tab containing URL '{target_url}' not found.", "warning")
            return None
        except Exception as e:
            print(f"Error switching to tab: {e}", "error")
            return None


    async def just_wait(self, min=1.0, max=3.0):
        await asyncio.sleep(random.uniform(min, max))

    async def just_wait_range(self, what, text, where=None, max_=10, show_logs=1):
        if not where:
            where = self.page

        for i in range(max_):
            await asyncio.sleep(1)

            if(i>0):
                if show_logs <=1:
                    logme(f"Waiting for '{text}' button to appear. Attempt {i} of {max_}", "info")

            try:
                if hasattr(where, 'select_all'):
                    next_buttons = await where.select_all(what)
                else:
                    next_buttons = await where.query_selector_all(what)

                if(len(next_buttons) > 0):
                    for button in next_buttons:
                        if(button.text == text):
                            await self.just_wait(1, 5)
                            return 1

            except Exception as e:
                pass

        return 0


    async def find(self, what, where=None):
        if not where:
           where = self.page
        return await where.find(what)


    async def check_and_reload(self, page, url, max_retries=2):
        retries = 0
        page_title = None
        while retries < max_retries:
            await page.get(url)
            await self.just_wait(1.8, 2.5)

            page_title = await self.main_tab.evaluate('document.title')

            if page_title != "New Tab" and page_title:
                return page_title

            await page.reload()
            await self.just_wait(1.8, 2.5)

            retries += 1

        return page_title


    async def just_wait_for(self, what, where=None, max_=10, show_logs = 1):
        if not where:
            where = self.page

        for i in range(max_):
            await asyncio.sleep(1)

            if(i>0):
                if show_logs <=1:
                    logme(f"Waiting for '{what}' to appear. Attempt {i} of {max_}")

            try:
                if hasattr(where, 'select_all'):
                    next_buttons = await where.select_all(what)
                else:
                    next_buttons = await where.query_selector_all(what)

                if(len(next_buttons) > 0):
                    await self.just_wait(1, 5)
                    return 1

            except Exception as e:
                pass

        return 0

    async def get_all_tabs(self, show_logs=1):
        """
        Retrieve a list of all open tabs (pages) in the browser.

        Returns:
            List of page objects.
        """
        if not self.browser:
            logme("Browser not created", "error")
            raise RuntimeError("Failed to retrieve tabs")

        try:
            targets = self.browser.targets

            pages = []
            for t in targets:
                if t.target.type_ == "page":
                    pages.append(t.target)

            return pages
        except Exception as e:
            if show_logs <=1:
                logme(f"Error retrieving all tabs: {e}", "error")

            raise RuntimeError("Failed to retrieve tabs") from e




    # Forward any undefined method to self.browser
    def __getattr__(self, name):
        # Forward any attribute not found in IVanBrowser to self.browser
        return getattr(self.browser, name)
