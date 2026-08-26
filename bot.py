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

    await update.message.reply_text(
        "مرحباً بك في نادي التحديات القيمية 🌱\n\nاختر من القائمة التالية:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    print("BUTTON CLICKED:", query.data)

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
                    "⭐ نصف سنوي",
                    callback_data="semi"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏆 سنوي",
                    callback_data="year"
                )
            ]
        ]

        await query.message.reply_text(
            "اختر خطة الاشتراك:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "monthly":

        await query.message.reply_text(
            "تم اختيار الاشتراك الشهري."
        )

    elif query.data == "semi":

        await query.message.reply_text(
            "تم اختيار الاشتراك النصف سنوي."
        )

    elif query.data == "year":

        await query.message.reply_text(
            "تم اختيار الاشتراك السنوي."
        )

    elif query.data == "about":

        await query.message.reply_text(
            "نادي التحديات القيمية برنامج اشتراكي يهدف إلى تعزيز القيم من خلال أنشطة مستمرة."
        )


async def invite(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    invite_link = await context.bot.create_chat_invite_link(
        chat_id=CHANNEL_ID,
        member_limit=1
    )

    await update.message.reply_text(
        invite_link.invite_link
    )


app = Application.builder().token(BOT_TOKEN).build()

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


async def main():

    await app.initialize()

    await app.start()

    await app.updater.start_polling(
        drop_pending_updates=True
    )

    try:

        while True:
            await asyncio.sleep(3600)

    finally:

        await app.updater.stop()

        await app.stop()

        await app.shutdown()


if __name__ == "__main__":

    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    loop.run_until_complete(main())
