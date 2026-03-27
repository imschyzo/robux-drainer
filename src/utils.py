import os, sys, ctypes, time, threading
from datetime import datetime

def rgb(r, g, b):
    if os.name == 'nt':
        os.system("") 
    return f"\033[38;2;{r};{g};{b}m"

RESET = "\033[0m"
GRAY   = rgb(170, 170, 170)
GREEN  = rgb(80, 220, 140)
RED    = rgb(235, 95, 95)
BLUE   = rgb(120, 185, 255)
PURPLE = rgb(190, 145, 255)
YELLOW = rgb(255, 210, 110)

_total_tries = 0
_total_robux = 0
_total_cookies = 0
_app_name = "Buyer"
_start_time = time.time()

def set_app_name(name):
    global _app_name
    _app_name = name

def update_cookie_count():
    global _total_cookies
    try:
        path = os.path.join("input", "cookies.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                _total_cookies = sum(1 for line in f if line.strip())
        else:
            _total_cookies = 0
    except:
        _total_cookies = 0

def add_try():
    global _total_tries
    _total_tries += 1

def add_robux(amount):
    global _total_robux
    _total_robux += amount

def _title_worker():
    while True:
        uptime_seconds = int(time.time() - _start_time)
        m, s = divmod(uptime_seconds, 60)
        h, m = divmod(m, 60)
        uptime_str = f"{h:d}h {m:02d}m {s:02d}s"
        
        title = f"{_app_name} | Cookies: {_total_cookies} | Success: {_total_tries} | Drained: {_total_robux} R$ | Uptime: {uptime_str}"
        
        if os.name == "nt":
            ctypes.windll.kernel32.SetConsoleTitleW(title)
        else:
            sys.stdout.write(f"\x1b]0;{title}\x07")
        time.sleep(1)

def now():
    return datetime.now().strftime("%H:%M:%S")

def log(tag, msg, color=GRAY):
    print(f"{GRAY}[{now()}]{RESET} {color}{tag} {msg}{RESET}")

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

update_cookie_count()
threading.Thread(target=_title_worker, daemon=True).start()