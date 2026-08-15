import os

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN غير موجود في Environment Variables")

MONTHLY_URL = "https://streampay.sa/s/iuaYZ"

SEMI_URL = "https://streampay.sa/s/mBtYQ"

YEAR_URL = "https://streampay.sa/s/1PW2Q"


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    keyboard = [

        [
            InlineKeyboardButton(
                "💎 اشتراك شهري - 49 ريال",
                url=MONTHLY_URL
            )
        ],

        [
            InlineKeyboardButton(
                "⭐ اشتراك نصف سنوي بخصم 10% - 264.60 ريال",
                url=SEMI_URL
            )
        ],

        [
            InlineKeyboardButton(
                "🏆 اشتراك سنوي بخصم 20% - 470.70 ريال",
                url=YEAR_URL
            )
        ]

    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        """
مرحباً بك في نادي التحديات القيمية

رحلتك الممتعة نحو الغرس القيمي

فضلاً اختر خطة الاشتراك المناسبة:
        """,
        reply_markup=reply_markup
    )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

app.run_polling()
