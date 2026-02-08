<div align="center">
  <h1>🎁 Telegram Gifts Tracker</h1>

  <p style="font-size: 18px; margin-bottom: 24px;">
    <b>Automated monitoring and notifications for new Telegram gifts and upgrades</b>
  </p>

[Report Bug](https://github.com/bohd4nx) · [Request Feature](https://github.com/bohd4nx) · [**Donate TON**](https://app.tonkeeper.com/transfer/UQCppfw5DxWgdVHf3zkmZS8k1mt9oAUYxQLwq2fz3nhO8No5)

</div>

---

## ✨ Features

- 🎁 **New Gifts Detection** - Automatically detects and announces new gifts in the Telegram store
- ⬆️ **Upgrade Monitoring** - Tracks when gifts become upgradeable and price changes
- 💎 **Sticker Management** - Downloads and uploads gift stickers to a dedicated channel
- 📊 **SQLite Database** - Stores gift history with async SQLAlchemy ORM

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/bohd4nx/GiftsTracker.git
cd GiftsTracker
pip install -r requirements.txt
```

### 2. Configuration

Copy example configuration and edit:

```bash
cp .env.example .env
```

Edit `.env` file:

```env
# Telegram API credentials
API_ID=your_api_id
API_HASH=your_api_hash
PHONE_NUMBER=+1234567890
PASSWORD=your_2fa_password

# Bot token
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Channels
CHANNEL_ID=-1001234567890
STICKERS_CHANNEL_ID=-1001234567890
STICKERS_CHANNEL_USERNAME=YourStickersChannel

# Settings
INTERVAL=45
```

### 3. Getting Required Data

#### 🔑 Telegram API Credentials

1. **Get API_ID and API_HASH**:
   - Visit [my.telegram.org/apps](https://my.telegram.org/apps)
   - Login with your phone number
   - Create a new application
   - Copy **API ID** → paste to `API_ID` in `.env`
   - Copy **API Hash** → paste to `API_HASH` in `.env`

2. **Phone Number & 2FA Password**:
   - `PHONE_NUMBER`: Your Telegram phone number in international format (e.g., `+1234567890`)
   - `PASSWORD`: Your Two-Factor Authentication password (leave empty if not enabled)

#### 🤖 Bot Token

1. **Create New Bot**:
   - Open Telegram and find [@BotFather](https://t.me/BotFather)
   - Send `/newbot` command
   - Follow instructions to create your bot
   - Copy the token → paste to `BOT_TOKEN` in `.env`

#### 📢 Notification Channel

1. **Create Public Channel**:
   - Create a new Telegram channel for gift notifications
   - Make it public (you can make it private later)
   - Add your bot as administrator with "Post Messages" permission

2. **Get Channel ID**:
   - Forward any message from channel to [@userinfobot](https://t.me/userinfobot)
   - Copy the **Chat ID** (format: `-100xxxxxxxxxx`)
   - Paste to `CHANNEL_ID` in `.env`

#### 🖼️ Stickers Channel

1. **Create Technical Channel**:
   - Create another channel for storing gift stickers
   - Set a unique username (e.g., `GiftsStickersCache`)
   - Add your bot as administrator

2. **Configure in .env**:
   - Get channel ID same way as notification channel
   - Paste ID to `STICKERS_CHANNEL_ID`
   - Paste username (without @) to `STICKERS_CHANNEL_USERNAME`

**Why separate channels?**

- Stickers channel acts as a CDN for gift animations
- Keeps notification channel clean
- Allows link previews with gift animations

#### ⚙️ Monitoring Interval

`INTERVAL` - Time in seconds between gift API checks (default: `45`)

- Minimum recommended: `30` seconds
- Adjust based on your needs (lower = faster detection, higher = less API calls)

**Start from scratch**: The bot will create `Gifts.db` automatically on first run.

### 5. Run the Bot

```bash
python main.py
```

**Expected output**:

```
[08.02.26 22:20:57] - INFO: Database initialized
[08.02.26 22:20:59] - INFO: Logged in as @your_username [123456789]
[08.02.26 22:20:59] - INFO: Starting gift check cycle #1
[08.02.26 22:21:00] - INFO: Found 0 new gifts to process
```

### Features Explained

#### New Gift Detection

When a new gift appears:

1. Bot fetches gift data from Telegram API
2. Downloads and uploads sticker to technical channel
3. Sends formatted notification to main channel
4. Saves gift to database

#### Upgrade Monitoring

When upgrade becomes available:

1. Detects `upgrade_price` field change from `None` to value
2. Sends new notification about upgrade availability
3. Stores upgrade message ID for future edits

When upgrade price changes:

1. Detects price difference in `upgrade_price`
2. Edits existing upgrade message with new price
3. Updates database record

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests

## 📜 License

This project is provided as-is for educational purposes.

---

<div align="center">

### Made with ❤️ by [@bohd4nx](https://t.me/bohd4nx)

**Star ⭐ this repo if you found it useful!**

[Donate TON](https://app.tonkeeper.com/transfer/UQCppfw5DxWgdVHf3zkmZS8k1mt9oAUYxQLwq2fz3nhO8No5)

</div>
