# ChatHomeAssistant
Telegram controlled home assistant.

Used tools for telegram communication are [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot/tree/master) and [telegram-send](https://github.com/rahiel/telegram-send)


## App configuration
File named AppConfig.py must be added to source directory with the content below with changed parameters. At least the YOUR_TELEGRAM_ACCOUNT_TOKEN must be set.

```python

AppConfig = {
    "debug": "False",
    'bluetooth_enabled': 'False',
    'telegram_token': 'YOUR_TELEGRAM_ACCOUNT_TOKEN',
    'ble_scanner_fifo': '/tmp/ble_scanner_fifo'
}

```
