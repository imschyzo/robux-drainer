import requests

class CsrfError(Exception):
    pass

class RobloxSession:
    def __init__(self, cookie: str, proxies: dict = None):
        self.cookie = cookie
        self.session = requests.Session()

        if proxies:
            self.session.proxies.update(proxies)
            
        self.session.headers.update({
            "Cookie": f".ROBLOSECURITY={cookie}",
            "User-Agent": "Roblox/WinInet",
            "Accept": "application/json"
        })
        
        self.csrf = self._get_csrf()
        self.user_id, self.username = self._get_user()

    def get_balance(self):
        r = self.session.get(f"https://economy.roblox.com/v1/users/{self.user_id}/currency")
        if r.status_code != 200:
            return 0
        return r.json().get("robux", 0)

    def _get_csrf(self):
        r = self.session.post("https://auth.roblox.com/v2/logout")
        token = r.headers.get("x-csrf-token")
        if not token:
            raise CsrfError("CSRF token invalid, probably caused by invalid cookie")
        return token

    def _get_user(self):
        r = self.session.get("https://users.roblox.com/v1/users/authenticated")
        if r.status_code != 200:
            raise CsrfError("Invalid or expired cookie")
        data = r.json()
        return data["id"], data["name"]

    def get_headshot_url(self, size=150):
        return f"https://www.roblox.com/headshot-thumbnail/image?userId={self.user_id}&width={size}&height={size}&format=png"

    def get_gamepass_info(self, gaid):
        r = self.session.get(f"https://apis.roblox.com/game-passes/v1/game-passes/{gaid}/product-info")
        if r.status_code != 200:
            raise Exception("Failed to get gamepass info")
        return r.json()

    def buy_gamepass(self, gaid):
        info = self.get_gamepass_info(gaid)
        payload = {
            "expectedCurrency": 1,
            "expectedPrice": info["PriceInRobux"],
            "expectedSellerId": info["Creator"]["Id"]
        }
        headers = {"X-Csrf-Token": self.csrf}
        
        r = self.session.post(
            f"https://economy.roblox.com/v1/purchases/products/{info['ProductId']}",
            json=payload, 
            headers=headers
        )
        
        try:
            return r.status_code, r.json()
        except:
            return r.status_code, r.text
