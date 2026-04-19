<div align="center">

<h1>Telegram Gifts Tracker</h1>

<p><b>Userbot that monitors new Telegram gifts, upgrade events and craft events — sends notifications and maintains a custom emoji pack.</b></p>

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Telegram](https://img.shields.io/badge/Channel-@GiftsTracker-2CA5E0?style=flat&logo=telegram&logoColor=white)](https://t.me/GiftsTracker)
[![Donate](https://img.shields.io/badge/Donate-TON-0098EA?style=flat&logo=ton&logoColor=white)](https://app.tonkeeper.com/transfer/UQCppfw5DxWgdVHf3zkmZS8k1mt9oAUYxQLwq2fz3nhO8No5)

</div>

---

## Features

- Detects new gifts in the Telegram store and sends rich notifications
- Monitors upgrade availability and tracks price changes on upgradeable gifts
- Tracks gift crafts and notifies when crafting events occur
- Uploads gift stickers to a dedicated channel for animated link previews
- Automatically builds and maintains a custom Telegram emoji pack
- Stores full gift history in SQLite via async SQLAlchemy
- `.status` command — shows DC, ping, uptime, polling interval and total gifts in DB

---

## Installation

```bash
git clone https://github.com/bohd4nx/GiftsTracker.git
cd GiftsTracker
pip install -e .
cp .env.example .env
```

Fill in `.env` (see [Configuration](#configuration) below), then:

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
| `PASSWORD`                  | 2FA password (leave empty if not set)                                       |
| `BOT_TOKEN`                 | Bot token from [@BotFather](https://t.me/BotFather)                         |
| `CHANNEL_ID`                | Notification channel ID (`-100xxxxxxxxxx`)                                  |
| `STICKERS_CHANNEL_ID`       | Channel ID used to host gift sticker files                                  |
| `STICKERS_CHANNEL_USERNAME` | Stickers channel username without `@`                                       |
| `INTERVAL`                  | Polling interval in seconds (default: `15`, min: `10`)                      |
| `EMOJI_PACK_SHORT_NAME`     | Short name for the custom emoji pack                                        |
| `EMOJI_PACK_TITLE`          | Display title for the emoji pack                                            |

> To get a channel ID: forward any message from the channel to [@userinfobot](https://t.me/userinfobot) and copy the Chat ID.

---

## Docker

**First run** must be interactive so Pyrogram can ask for the login code:

```bash
docker compose run --rm app
```

After login the session is saved to `./data/`. Press `Ctrl+C` to stop.

**Production:**

```bash
docker compose up -d
```

Useful commands:

```bash
docker compose logs -f              # live logs
docker compose restart              # restart
docker compose down                 # stop & remove
docker compose up -d --build        # rebuild & restart
```

> The `./data` directory is mounted to `/app/data` — it holds the SQLite database and session file.

---

## License

This project is provided as-is for educational purposes.

---

<div align="center">

### Made with ❤️ by [@bohd4nx](https://t.me/bohd4nx)

**Star ⭐ this repo if you found it useful!**

</div>

