# Created by Aero25x
# For HiddenCode
# https://t.me/hidden_coding


import asyncio
import re
import math
from IVan.xvfb_controller import conditional_xvfb
import os
from IVan.IVanBrowser import IVanBrowser
from .logger import logme
import random
from IVan import send_to_eclipse

# TODO:
# 1. Add Screen text capture and OCR to speed up the process
# 2. Optimize the code to run faster for less resources usage
# 3. Make undertect docker


PASSWORD = "HiddenCode"
MAKE_HIDDEN = False
# 3 - only errors
# 2 - errors and warings
# 1 - all
SHOW_MOVEMENT_LOGS = 2
RANDOM_START_PAGE= ['https://google.com', "https://duckduckgo.com/", "https://coinmarketcap.com/", "https://dropstab.com/", "https://www.coingecko.com/"]


with_advanced_proxy = False




async def click_in_phantom(browser, text, delay_multi = 1.0):

    try:
        phantom_page = await browser.switch_to_tab("chrome-extension://aflkmfhebedbjioipglgcbcmnbpgliof/popout.html", show_logs=SHOW_MOVEMENT_LOGS, similar=True)
    except:
        phantom_page = None


    if phantom_page:
    
        # check is required enter passowd

        # try:
        #     password_inputs = await phantom_page.select_all("input[data-testid=unlock-form-password-input]", timeout=1)

        #     if password_inputs:
        #         await browser.fast_enter("input[data-testid=unlock-form-password-input]", PASSWORD, phantom_page, show_logs=SHOW_MOVEMENT_LOGS)

        #         await browser.just_wait(2,3)

        #         if not await browser.click_where_class_text_contains("button", "Unlock", phantom_page, show_logs=SHOW_MOVEMENT_LOGS):
        #             return

        #         await browser.just_wait(1,2)

        #         await browser.just_wait(int(3*delay_multi), int(7*delay_multi))
        # except:
        #     await browser.just_wait(int(3*delay_multi), int(7*delay_multi))
        # by Aer025x
		

        await browser.just_wait(1,1)

        status = await browser.click_where_class_text_contains('div[tabindex="0"]', text, phantom_page, show_logs=SHOW_MOVEMENT_LOGS)
        if not status:

            await browser.just_wait(1, 2)
            for i in range(7):
                status = await browser.click_where_class_text_contains('div[tabindex="0"]', text, phantom_page, show_logs=SHOW_MOVEMENT_LOGS)
                if not status:
                    await browser.just_wait(1, 2)

                    if i == 6:
                        return
                else:
                    break

        return True



async def change_speed_fee(browser):
    try:
        await browser.just_wait(2,7)

        await browser.click_where("button:has(svg.settings-icon)", show_logs=SHOW_MOVEMENT_LOGS)
            # return

        await browser.just_wait(1,2)

        await browser.click_where_class_text_contains("button", "Fast", show_logs=SHOW_MOVEMENT_LOGS, similar=True)
            # return

        await browser.just_wait(1,2)

    except Exception as e:
        logme(str(e), "error")




async def connect_wallet(all_tabs, browser, profile_id, wallet_key):
    for tab in all_tabs:
        # initialize for onboarding page if opened in Phantom Wallet
        if tab.url == "chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/onboarding.html":


            phantom_page = await browser.switch_to_tab("chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/onboarding.html", show_logs=SHOW_MOVEMENT_LOGS)

            if not await browser.click_where_class_text_contains("button", "I already have a wallet", phantom_page, show_logs=SHOW_MOVEMENT_LOGS):
                return

            await browser.just_wait()


            if " " in wallet_key:
                if not await browser.click_where_class_text_contains("button", "Import Secret Recovery Phrase", phantom_page, show_logs=SHOW_MOVEMENT_LOGS):
                    return

                await browser.just_wait(0.5,1)

                wallet_keys = wallet_key.split(" ")

                for i in range(12):
                    await browser.fast_enter(f"input[data-testid='secret-recovery-phrase-word-input-{i}']", wallet_keys[i], phantom_page, show_logs=SHOW_MOVEMENT_LOGS)

                if not await browser.click_where_class_text_contains("button", "Import Wallet", phantom_page, show_logs=SHOW_MOVEMENT_LOGS):
                    return

                await browser.just_wait(4.5,7)
                if not await browser.click_where_class_text_contains("button", "Continue", phantom_page, show_logs=SHOW_MOVEMENT_LOGS):
                    return

                await browser.just_wait(0.5,1)

                await browser.fast_enter("input[name=password]", PASSWORD, phantom_page, show_logs=SHOW_MOVEMENT_LOGS)
                await browser.fast_enter("input[name=confirmPassword]", PASSWORD, phantom_page, show_logs=SHOW_MOVEMENT_LOGS)

                await browser.click_where("input[type=checkbox]", phantom_page, show_logs=SHOW_MOVEMENT_LOGS)
                if not await browser.click_where_class_text_contains("button", "Continue", phantom_page, show_logs=SHOW_MOVEMENT_LOGS):
                    return

                await browser.just_wait(2,5)

            else:
                if not await browser.click_where_class_text_contains("button", "Import Private Key", phantom_page, show_logs=SHOW_MOVEMENT_LOGS):
                    return

                await browser.just_wait(0.5,1)

                await browser.human_enter("input[placeholder=Name]", profile_id, phantom_page, show_logs=SHOW_MOVEMENT_LOGS)

                await browser.fast_enter("textarea[placeholder='Private key']", wallet_key, phantom_page, show_logs=SHOW_MOVEMENT_LOGS)

                await browser.click_where_class_text_contains("button", "Import", phantom_page, show_logs=SHOW_MOVEMENT_LOGS)

                await browser.fast_enter("input[name=password]", PASSWORD, phantom_page, show_logs=SHOW_MOVEMENT_LOGS)
                await browser.fast_enter("input[name=confirmPassword]", PASSWORD, phantom_page, show_logs=SHOW_MOVEMENT_LOGS)

                await browser.click_where("input[type=checkbox]", phantom_page, show_logs=SHOW_MOVEMENT_LOGS)

                if not await browser.click_where_class_text_contains("button", "Continue", phantom_page, show_logs=SHOW_MOVEMENT_LOGS):
                    return

                await browser.just_wait(2,5)

            if not await browser.click_where_class_text_contains("button", "Get Started", phantom_page, show_logs=SHOW_MOVEMENT_LOGS):
                return

            await browser.just_wait(1,2)

            logme(f"[{profile_id}]: Phantom Wallet imported!")

            break

        elif tab.url == "chrome-extension://aflkmfhebedbjioipglgcbcmnbpgliof/options.html?onboarding=true":

            backpack_page = await browser.switch_to_tab("chrome-extension://aflkmfhebedbjioipglgcbcmnbpgliof/options.html?onboarding=true", show_logs=SHOW_MOVEMENT_LOGS)

            if not await browser.click_where_class_text_contains("button", "Import Wallet", backpack_page, show_logs=SHOW_MOVEMENT_LOGS):
                return

            await browser.just_wait()

            if not await browser.click_where_class_text_contains("button", "Solana", backpack_page, show_logs=SHOW_MOVEMENT_LOGS):
                return
        else:
            print(f"NOT FOUND URL in wallet : {tab} {tab.url}")



async def main(id, wallet, todo):

    screen_size = (1920, 1080)

    profile_id = wallet["address"][:4]+"..."+wallet["address"][-4:]
    ivan_ua = wallet['ua']


    with conditional_xvfb(MAKE_HIDDEN):

        # Initialize the browser
        browser = IVanBrowser(profile_id)
        chrome_profile_path = f'profiles/__{browser.uid}__'



        # Define the absolute path to your extension
        extension_relative_path = 'extensions/aflkmfhebedbjioipglgcbcmnbpgliof/0.10.103_0'
        # extension_relative_path = 'extensions/bfnaelmomeimhlpmgjnjophhpkkoljpa/24.25.0_0'
        extension_absolute_path = os.path.abspath(extension_relative_path)


        # Add Chrome arguments
        add_args = [
            f"--window-size={screen_size[0]},{screen_size[1]}",  # Screen size
            f"--user-agent={ivan_ua}",
            f"--load-extension={extension_absolute_path}",  # Load proxy and additional extensions
        ]


        await browser.start(
            user_data_dir=chrome_profile_path,
            browser_args=add_args,
            proxy=wallet['proxy']
        )

        logme("Open random page")



        await browser.get("chrome-extension://aflkmfhebedbjioipglgcbcmnbpgliof/options.html?onboarding=true")


        await asyncio.sleep(3)



        if wallet['privateKey'] and wallet['privateKey']!='' and len(wallet['privateKey'])>32:
            wallet_key = wallet['privateKey']
        elif wallet['phrase'] and wallet['phrase']!='' and len(wallet['phrase'])>32:
            wallet_key = wallet['phrase']
        else:
            logme(f"[{browser.uid}]: Incorrect format of wallet info, please check is correct entered: phrase or privateKey", "error")
            return






        # Backpack wallet preparation
        if not await browser.click_where_class_text_contains("button", "Import Wallet", show_logs=SHOW_MOVEMENT_LOGS):
            return

        await browser.just_wait(1,1)

        if not await browser.click_where_class_text_contains("button", "Solana", show_logs=SHOW_MOVEMENT_LOGS):
            return

        await browser.just_wait(1,1)

        if not await browser.click_where_class_text_contains("button", "Import private key", show_logs=SHOW_MOVEMENT_LOGS):
            return

        await browser.just_wait(1,1)

        await browser.fast_enter('textarea[placeholder="Enter private key"]', wallet_key, show_logs=SHOW_MOVEMENT_LOGS)

        if not await browser.click_where_class_text_contains("button", "Import", show_logs=SHOW_MOVEMENT_LOGS):
            return

        await browser.just_wait(1,1)

        await browser.fast_enter('input[placeholder="Password"]', PASSWORD, show_logs=SHOW_MOVEMENT_LOGS)
        await browser.fast_enter('input[placeholder="Confirm Password"]', PASSWORD, show_logs=SHOW_MOVEMENT_LOGS)

        await browser.click_where("input[type=checkbox]", show_logs=SHOW_MOVEMENT_LOGS)
        await browser.just_wait(0.4,1)

        if not await browser.click_where_class_text_contains("button", "Next", show_logs=SHOW_MOVEMENT_LOGS):
            return

        await browser.just_wait(5, 7)









        await browser.get(random.choice(RANDOM_START_PAGE))


        # placing order by A3ro25x
        if SHOW_MOVEMENT_LOGS<=1:
            logme(f"[{browser.uid}]: Placing Orders")




        for i_task, task in enumerate(todo):


            if task['order'] == "Market":

                await browser.get("chrome-extension://aflkmfhebedbjioipglgcbcmnbpgliof/popup.html")

                await browser.just_wait(1, 2)

                temp_items_network = await browser.page.select_all("#root > span:nth-child(1) > span > div > div > div:nth-child(7) > div > div > div.css-175oi2r.r-13awgt0 > div.css-175oi2r.r-13awgt0 > div > div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-12vffkv > div.css-175oi2r.r-13awgt0.r-12vffkv > div > div > div > div.css-175oi2r.r-13awgt0 > div > div.css-175oi2r.r-13awgt0.r-1udh08x > div > div > div > div > div > div > div.css-175oi2r.r-13awgt0 > div > div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-12vffkv > div.css-175oi2r.r-13awgt0.r-12vffkv > div > div > div > div.css-175oi2r.r-184en5c.r-12vffkv > div > div > div.css-175oi2r.r-1oszu61.r-13awgt0.r-18u37iz.r-12vffkv > div.css-175oi2r.r-1777fci.r-12vffkv > div > div._bg-0hover-1067792163._dsp-flex._ai-stretch._fd-row._fb-auto._bxs-border-box._pos-relative._mih-0px._miw-0px._h-10037._fs-0._btw-0px._brw-1px._bbw-0px._blw-0px._bts-solid._brs-solid._bbs-solid._bls-solid._btc-65753118._brc-65753118._bbc-65753118._blc-65753118 > div > div")


                print(f"Clicked on Network Button: {len(temp_items_network)}")

                for item in temp_items_network:
                    await item.click()

                await browser.just_wait(1,2)

                try:
                    temp_items_network = await browser.page.select_all("div.is_PopoverClose")
                except:
                    await browser.just_wait(1,2)
                    try:
                        temp_items_network = await browser.page.select_all("div.is_PopoverClose")
                    except:
                        temp_items_network = ["", "", ""]


                print(f"Need Network switching: {task['network0']} # {len(temp_items_network)}")

                if len(temp_items_network) == 3: # solana and eclipse imported
                    print("2 Network have already been imported")
                elif len(temp_items_network) <= 2: # solana only



                    await browser.just_wait(1,2)
                    temp_items_network2 = await browser.page.select_all("div.is_PopoverClose")

                    print(f"Found Network button in BackPack: {len(temp_items_network2)}")

                    for parent in temp_items_network2[::-1][:1]:
                        child_div = await parent.query_selector("div")  # Replace 'div.child-class' with your actual selector

                        if child_div:
                            # Click on the child div
                            await child_div.click()
                            break
                        else:
                            print("Child div not found within the parent element.")





                    await browser.just_wait(1,1)

                    if not await browser.click_where_button_text("Eclipse", show_logs=SHOW_MOVEMENT_LOGS):
                        logme(f"[{browser.uid}]: failed to click on Eclipse")
                        return

                    await browser.just_wait(2,3)


                    temp_items_network3 = await browser.page.select_all("#root > span:nth-child(1) > span > div > div > div:nth-child(7) > div > div > div.css-175oi2r.r-13awgt0 > div.css-175oi2r.r-13awgt0 > div:nth-child(2) > div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-12vffkv > div.css-175oi2r.r-13awgt0.r-12vffkv > div > div > div > div.css-175oi2r.r-13awgt0 > div > div > div > div.css-175oi2r.r-13awgt0 > div:nth-child(2) > div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-12vffkv > div.css-175oi2r.r-13awgt0.r-12vffkv > div > div > div > div.css-175oi2r.r-13awgt0 > div > div.view > div > div:nth-child(2) > div")

                    for button in temp_items_network3:
                        await button.click()

                    await browser.just_wait(3,5)

                    await browser.get("chrome-extension://aflkmfhebedbjioipglgcbcmnbpgliof/popup.html")



                    await browser.just_wait(1,2)
                    temp_items_network3 = await browser.page.select_all("#root > span:nth-child(1) > span > div > div > div:nth-child(7) > div > div > div.css-175oi2r.r-13awgt0 > div.css-175oi2r.r-13awgt0 > div:nth-child(2) > div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-12vffkv > div.css-175oi2r.r-13awgt0.r-12vffkv > div > div > div > div.css-175oi2r.r-13awgt0 > div > div > div > div.css-175oi2r.r-13awgt0 > div:nth-child(2) > div.css-175oi2r.r-1p0dtai.r-1d2f490.r-u8s1d.r-zchlnj.r-ipm5af.r-12vffkv > div.css-175oi2r.r-13awgt0.r-12vffkv > div > div > div > div.css-175oi2r.r-184en5c.r-12vffkv > div > div > div.css-175oi2r.r-1oszu61.r-13awgt0.r-18u37iz.r-12vffkv > div.css-175oi2r.r-1awozwy.r-18u37iz.r-1h0z5md.r-1iusvr4.r-16y2uox.r-12vffkv > a")

                    for button in temp_items_network3:
                        await button.click()


                    await browser.just_wait(1.5,2)

                    temp_items_network3 = await browser.page.select_all("button.MuiButtonBase-root.MuiIconButton-root.css-8owaep.MuiIconButton-sizeLarge.css-1i4dq24")

                    for button in temp_items_network3:
                        await button.click()

                    await browser.just_wait(1.5,2)

                    temp_items_network3 = await browser.page.select_all('div[aria-haspopup="dialog"]')

                    for button in temp_items_network3[:1]:
                        await button.click()

                    await browser.just_wait(0.7,1)


                print(f"Network switching: {task['network0']}")

                if not await browser.click_where_class_text_contains("div.is_PopoverClose>div", task['network0'], show_logs=SHOW_MOVEMENT_LOGS):
                    logme(f"[{browser.uid}]: failed to click on network")
                    return

                await browser.just_wait(0.7,1)

                if MAKE_HIDDEN:
                    await browser.make_screenshot(f"[{i_task}] {task['market_id']} - switch network")





            elif task['order'] =='Send':

                if task['market_id'] == 'gasZip':

                    try:
                        tx_hash = send_to_eclipse.send_native_from_base_to_elcipse(
                            private_key=wallet['evm_privateKey'],
                            amount_eth=round(random.uniform(task['min_amount'], task['max_amount']), 16),
                            solana_address=wallet['address'],
                            provider_url="REPLACEME"  # UPDATE TO BASE RPC
                        )
                        print(f"Transaction successful with hash: {tx_hash}\n\n\n")
                    except Exception as e:
                        print(f"[send_native_from_base_to_elcipse]: An error occurred: {e}")

                else:
                    print("Found unknown market id in Send")


                break






            for tries in range(3):

                await browser.get(f"{task['market_id']}")

                await browser.just_wait(7, 10)

                if MAKE_HIDDEN:
                    await browser.make_screenshot(f"[{i_task}] 1. Opened {task['market_id']}")

                # check is requered connect wallet

                if tries + 1 == 1:
                    if await browser.exists_where_class_text_contains("button", 'Connect wallet'):
                        print("Via fast button")
                        if SHOW_MOVEMENT_LOGS <=1:
                            logme(f"[{browser.uid}]: Connecting wallet to {task['market_id']}")

                        await browser.click_where_button_text("Connect wallet", show_logs=SHOW_MOVEMENT_LOGS, last=True)
                        await browser.just_wait()
                        await browser.make_screenshot(f"[{i_task}] 2. Backpack is corrected to ")

                        await browser.click_where_class_text_contains("button", "Solana", show_logs=SHOW_MOVEMENT_LOGS)

                        await browser.just_wait(1,2)

                        await browser.click_where_class_text_contains("button", "Backpack", show_logs=SHOW_MOVEMENT_LOGS)

                        await browser.just_wait(1,2)
                        # switchin to phantom

                        await click_in_phantom(browser, "Approve")



                        if MAKE_HIDDEN:
                            await browser.make_screenshot(f"[{i_task}] 2. Phantom is corrected to {task['market_id']}")

                    elif await browser.exists_where_class_text_contains("button", 'Connect Wallet'):
                        print("Via fast button")
                        if SHOW_MOVEMENT_LOGS <=1:
                            logme(f"[{browser.uid}]: Connecting wallet to {task['market_id']}")

                        await browser.click_where_button_text("Connect Wallet", show_logs=SHOW_MOVEMENT_LOGS, last=True)
                        await browser.just_wait()
                        await browser.make_screenshot(f"[{i_task}] 2. Backpack is corrected to ")

                        await browser.click_where_class_text_contains("button", "Solana", show_logs=SHOW_MOVEMENT_LOGS)

                        await browser.just_wait(1,2)

                        await browser.click_where_class_text_contains("button", "Backpack", show_logs=SHOW_MOVEMENT_LOGS)

                        await browser.just_wait(1,2)
                        # switchin to phantom


                        await click_in_phantom(browser, "Approve")



                        if MAKE_HIDDEN:
                            await browser.make_screenshot(f"[{i_task}] 2. Phantom is corrected to {task['market_id']}")




                # set up order
                await browser.just_wait(3,5)


                if task['action'] == 'usenexus':


                    if not await browser.click_where_button_text('From', show_logs=SHOW_MOVEMENT_LOGS):
                        logme(f"[{browser.uid}]: failed to set: From network {task['network0']}")
                        return

                    await browser.just_wait(1,1.5)

                    await browser.fast_enter('input[placeholder="Chain Name or ID"]', task['network0'])

                    await browser.just_wait(1,1.5)

                    if not await browser.click_where_button_text(task['network0'], show_logs=SHOW_MOVEMENT_LOGS):
                        logme(f"[{browser.uid}]: failed to click on from network select: {task['network0']}")
                        return


                    await browser.just_wait(1,1.5)


                    if not await browser.click_where_button_text('To', show_logs=SHOW_MOVEMENT_LOGS):
                        logme(f"[{browser.uid}]: failed to set: From network {task['network1']}")
                        return


                    await browser.just_wait(1,1.5)

                    await browser.fast_enter('input[placeholder="Chain Name or ID"]', task['network1'])

                    await browser.just_wait(1,1.5)

                    if not await browser.click_where_button_text(task['network1'], show_logs=SHOW_MOVEMENT_LOGS):
                        logme(f"[{browser.uid}]: failed to click on TO network select: {task['network1']}")
                        return


                    await browser.just_wait(1,1.5)

                    if not await browser.click_where_button_text('Select Token', show_logs=SHOW_MOVEMENT_LOGS):
                        logme(f"[{browser.uid}]: failed to set: Select Token {task['token0']}")
                        return


                    await browser.just_wait(1,1.5)

                    await browser.fast_enter('input[name="token-search"]', task['token0'])


                    if not await browser.click_where_button_text(task['token0'], show_logs=SHOW_MOVEMENT_LOGS):
                        logme(f"[{browser.uid}]: failed to click on token select: {task['token0']}")
                        return


                    await browser.just_wait(1,1.5)

                    if not await browser.click_where_button_text("Max", show_logs=SHOW_MOVEMENT_LOGS):
                        logme(f"[{browser.uid}]: failed to click on Max")
                        return

                    if not await browser.click_where_button_text("Self", show_logs=SHOW_MOVEMENT_LOGS):
                        logme(f"[{browser.uid}]: failed to click on Self")
                        return




                    available_max_balance = await browser.find_p_with_text(r'My balance:\s*.*', show_logs=2, item='div')
                    if not available_max_balance:
                        await browser.screenshoot(f"[{browser.uid}]: Failed to found 'My Balance'")
                        logme(f"[{browser.uid}]: Failed to found 'My Balance'")
                        return
                    else:
                        if available_max_balance == "My balance: 0":
                            logme(f"[{browser.uid}]: Balance is Empty")
                            await browser.make_screenshot(f"[{i_task}] Balance is Empty - {task['market_id']}")
                            return


                    await browser.just_wait(5,10)

                    if not await browser.click_where_button_text("Continue", show_logs=SHOW_MOVEMENT_LOGS):
                        logme(f"[{browser.uid}]: failed to click on Continue")
                        return

                    await browser.just_wait(5,7)

                    if not await browser.click_where_button_text(f"Send to {task['network1']}", show_logs=SHOW_MOVEMENT_LOGS):
                        logme(f"[{browser.uid}]: failed to click on Send to {task['network1']}")
                        return

                    await browser.just_wait(3,5)
                    # print("confirm in trasnaction")
                    await click_in_phantom(browser, "Approve")


                    await browser.just_wait(30,35)


                    H1ddenC0de_balance = await browser.find_p_with_text(r'My balance:\s*.*', show_logs=2, item='div')
                    if not H1ddenC0de_balance:
                        await browser.screenshoot(f"[{browser.uid}]: Failed to found 'My Balance'")
                        logme(f"[{browser.uid}]: Failed to found 'My Balance'")
                        return

                    if H1ddenC0de_balance == available_max_balance:
                        await browser.make_screenshot(f"[{i_task}] Balance failed to to change - {task['market_id']}")

                        print(f"[{browser.uid}]: Failed to swap")
                    else:
                        print(f"[{browser.uid}]: Balance changed after swap")
                        break


                elif task['action'] == 'lifinity':

                    all_temp_items = await browser.page.select_all("body > div > div.flex-1 > div > div.flex.justify-center.pt-24 > div > div > div > div.mx-6.mb-2.mt-2.flex.items-center.justify-between.rounded-md.bg-slate-300\/50.px-2.dark\:bg-slate-500\/30 > div > button")

                    for item in all_temp_items:
                        await item.click()

                    await browser.just_wait(0.3,0.5)

                    await browser.fast_enter('input[placeholder="Search name or mint address"]', task['token0'])

                    await browser.just_wait(0.3,0.5)

                    if not await browser.click_where_class_text_contains('div.last\:mb-0:nth-child(1) > button', task['token0'], show_logs=SHOW_MOVEMENT_LOGS):
                        logme(f"[{browser.uid}]: failed to click on from token select: {task['token0']}")
                        return


                    await browser.just_wait(1,1.5)

                    all_temp_items = await browser.page.select_all("div.mx-6:nth-child(5) > div:nth-child(1) > button:nth-child(1)")


                    for item in all_temp_items:
                        await item.click()

                    await browser.just_wait(0.3,0.5)

                    await browser.fast_enter('input[placeholder="Search name or mint address"]', task['token1'])

                    await browser.just_wait(0.3,0.5)

                    if not await browser.click_where_class_text_contains('div.last\:mb-0:nth-child(1) > button', task['token1'], show_logs=SHOW_MOVEMENT_LOGS):
                        logme(f"[{browser.uid}]: failed to click on from token1 select: {task['token1']}")
                        return


                    await browser.just_wait(1,1.5)

                    available_max_balance = await browser.find_p_with_text(r'Balance:\s*.*', show_logs=2, item='button.text-gray-500', via_html=True)
                    if not available_max_balance:
                        await browser.screenshoot(f"[{browser.uid}]: Failed to found 'Balance'")
                        logme(f"[{browser.uid}]: Failed to found 'Balance'")
                        return
                    else:


                        # Define a regex pattern to capture the numeric value after 'Balance:'
                        pattern = r'Balance:\s*([\d.]+)'

                        match = re.search(pattern, available_max_balance)
                        if match:
                            balance_str = match.group(1)
                            available_max_balance = float(balance_str)
                        else:
                            available_max_balance = 0  # Default value or handle accordingly


                        try:
                            if task['type']=='Buy' and task['token0']=='USDC':
                                available_max_balance = math.floor(available_max_balance*100)/100
                        except Exception as e:
                            print(e)
                            available_max_balance = 0


                    if available_max_balance == 0:
                        print(f"lifinity balance is zero of token {task['token0']} - by HiddenCode")
                        return


                    available_max_balance = available_max_balance * random.randint(task['percentage_min'], task['percentage_max']) / 100

                    await browser.human_enter('input[name="amountIn"]', str(available_max_balance), show_logs=SHOW_MOVEMENT_LOGS)

                    await browser.just_wait(1,1.5)

                    if not await browser.click_where_button_text("Swap", show_logs=SHOW_MOVEMENT_LOGS):
                        logme(f"[{browser.uid}]: failed to click on Swap")
                        return


                    if MAKE_HIDDEN:
                        await browser.screenshoot(f"[{browser.uid}]: In Swap on lifi")

                    await browser.just_wait(1,1.5)
                    await click_in_phantom(browser, "Approve")

                    await browser.just_wait(20,30)



                    H1ddenC0de_balance = await browser.find_p_with_text(r'Balance:\s*.*', show_logs=2, item='button.text-gray-500', via_html=True)
                    if not H1ddenC0de_balance:
                        await browser.screenshoot(f"[{browser.uid}]: Failed to found 'Balance'")
                        logme(f"[{browser.uid}]: Failed to found 'Balance'")
                        return
                    else:


                        # Define a regex pattern to capture the numeric value after 'Balance:'
                        pattern = r'Balance:\s*([\d.]+)'

                        match = re.search(pattern, H1ddenC0de_balance)
                        if match:
                            balance_str = match.group(1)
                            H1ddenC0de_balance = float(balance_str)
                        else:
                            H1ddenC0de_balance = 0  # Default value or handle accordingly


                        try:
                            if task['type']=='Buy' and task['token0']=='USDC':
                                H1ddenC0de_balance = math.floor(H1ddenC0de_balance*100)/100
                        except Exception as e:
                            print(e)
                            H1ddenC0de_balance = 0



                    if H1ddenC0de_balance == available_max_balance:
                        await browser.make_screenshot(f"[{i_task}] Balance failed to to change - {task['market_id']}")

                        print(f"[{browser.uid}] Failed to swap")
                    else:
                        print(f"[{browser.uid}]: Balance changed after swap")
                        break




            if 'min_delay' in task and 'max_delay' in task:
                try:
                    r_delay = random.randint(task['min_delay'], task['max_delay'])
                    logme(f"Awaiting for {int(r_delay)} for next step by HiddenCode")
                    await asyncio.sleep(r_delay)
                except:
                    await asyncio.sleep(30)
            else:
                # logme(f"[{browser.uid}]: Task delay is zero:\n\n", "warning")
                await asyncio.sleep(30)

        # Keep the script running to interact with the browser
        logme(f"[{browser.uid}]: Do whatever you want...\n\n\n")
        # Optionally, you can cleanly close the browser after input

        await browser.close()



# Created by Aero25x

# For HiddenCode
# https://t.me/hidden_coding
