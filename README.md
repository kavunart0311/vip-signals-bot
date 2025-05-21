# VIP Signals Telegram Bot

## Що це?
Telegram-бот, який отримує сигнали з TradingView через Webhook і надсилає їх в особистий чат.

---

## Як запустити на Render.com (без ПК)

1. Зареєструйся на https://render.com
2. Створи новий Web Service:
   - Обери Python 3
   - Завантаж цей репозиторій (архів з файлами main.py, config.json, requirements.txt)
   - Установи команду запуску:
     ```
     python3 main.py
     ```
   - Вкажи Environment Variables:
     - `TELEGRAM_TOKEN` — з config.json
     - `TELEGRAM_CHAT_ID` — з config.json
     - `WEBHOOK_SECRET` — з config.json
3. Запусти сервіс, отримай URL на кшталт https://your-service.onrender.com
4. В TradingView створи алерт із Webhook URL:
   ```
   https://your-service.onrender.com/webhook
   ```
   Додай заголовок:
   ```
   X-Webhook-Secret: mysecret123
   ```
5. В полі повідомлення в алерті вкажи JSON формату:
   ```json
   {
     "pair": "EUR/USD",
     "pattern": "Double Bottom",
     "direction": "UP",
     "timeframe": "1m",
     "RSI": 27,
     "SMA_signal": "below",
     "entry_price": 1.07145
   }
   ```
---

Якщо будуть питання — пиши!