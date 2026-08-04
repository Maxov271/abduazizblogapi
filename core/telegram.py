"""
Telegram bot orqali admin'ga xabar yuborish.
Sozlash: .env faylida TELEGRAM_BOT_TOKEN va TELEGRAM_CHAT_ID
(yoki admin panel -> Site sozlamalari -> shu maydonlar).

Chat ID'ni olish: botga /start yozing, so'ng
https://api.telegram.org/bot<TOKEN>/getUpdates manzilini oching,
javobdagi "chat":{"id": ...} qiymatini oling.
"""
import logging
import requests
from django.conf import settings
from .models import SiteSettings

logger = logging.getLogger(__name__)


def _credentials():
    site = SiteSettings.load()
    token = site.telegram_bot_token or settings.TELEGRAM_BOT_TOKEN
    chat_id = site.telegram_chat_id or settings.TELEGRAM_CHAT_ID
    return token, chat_id


def send_telegram_message(text: str) -> bool:
    token, chat_id = _credentials()
    if not token or not chat_id:
        logger.warning("Telegram bot sozlanmagan — xabar yuborilmadi.")
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        resp = requests.post(url, data={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
        }, timeout=5)
        return resp.ok
    except requests.RequestException:
        logger.exception("Telegramga xabar yuborishda xato")
        return False


def notify_new_comment(comment):
    target = comment.post.title if comment.post else "Umumiy sayt izohi"
    text = (
        f"🆕 <b>Yangi izoh</b>\n"
        f"Sahifa: {target}\n"
        f"Ism: {comment.name}\n"
        f"Email: {comment.email or '-'}\n\n"
        f"{comment.message}"
    )
    send_telegram_message(text)


def notify_new_contact_message(msg):
    text = (
        f"📩 <b>Yangi kontakt xabari</b>\n"
        f"Ism: {msg.name}\n"
        f"Email: {msg.email}\n\n"
        f"{msg.message}"
    )
    send_telegram_message(text)
