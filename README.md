
# 🚀 Simplified Binance Spot Testnet Trading Bot

A lightweight trading bot built in **Python** using the [Binance Spot Testnet](https://testnet.binance.vision).  
Supports **MARKET**, **LIMIT**, and **OCO (One Cancels the Other)** orders with both **CLI** and a simple **Tkinter GUI** interface.  
Perfect for learning algorithmic trading without risking real money.

---

## 📌 Features
- ✅ Place **MARKET**, **LIMIT**, and **OCO** orders (Buy/Sell).  
- ✅ Works on Binance Spot **Testnet API** (no KYC needed).  
- ✅ **Command-line interface (CLI)** for quick trading.  
- ✅ **Lightweight Tkinter GUI** for easy interaction.  
- ✅ **Secure API key handling** using `.env` file.  
- ✅ **Logging** of all requests, responses, and errors.  
- ✅ (Optional) View balances of your account.  

---

## ⚙️ Requirements
- Python 3.8+  
- Binance Testnet account → [https://testnet.binance.vision](https://testnet.binance.vision)  
- Dependencies (install via `pip`):

```bash
pip install -r requirements.txt
````

### `requirements.txt`

```
python-binance
python-dotenv
```

(Tkinter usually comes pre-installed with Python on most systems.)

---

## 🔑 Setup

1. **Clone this repository:**

   ```bash
   git clone https://github.com/YOUR_USERNAME/binance-trading-bot.git
   cd binance-trading-bot
   ```

2. **Create a `.env` file** in the root folder:

   ```ini
   API_KEY=your_api_key_here
   API_SECRET=your_api_secret_here
   ```

3. **Run the bot.**

---

## 🖥️ Usage

### CLI Mode

Run with parameters:

```bash
python trading_bot.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

#### Examples:

* **Market Buy:**

  ```bash
  python trading_bot.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
  ```

* **Limit Sell:**

  ```bash
  python trading_bot.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 30000
  ```

* **OCO Order:**

  ```bash
  python trading_bot.py --symbol BTCUSDT --side SELL --type OCO --quantity 0.01 --price 31000 --stop-price 29500 --stop-limit-price 29400
  ```

---

### GUI Mode

Launch a simple Tkinter interface:

```bash
python trading_bot.py --gui
```

**Features:**

* Enter **symbol, side, type, quantity, price, stop prices**.
* Place orders with one click.
* See order responses in a popup window.

---

## 📒 Logs

All logs are stored in:

```
logs/bot.log
```

with automatic rotation (up to 3 files, 1MB each).

---

## ⚠️ Disclaimer

This bot is for **educational purposes only**.

* It connects only to the **Binance Spot Testnet**.
* Never share your API keys.
* Add `.env` to your `.gitignore` before pushing to GitHub.

---

