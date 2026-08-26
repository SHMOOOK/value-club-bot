import os
import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

MONTHLY_URL = "https://streampay.sa/s/iuaYZ"
SEMI_URL = "https://streampay.sa/s/mBtYQ"
YEAR_URL = "https://streampay.sa/s/1PW2Q"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

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

    await update.message.reply_text(
        "مرحباً بك في نادي التحديات القيمية 🌱\n\nاختر من القائمة التالية:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "plans":

        keyboard = [
            [
                InlineKeyboardButton(
                    "💎 شهري - 49 ريال",
                    callback_data="monthly"
                )
            ],
            [
                InlineKeyboardButton(
                    "⭐ نصف سنوي بخصم 10% - 264.60 ريال بدلا من 294 ريال",
                    callback_data="semi"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏆 سنوي بخصم 20% - 470.70 ريال بدلا من 588 ريال",
                    callback_data="year"
                )
            ]
        ]

        await query.message.reply_text(
            "اختر خطة الاشتراك المناسبة:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "monthly":

        user_id = query.from_user.id

        keyboard = [
            [
                InlineKeyboardButton(
                    "💳 الانتقال للدفع",
                    url=MONTHLY_URL
                )
            ]
        ]

        await query.message.reply_text(
            f"""💎 الاشتراك الشهري

رقم العضوية الخاص بك:

{user_id}

انسخ هذا الرقم وضعه في حقل:

رقم العضوية في تيليجرام

داخل نموذج الدفع.
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "semi":

        user_id = query.from_user.id

        keyboard = [
            [
                InlineKeyboardButton(
                    "💳 الانتقال للدفع",
                    url=SEMI_URL
                )
            ]
        ]

        await query.message.reply_text(
            f"""⭐ الاشتراك نصف السنوي

رقم العضوية الخاص بك:

{user_id}

انسخ هذا الرقم وضعه في حقل:

رقم العضوية في تيليجرام

داخل نموذج الدفع.
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "year":

        user_id = query.from_user.id

        keyboard = [
            [
                InlineKeyboardButton(
                    "💳 الانتقال للدفع",
                    url=YEAR_URL
                )
            ]
        ]

        await query.message.reply_text(
            f"""🏆 الاشتراك السنوي

رقم العضوية الخاص بك:

{user_id}

انسخ هذا الرقم وضعه في حقل:

رقم العضوية في تيليجرام

داخل نموذج الدفع.
""",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "about":

        await query.message.reply_text(
            "نادي التحديات القيمية برنامج اشتراكي يهدف إلى تعزيز القيم من خلال أنشطة وتحديات مستمرة."
        )


async def invite(update: Update, context: ContextTypes.DEFAULT_TYPE):

    invite_link = await context.bot.create_chat_invite_link(
        chat_id=CHANNEL_ID,
        member_limit=1
    )

    await update.message.reply_text(
        f"رابط الدعوة:\n{invite_link.invite_link}"
    )


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("invite", invite))
app.add_handler(CallbackQueryHandler(button_handler))


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
