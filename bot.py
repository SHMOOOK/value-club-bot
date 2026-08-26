import os
import asyncio
import requests

from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

STREAMPAY_API_KEY = os.getenv("STREAMPAY_API_KEY")

FORM_ID = "06e03f83-63b4-4c61-9f3a-6218985e824b"

MONTHLY_PRODUCT_ID = "bc2efc35-de79-45f6-90c0-1e818afa416d"
SEMI_PRODUCT_ID = "be42362d-af9d-415d-9543-876821cac8a2"
YEAR_PRODUCT_ID = "871271af-546a-4ea8-b5b5-21e644535fa1"


def create_payment_link(
    telegram_id: int,
    plan_name: str,
    product_id: str
):

    response = requests.post(
        "https://stream-app-service.streampay.sa/api/v2/payment_links",
        headers={
            "x-api-key": STREAMPAY_API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        json={
            "name": plan_name,
            "currency": "SAR",
            "max_number_of_payments": 1,
            "contact_information_type": "PHONE",
            "form_id": FORM_ID,
            "custom_metadata": {
                "telegram_id": str(telegram_id)
            },
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 1
                }
            ]
        },
        timeout=30
    )

    print("=" * 50)
    print("STREAM STATUS:")
    print(response.status_code)

    print("=" * 50)
    print("STREAM BODY:")
    print(response.text)

    print("=" * 50)

    response.raise_for_status()

    data = response.json()

    return data["url"]


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

    if query.data == "plans":

        keyboard = [
            [
                InlineKeyboardButton(
                    "💎 شهري - 49 ريالا فقط",
                    callback_data="monthly"
                )
            ],
            [
                InlineKeyboardButton(
                    "⭐ 6 أشهر 10% (264.60 بدل 294 ريال)",
                    callback_data="semi"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏆 سنوي 20% (470.70 بدل 588 ريال)",
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

        try:

            payment_url = create_payment_link(
                telegram_id=
