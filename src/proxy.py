import os
import random

INPUT_DIR = "input"
PROXIES_FILE = os.path.join(INPUT_DIR, "proxies.txt")

def load_proxies():
    if not os.path.exists(PROXIES_FILE):
        return []
    with open(PROXIES_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def format_proxy(proxy_str):
    """
    Supports:
    - 1.2.3.4:8080 (HTTP)
    - 1.2.3.4:8080:user:pass (HTTP Auth)
    - user:pass:1.2.3.4:8080 (HTTP Auth Alternate)
    - socks5://1.2.3.4:1080 (SOCKS5)
    - socks5://user:pass@1.2.3.4:1080 (SOCKS5 Auth)
    """
    proxy_str = proxy_str.replace(" ", "").lower()
    
    protocol = "http"
    if "socks5" in proxy_str:
        protocol = "socks5"
        proxy_str = proxy_str.replace("socks5://", "")
    elif "socks4" in proxy_str:
        protocol = "socks4"
        proxy_str = proxy_str.replace("socks4://", "")
    else:
        proxy_str = proxy_str.replace("http://", "").replace("https://", "")

    if "@" in proxy_str:
        p_url = f"{protocol}://{proxy_str}"
    elif proxy_str.count(":") == 3:
        parts = proxy_str.split(":")

        if "." in parts[0]: 
            p_url = f"{protocol}://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
        else:
            p_url = f"{protocol}://{parts[0]}:{parts[1]}@{parts[2]}:{parts[3]}"
    else:
        p_url = f"{protocol}://{proxy_str}"
    
    return {"http": p_url, "https": p_url}

def get_next_proxy(proxy_list):
    if not proxy_list:
        return None
    return format_proxy(random.choice(proxy_list))
