# KellyDr*iner
Automated tool that checks Roblox cookies and buys configured gamepasses.

## Features
- Scrapes cookies from input files (`robux*.txt` / `rap*.txt`)
- Checks account balance before purchasing
- Prioritizes higher-priced gamepasses first
- Automatically removes invalid or empty cookies
- Built-in rate limit handling
- Discord webhook notifications
- Optional bot token support

## Requirements
- Python 3.11.7 (recommended, other versions may work)

## Installation
```bash
pip install -r requirements.txt
```

## Config
Edit `input/config.json`:
```json
{
  "gamepasses": [
    {"id": 1720983217, "price": 5000},
    {"id": 1720681245, "price": 3000},
    {"id": 1721465215, "price": 2000},
    {"id": 1720513163, "price": 2000},
    {"id": 1722443040, "price": 1000},
    {"id": 1721615167, "price": 500},
    {"id": 1720603165, "price": 300},
    {"id": 1721951200, "price": 200},
    {"id": 1722323191, "price": 100},
    {"id": 1720959084, "price": 50},
    {"id": 1722065157, "price": 30},
    {"id": 1720597211, "price": 20},
    {"id": 1721087233, "price": 10},
    {"id": 1721705044, "price": 5},
    {"id": 1721049182, "price": 3},
    {"id": 1722377137, "price": 2}
  ],
  "delay": 3,
  "webhook": "",
  "user_id": "",
  "bot_token": ""
}
```

| Field | Description |
|-------|-------------|
| `gamepasses` | List of gamepass IDs and their prices |
| `delay` | Time (seconds) between each account |
| `webhook` | Discord webhook URL (optional) |
| `user_id` | Your Discord user ID (optional) |
| `bot_token` | You discord bot token (optional) |

## Input
Place cookie files in the `input/` folder. You can also just drop cookies directly into `cookies.txt`.

## Notes
- Gamepasses are purchased in descending price order
- Accounts with 0 Robux are automatically skipped and removed
- Invalid cookies are cleaned up automatically
- `delay` controls the wait time between processing accounts
- You can upload robux*.txt or rap*.txt files with u:p:c format in input folder 

## Disclaimer
For educational purposes only. Use at your own risk. I don't support hacking or brutting accounts

## Support
For technical help you can always open ticket on our server https://discord.gg/kellystock
