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
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN غير موجود")

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


async def invite(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        invite_link = await context.bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            member_limit=1
        )

        await update.message.reply_text(
            f"""
✅ تم إنشاء رابط الدخول

الرابط صالح لمستخدم واحد فقط:

{invite_link.invite_link}
"""
        )

    except Exception as e:

        await update.message.reply_text(
            f"حدث خطأ:\n{e}"
        )


app = Application.builder().token(
    BOT_TOKEN
).build()

app.add_handler(
    CommandHandler(
        "start",
        start
    )
)

app.add_handler(
    CommandHandler(
        "invite",
        invite
    )
)

app.run_polling()
