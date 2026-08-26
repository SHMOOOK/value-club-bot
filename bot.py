import os
import asyncio

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
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
                "📋 خطط الاشتراك",
                callback_data="plans"
            )
        ],

        [
            InlineKeyboardButton(
                "ℹ️ عن النادي",
                callback_data="about"
            )
        ]

    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        """
مرحباً بك في نادي التحديات القيمية 🌱

رحلتك الممتعة نحو الغرس القيمي

اختر من القائمة التالية:
        """,
        reply_markup=reply_markup
    )


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if query.data == "plans":

        keyboard = [

            [
                InlineKeyboardButton(
                    "💎 اشتراك شهري - 49 ريال",
                    callback_data="monthly"
                )
            ],

            [
                InlineKeyboardButton(
                    "⭐ اشتراك نصف سنوي بخصم 10% - 264.60 ريال",
                 [
            InlineKeyboardButton(
                "📋 خطط الاشتراك",
                callback_data="plans"
            )
        ],

        [
            InlineKeyboardButton(
                "ℹ️ عن النادي",
                callback_data="about"
            )
        ]

    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        """
مرحباً بك في نادي التحديات القيمية 🌱

رحلتك الممتعة نحو الغرس القيمي

اختر من القائمة التالية:
        """,
        reply_markup=reply_markup
    )


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    if query.data == "plans":

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

        await query.message.reply_text(
            """
اختر خطة الاشتراك المناسبة:

💎 شهري (قيمة واحدة - 5 أنشطة تفاعلية)
⭐ نصف سنوي (6 قيم - 30 نشاط تفاعلي)
🏆 سنوي (12 قيمة - 60 نشاط تفاعلي)
            """,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "about":

        await query.message.reply_text(
            """
🌱 نادي التحديات القيمية

برنامج اشتراكي يهدف إلى تعزيز القيم من خلال تحديات وأنشطة عملية مستمرة.

للاشتراك اضغط على:
📋 خطط الاشتراك
"""
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

🔗 الرابط:

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

app.add_handler(
    CallbackQueryHandler(
        button_handler
    )
)

import asyncio


async def main():
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
