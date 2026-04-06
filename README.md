<div align="center">

  <h1>Telegram Gifts Tracker</h1>

  <p>
    <b>Userbot that monitors new Telegram gifts and upgrade events, sends notifications and maintains a custom emoji pack.</b>
  </p>

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Telegram](https://img.shields.io/badge/Subscribe-@GiftsTracker-2CA5E0?style=flat&logo=telegram&logoColor=white)](https://t.me/GiftsTracker)

[Report Bug](https://github.com/bohd4nx/GiftsTracker/issues) · [Request Feature](https://github.com/bohd4nx/GiftsTracker/issues) · [**Donate TON**](https://app.tonkeeper.com/transfer/UQCppfw5DxWgdVHf3zkmZS8k1mt9oAUYxQLwq2fz3nhO8No5)

</div>

---

## Features

- Detects new gifts in the Telegram store and sends notifications
- Monitors when gifts become upgradeable and tracks upgrade price changes
- Downloads gift stickers and uploads them to a dedicated channel for link previews
- Automatically builds and maintains a custom Telegram emoji pack from all gift stickers
- Stores full gift history in SQLite via async SQLAlchemy

---

## Installation

```bash
git clone https://github.com/bohd4nx/GiftsTracker.git
cd GiftsTracker
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your credentials (see [Configuration](#configuration) below), then run:

```bash
python main.py
```

---

## Configuration

| Variable                    | Description                                                                 |
| --------------------------- | --------------------------------------------------------------------------- |
| `API_ID`                    | Telegram API ID from [my.telegram.org/apps](https://my.telegram.org/apps)   |
| `API_HASH`                  | Telegram API Hash from [my.telegram.org/apps](https://my.telegram.org/apps) |
| `PHONE_NUMBER`              | Your phone number in international format (`+1234567890`)                   |
| `PASSWORD`                  | 2FA password (leave empty if not enabled)                                   |
| `BOT_TOKEN`                 | Bot token from [@BotFather](https://t.me/BotFather)                         |
| `CHANNEL_ID`                | Notification channel ID (format: `-100xxxxxxxxxx`)                          |
| `STICKERS_CHANNEL_ID`       | Stickers channel ID — used to host gift sticker files                       |
| `STICKERS_CHANNEL_USERNAME` | Stickers channel username without `@`                                       |
| `INTERVAL`                  | Polling interval in seconds (default: `15`, minimum: `10`)                  |
| `EMOJI_PACK_SHORT_NAME`     | Short name for the custom emoji pack                                        |
| `EMOJI_PACK_TITLE`          | Display title for the emoji pack                                            |

**Stickers channel** acts as a CDN for gift animations — the bot uploads each sticker there and uses it as a link preview source in notifications. Keep it separate from the main channel.

To get a channel ID: forward any message from the channel to [@userinfobot](https://t.me/userinfobot) and copy the Chat ID.

---

## How It Works

**New gift:** fetches gift data -> uploads sticker to stickers channel -> adds sticker to emoji pack -> sends notification with link preview.

**Upgrade available:** detects `upgrade_price` appearing on a previously tracked gift → sends upgrade notification → stores message ID for future edits.

**Upgrade price changed:** detects price difference → edits existing upgrade notification → updates DB record.

**Status command:** send `.status` in any chat where the userbot is active to see datacenter, ping, uptime, interval, and total gifts in DB.

---

## Docker

**First run** must be interactive for Pyrogram to prompt the Telegram login code:

```bash
docker build -t giftsTracker .
mkdir -p ~/giftsTracker/data

docker run -it --rm \
  --env-file .env \
  -v ~/giftsTracker/data:/app/data \
  giftsTracker
```

After successful login, session is saved to `~/giftsTracker/data/GiftsTracker.session`. Press Ctrl+C.

**Production:**

```bash
docker run -d --name giftsTracker \
  --env-file .env \
  --restart unless-stopped \
  -v ~/giftsTracker/data:/app/data \
  giftsTracker
```

```bash
docker logs -f giftsTracker                                          # live logs
docker restart giftsTracker                                          # restart
docker stop giftsTracker && docker rm giftsTracker                   # stop & remove
docker build -t giftsTracker . && docker restart giftsTracker        # rebuild & restart
```

> `/app/data` holds the SQLite database and Pyrogram session. Always mount it as a volume — data is lost if the container is removed without it.

---

## License

This project is provided as-is for educational purposes.

---

<div align="center">

### Made with ❤️ by [@bohd4nx](https://t.me/bohd4nx)

**Star ⭐ this repo if you found it useful!**

</div>

