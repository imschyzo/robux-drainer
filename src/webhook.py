from datetime import datetime, timezone
import requests

def send_discord_webhook(webhook, username, user_id, gaid, cost, status_code, status_json, headshot_trash, userid):
    avatar_api_url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png&isCircular=false"
    final_img = "https://static.wikia.nocookie.net/roblox/images/6/66/Content_Deleted.png"
    
    try:
        response = requests.get(avatar_api_url)
        if response.status_code == 200:
            res_json = response.json()
            if "data" in res_json and len(res_json["data"]) > 0:
                final_img = res_json["data"][0].get("imageUrl", final_img)
    except Exception as e:
        print(f"Thumbnail Error: {e}")

    if isinstance(status_json, dict):
        p = status_json.get("purchased", False)
        status_text = "✅ Success" if p else "❌ Failed"
    else:
        status_text = f"Code: {status_code}"

    embed = {
        "title": f"@{username} ({user_id})",
        "color": 16777215 if "Success" in status_text else 0xFF0000,
        "thumbnail": {"url": final_img}, 
        "fields": [
            {"name": "Gamepass ID", "value": f"`{gaid}`", "inline": True},
            {"name": "Cost", "value": f"**{cost} R$**", "inline": True}
        ],
        "footer": {"text": "discord.gg/kellystock"},
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    data = {
        "content": f"<@{userid}>" if userid else "",
        "username": "kellydrainer",
        "embeds": [embed]
    }

    try:
        res = requests.post(webhook, json=data)
        if res.status_code not in [200, 204]:
            print(f"[!] Webhook failed with status {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[!] Critical Webhook Error: {e}")
